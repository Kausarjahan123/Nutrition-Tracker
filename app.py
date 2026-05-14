import streamlit as st
import requests
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Nutrition Tracker",
    page_icon="🥗",
    layout="centered"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🥗 AI Nutrition Tracker")
st.write("Get complete nutritional facts using USDA data with intelligent food matching.")

# ---------------------------------------------------
# USDA API KEY
# ---------------------------------------------------

API_KEY = "P73wIVJPiCNTOFtegbe97NOAyX8cCif4fDzCwk07"

# ---------------------------------------------------
# USDA SEARCH
# ---------------------------------------------------

def search_food(food_name):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 25
    }

    try:

        response = requests.get(url, params=params)
        data = response.json()

        if "foods" not in data:
            return []

        foods = data["foods"]

        # PRIORITIZE REAL / FOUNDATION FOODS
        priority_foods = []

        for food in foods:

            data_type = food.get("dataType", "")

            if data_type in ["Foundation", "SR Legacy"]:
                priority_foods.append(food)

        if priority_foods:
            return priority_foods

        return foods

    except:
        return []

# ---------------------------------------------------
# GET NUTRIENT
# ---------------------------------------------------

def get_nutrient(nutrients, nutrient_name, unit=None):

    for nutrient in nutrients:

        name = nutrient.get("nutrientName", "")
        nutrient_unit = nutrient.get("unitName", "")
        value = nutrient.get("value", 0)

        if name == nutrient_name:

            if unit:

                if nutrient_unit == unit:
                    return value

            else:
                return value

    return 0

# ---------------------------------------------------
# SCALE VALUES
# ---------------------------------------------------

def scale(value, grams):

    return (value * grams) / 100

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

food_query = st.text_input(
    "🍗 Enter Food Name",
    placeholder="Examples: chicken breast, banana, white rice, egg"
)

grams = st.number_input(
    "⚖️ Enter grams",
    min_value=1,
    value=100
)

# ---------------------------------------------------
# SEARCH RESULTS
# ---------------------------------------------------

