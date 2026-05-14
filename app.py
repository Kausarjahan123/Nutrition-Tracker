import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="AI Nutrition Tracker",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 AI Nutrition Tracker")
st.write("Smart USDA-based nutrition with intelligent food matching")

API_KEY = "P73wIVJPiCNTOFtegbe97NOAyX8cCif4fDzCwk07"

# ---------------- SMART SCORING ---------------- #

def score_food(food, query):

    text = food.get("description", "").lower()
    data_type = food.get("dataType", "")
    category = food.get("foodCategory", "").lower()

    score = 0
    query = query.lower()

    # exact match boost
    if query in text:
        score += 60

    # word overlap
    for word in query.split():
        if word in text:
            score += 10

    # strong mismatch penalties
    if "basmati" in query and "glutinous" in text:
        score -= 100

    if "rice" in query and "noodle" in text:
        score -= 90

    if "chicken" in query and "beef" in text:
        score -= 100

    # prefer clean datasets
    if data_type in ["SR Legacy", "Foundation"]:
        score += 10

    return score


# ---------------- USDA SEARCH ---------------- #

def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 25
    }

    response = requests.get(url, params=params)
    data = response.json()

    foods = data.get("foods", [])

    # rank results intelligently
    ranked = sorted(
        foods,
        key=lambda x: score_food(x, food_name),
        reverse=True
    )

    return ranked


# ---------------- NUTRIENT FETCH ---------------- #

def get_nutrient(nutrients, name, unit=None):

    for n in nutrients:

        if n.get("nutrientName") == name:

            if unit:
                if n.get("unitName") == unit:
                    return n.get("value", 0)
            else:
                return n.get("value", 0)

    return 0


# ---------------- CONFIDENCE ---------------- #

def confidence(food, query):

    text = food.get("description", "").lower()

    score = 0

    if query.lower() in text:
        score += 60

    for w in query.lower().split():
        if w in text:
            score += 10

    return min(score, 100)


# ---------------- INPUT ---------------- #

food_query = st.text_input("🍗 Enter Food Name")
grams = st.number_input("⚖️ Enter grams", min_value=1, value=100)


# ---------------- MAIN ---------------- #

if food_query:

    foods = search_food(food_query)

    if foods:

        options = {}

        for f in foods:

            label = f"{f.get('description','Unknown')} | {f.get('foodCategory','')} | {f.get('dataType','')}"
            options[label] = f

        selected_label = st.selectbox("✅ Select Best Match", list(options.keys()))
        selected_food = options[selected_label]

        if st.button("🔍 Get Nutrition Facts"):

            nutrients = selected_food.get("foodNutrients", [])

            calories = get_nutrient(nutrients, "Energy", "KCAL")
            protein = get_nutrient(nutrients, "Protein")
            carbs = get_nutrient(nutrients, "Carbohydrate, by difference")
            fats = get_nutrient(nutrients, "Total lipid (fat)")
            fiber = get_nutrient(nutrients, "Fiber, total dietary")
            sugar = (
    get_nutrient(nutrients, "Sugars, total including NLEA")
    or get_nutrient(nutrients, "Total Sugars")
    or 0
)

            # scaling
            def scale(x): return (x * grams) / 100

            calories = scale(calories)
            protein = scale(protein)
            carbs = scale(carbs)
            fats = scale(fats)
            fiber = scale(fiber)
            sugar = scale(sugar)

            # confidence
            conf = confidence(selected_food, food_query)

            st.markdown("---")
            st.subheader(f"📊 Nutrition for {grams}g")

            st.success(selected_food["description"])

            st.info(f"Match Confidence: {conf}%")

            if conf < 60:
                st.warning("⚠️ This may not be an exact match. Values are approximate.")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🔥 Calories", f"{calories:.2f} kcal")
                st.metric("💪 Protein", f"{protein:.2f} g")
                st.metric("🍞 Carbs", f"{carbs:.2f} g")

            with col2:
                st.metric("🥑 Fats", f"{fats:.2f} g")
                st.metric("🌾 Fiber", f"{fiber:.2f} g")
                st.metric("🍬 Sugar", f"{sugar:.2f} g")

            st.markdown("---")

            st.table(pd.DataFrame({
                "Nutrient": ["Calories","Protein","Carbs","Fats","Fiber","Sugar"],
                "Amount": [
                    f"{calories:.2f}",
                    f"{protein:.2f}",
                    f"{carbs:.2f}",
                    f"{fats:.2f}",
                    f"{fiber:.2f}",
                    f"{sugar:.2f}"
                ]
            }))

    else:
        st.error("No foods found. Try a simpler name.")
