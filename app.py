import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Nutrition Tracker",
    page_icon="🥗",
    layout="centered"
)

# ---------------- TITLE ---------------- #

st.title("🥗 AI Nutrition Tracker")
st.write("Get accurate nutrition facts directly from USDA.")

# ---------------- USDA API KEY ---------------- #
# Replace with your real USDA API key

API_KEY = "P73wIVJPiCNTOFtegbe97NOAyX8cCif4fDzCwk07"

# ---------------- SEARCH FUNCTION ---------------- #

def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 20,
        "dataType": ["Foundation", "SR Legacy"]
    }

    response = requests.get(url, params=params)

    data = response.json()

    if "foods" not in data:
        return []

    foods = data["foods"]

    # Prioritize exact matches
    exact_matches = []

    for food in foods:

        description = food.get("description", "").lower()

        if food_name.lower() in description:
            exact_matches.append(food)

    if exact_matches:
        return exact_matches

    return foods

# ---------------- GET NUTRIENT ---------------- #

def get_nutrient(nutrients, nutrient_name):

    for nutrient in nutrients:

        if nutrient.get("nutrientName") == nutrient_name:
            return nutrient.get("value", 0)

    return 0

# ---------------- USER INPUT ---------------- #

food_query = st.text_input(
    "🍗 Enter Food Name",
    placeholder="Example: chicken breast, rice, banana"
)

grams = st.number_input(
    "⚖️ Enter grams",
    min_value=1,
    value=100
)

# ---------------- SEARCH RESULTS ---------------- #

if food_query:

    foods = search_food(food_query)

    if foods:

        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")

            category = food.get("foodCategory", "")

            label = description

            if category:
                label += f" | {category}"

            food_options[label] = food

        selected_food_label = st.selectbox(
            "✅ Select Exact Food Match",
            list(food_options.keys())
        )

        selected_food = food_options[selected_food_label]

        # ---------------- BUTTON ---------------- #

        if st.button("🔍 Get Nutrition Facts"):

            nutrients = selected_food.get("foodNutrients", [])

            calories = get_nutrient(nutrients, "Energy")
            protein = get_nutrient(nutrients, "Protein")
            carbs = get_nutrient(nutrients, "Carbohydrate, by difference")
            fats = get_nutrient(nutrients, "Total lipid (fat)")
            fiber = get_nutrient(nutrients, "Fiber, total dietary")
            sugar = get_nutrient(nutrients, "Sugars, total including NLEA")

            # Scale nutrients based on grams

            calories = (calories * grams) / 100
            protein = (protein * grams) / 100
            carbs = (carbs * grams) / 100
            fats = (fats * grams) / 100
            fiber = (fiber * grams) / 100
            sugar = (sugar * grams) / 100

            # ---------------- RESULTS ---------------- #

            st.markdown("---")

            st.subheader(f"📊 Nutrition Facts for {grams}g")

            st.success(selected_food_label)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🔥 Calories", f"{calories:.2f} kcal")
                st.metric("💪 Protein", f"{protein:.2f} g")
                st.metric("🍞 Carbs", f"{carbs:.2f} g")

            with col2:
                st.metric("🥑 Fats", f"{fats:.2f} g")
                st.metric("🌾 Fiber", f"{fiber:.2f} g")
                st.metric("🍬 Sugar", f"{sugar:.2f} g")

            # ---------------- TABLE ---------------- #

            nutrition_table = pd.DataFrame({

                "Nutrient": [
                    "Calories",
                    "Protein",
                    "Carbohydrates",
                    "Fats",
                    "Fiber",
                    "Sugar"
                ],

                "Amount": [
                    f"{calories:.2f} kcal",
                    f"{protein:.2f} g",
                    f"{carbs:.2f} g",
                    f"{fats:.2f} g",
                    f"{fiber:.2f} g",
                    f"{sugar:.2f} g"
                ]

            })

            st.markdown("---")
            st.table(nutrition_table)

    else:
        st.error("❌ No foods found. Try another search.")