if food_query:

    foods = search_food(food_query)

    # ---------------------------------------------------
    # FOOD FOUND
    # ---------------------------------------------------

    if foods:

        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")
            category = food.get("foodCategory", "")
            data_type = food.get("dataType", "")

            label = f"{description}"

            if category:
                label += f" | {category}"

            if data_type:
                label += f" | {data_type}"

            food_options[label] = food

        selected_food_label = st.selectbox(
            "✅ Select Best Match",
            list(food_options.keys())
        )

        selected_food = food_options[selected_food_label]

        # ---------------------------------------------------
        # BUTTON
        # ---------------------------------------------------

        if st.button("🔍 Get Complete Nutrition Facts"):

            nutrients = selected_food.get("foodNutrients", [])

            # ---------------------------------------------------
            # MACROS
            # ---------------------------------------------------

            calories = get_nutrient(nutrients, "Energy", "KCAL")
            protein = get_nutrient(nutrients, "Protein")
            carbs = get_nutrient(nutrients, "Carbohydrate, by difference")
            fats = get_nutrient(nutrients, "Total lipid (fat)")
            fiber = get_nutrient(nutrients, "Fiber, total dietary")
            sugar = get_nutrient(nutrients, "Sugars, total including NLEA")

            saturated_fat = get_nutrient(
                nutrients,
                "Fatty acids, total saturated"
            )

            cholesterol = get_nutrient(
                nutrients,
                "Cholesterol"
            )

            sodium = get_nutrient(
                nutrients,
                "Sodium, Na"
            )

            potassium = get_nutrient(
                nutrients,
                "Potassium, K"
            )

            calcium = get_nutrient(
                nutrients,
                "Calcium, Ca"
            )

            iron = get_nutrient(
                nutrients,
                "Iron, Fe"
            )

            vitamin_c = get_nutrient(
                nutrients,
                "Vitamin C, total ascorbic acid"
            )

            vitamin_a = get_nutrient(
                nutrients,
                "Vitamin A, IU"
            )

            # ---------------------------------------------------
            # SCALE ALL VALUES
            # ---------------------------------------------------

            calories = scale(calories, grams)
            protein = scale(protein, grams)
            carbs = scale(carbs, grams)
            fats = scale(fats, grams)
            fiber = scale(fiber, grams)
            sugar = scale(sugar, grams)

            saturated_fat = scale(saturated_fat, grams)
            cholesterol = scale(cholesterol, grams)
            sodium = scale(sodium, grams)
            potassium = scale(potassium, grams)
            calcium = scale(calcium, grams)
            iron = scale(iron, grams)
            vitamin_c = scale(vitamin_c, grams)
            vitamin_a = scale(vitamin_a, grams)

            # ---------------------------------------------------
            # RESULTS
            # ---------------------------------------------------

            st.markdown("---")

            st.subheader(f"📊 Complete Nutrition Facts ({grams}g)")

            st.success(selected_food_label)

            # ---------------------------------------------------
            # MAIN METRICS
            # ---------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🔥 Calories", f"{calories:.2f} kcal")
                st.metric("💪 Protein", f"{protein:.2f} g")
                st.metric("🍞 Carbs", f"{carbs:.2f} g")

            with col2:
                st.metric("🥑 Fats", f"{fats:.2f} g")
                st.metric("🌾 Fiber", f"{fiber:.2f} g")
                st.metric("🍬 Sugar", f"{sugar:.2f} g")

            with col3:
                st.metric("🧈 Saturated Fat", f"{saturated_fat:.2f} g")
                st.metric("🩸 Cholesterol", f"{cholesterol:.2f} mg")
                st.metric("🧂 Sodium", f"{sodium:.2f} mg")

            # ---------------------------------------------------
            # VITAMINS & MINERALS
            # ---------------------------------------------------

            st.markdown("---")
            st.subheader("🧬 Vitamins & Minerals")

            col4, col5 = st.columns(2)

            with col4:
                st.metric("🍌 Potassium", f"{potassium:.2f} mg")
                st.metric("🦴 Calcium", f"{calcium:.2f} mg")
                st.metric("🩸 Iron", f"{iron:.2f} mg")

            with col5:
                st.metric("🍊 Vitamin C", f"{vitamin_c:.2f} mg")
                st.metric("🥕 Vitamin A", f"{vitamin_a:.2f} IU")

            # ---------------------------------------------------
            # FULL TABLE
            # ---------------------------------------------------

            st.markdown("---")
            st.subheader("📋 Full Nutrition Table")

            nutrition_table = pd.DataFrame({

                "Nutrient": [

                    "Calories",
                    "Protein",
                    "Carbohydrates",
                    "Fats",
                    "Fiber",
                    "Sugar",
                    "Saturated Fat",
                    "Cholesterol",
                    "Sodium",
                    "Potassium",
                    "Calcium",
                    "Iron",
                    "Vitamin C",
                    "Vitamin A"

                ],

                "Amount": [

                    f"{calories:.2f} kcal",
                    f"{protein:.2f} g",
                    f"{carbs:.2f} g",
                    f"{fats:.2f} g",
                    f"{fiber:.2f} g",
                    f"{sugar:.2f} g",
                    f"{saturated_fat:.2f} g",
                    f"{cholesterol:.2f} mg",
                    f"{sodium:.2f} mg",
                    f"{potassium:.2f} mg",
                    f"{calcium:.2f} mg",
                    f"{iron:.2f} mg",
                    f"{vitamin_c:.2f} mg",
                    f"{vitamin_a:.2f} IU"

                ]

            })

            st.table(nutrition_table)

    # ---------------------------------------------------
    # NO FOOD FOUND
    # ---------------------------------------------------

    else:

        st.warning(
            "⚠️ Exact USDA food not found. Try a more general food name."
        )
