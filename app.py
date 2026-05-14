import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Nutrition Tracker",
    page_icon="🥗",
    layout="centered"
)

# ---------------- TITLE ---------------- #
st.title("🥗 AI Nutrition Tracker")
st.write("Search any food and get accurate nutrition facts from USDA.")

# ---------------- USDA API ---------------- #
API_KEY = "P73wIVJPiCNTOFtegbe97NOAyX8cCif4fDzCwk07"

# ---------------- SEARCH FUNCTION ---------------- #
def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 10
    }

    try:
        response = requests.get(url, params=params)

        # DEBUG
        st.write("Status Code:", response.status_code)

        data = response.json()

        # DEBUG
        st.write(data)

        if "foods" in data:
            return data["foods"]

        return []

    except Exception as e:
        st.error(f"Error: {e}")
        return []

# ---------------- USER INPUT ---------------- #
food_query = st.text_input("🍗 Search Food")

grams = st.number_input(
    "⚖️ Enter grams",
    min_value=1,
    value=100
)

# ---------------- FOOD SEARCH ---------------- #
if food_query:

    foods = search_food(food_query)

    if foods:

        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")

            brand = food.get("brandOwner", "")

            category = food.get("foodCategory", "")

            label = description

            if brand:
                label += f" | {brand}"

            if category:
                label += f" | {category}"

            food_options[label] = food

        selected_food_label = st.selectbox(
            "✅ Select Exact Food",
            list(food_options.keys())
        )

        selected_food = food_options[selected_food_label]

        # ---------------- BUTTON ---------------- #
        if st.button("🔍 Get Nutrition Facts"):

            nutrients = selected_food.get("foodNutrients", [])

            protein = 0
            carbs = 0
            fats = 0
            calories = 0
            fiber = 0
            sugar = 0

            for nutrient in nutrients:

                name = nutrient.get("nutrientName", "")
                value = nutrient.get("value", 0)

                adjusted = (value * grams) / 100

                # Calories
                if name == "Energy":
                    calories = adjusted

                # Protein
                elif name == "Protein":
                    protein = adjusted

                # Carbs
                elif name == "Carbohydrate, by difference":
                    carbs = adjusted

                # Fat
                elif name == "Total lipid (fat)":
                    fats = adjusted

                # Fiber
                elif name == "Fiber, total dietary":
                    fiber = adjusted

                # Sugar
                elif name == "Sugars, total including NLEA":
                    sugar = adjusted

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
                    "Carbs",
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

            st.table(nutrition_table)

    else:
        st.error("❌ No foods found.")
