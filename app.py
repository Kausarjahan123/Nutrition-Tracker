import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Nutrition Tracker",
    page_icon="🥗",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00FFAA;
    text-align: center;
}

.stTextInput > div > div > input {
    background-color: #262730;
    color: white;
}

.stNumberInput input {
    background-color: #262730;
    color: white;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #262730;
    color: white;
}

div.stButton > button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #00cc88;
    color: white;
}

.metric-container {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🥗 AI Nutrition Tracker")
st.write("Search foods from USDA database and get accurate nutrition facts.")

# ---------------- USDA API ---------------- #
API_KEY = "YOUR_USDA_API_KEY"

# ---------------- SEARCH FUNCTION ---------------- #
def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 10
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    if "foods" in data:
        return data["foods"]

    return []

# ---------------- USER INPUT ---------------- #
food_query = st.text_input("🍗 Search Food")

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

            brand = food.get("brandOwner", "")

            food_category = food.get("foodCategory", "")

            label = description

            if brand:
                label += f" | {brand}"

            if food_category:
                label += f" | {food_category}"

            food_options[label] = food

        selected_label = st.selectbox(
            "✅ Select Exact Food Item",
            list(food_options.keys())
        )

        selected_food = food_options[selected_label]

        # ---------------- BUTTON ---------------- #
        if st.button("🔍 Get Accurate Nutrition"):

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

                adjusted_value = (value * grams) / 100

                # Protein
                if name == "Protein":
                    protein = adjusted_value

                # Carbs
                elif name == "Carbohydrate, by difference":
                    carbs = adjusted_value

                # Fat
                elif name == "Total lipid (fat)":
                    fats = adjusted_value

                # Calories
                elif name == "Energy":
                    calories = adjusted_value

                # Fiber
                elif name == "Fiber, total dietary":
                    fiber = adjusted_value

                # Sugar
                elif name == "Sugars, total including NLEA":
                    sugar = adjusted_value

            # ---------------- RESULTS ---------------- #
            st.markdown("---")

            st.subheader(f"📊 Nutrition Facts for {grams}g")

            st.success(selected_label)

            # Metrics
            col1, col2 = st.columns(2)

            with col1:
                st.metric("🔥 Calories", f"{calories:.2f} kcal")
                st.metric("💪 Protein", f"{protein:.2f} g")
                st.metric("🍞 Carbs", f"{carbs:.2f} g")

            with col2:
                st.metric("🥑 Fats", f"{fats:.2f} g")
                st.metric("🌾 Fiber", f"{fiber:.2f} g")
                st.metric("🍬 Sugar", f"{sugar:.2f} g")

            # ---------------- MACRO TABLE ---------------- #
            st.markdown("---")

            nutrition_data = {
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
            }

            df = pd.DataFrame(nutrition_data)

            st.table(df)

    else:
        st.error("❌ No foods found. Try another search.")
