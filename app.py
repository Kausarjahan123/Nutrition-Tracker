import streamlit as st
import requests

st.set_page_config(page_title="AI Nutrition Tracker", layout="centered")

# ---------------- UI ---------------- #
st.title("🥗 AI Nutrition Tracker")
st.write("Search foods from USDA database with accurate nutrition facts.")

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
    data = response.json()

    if "foods" in data:
        return data["foods"]

    return []

# ---------------- USER INPUT ---------------- #
food_query = st.text_input("🍗 Search Food")

grams = st.number_input("⚖️ Enter grams", min_value=1, value=100)

# ---------------- SEARCH RESULTS ---------------- #
if food_query:

    foods = search_food(food_query)

    if foods:

        # create dropdown options
        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")

            brand = food.get("brandOwner", "")

            label = f"{description} ({brand})" if brand else description

            food_options[label] = food

        selected_label = st.selectbox(
            "Select exact food item",
            list(food_options.keys())
        )

        selected_food = food_options[selected_label]

        # ---------------- BUTTON ---------------- #
        if st.button("Get Accurate Nutrition"):

            nutrients = selected_food.get("foodNutrients", [])

            protein = carbs = fats = calories = 0

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

                # Fats
                elif name == "Total lipid (fat)":
                    fats = adjusted_value

                # Calories
                elif name == "Energy":
                    calories = adjusted_value

            # ---------------- RESULTS ---------------- #
            st.markdown("---")

            st.subheader(f"Nutrition Facts for {grams}g")

            st.success(selected_label)

            st.metric("🔥 Calories", f"{calories:.2f} kcal")
            st.metric("💪 Protein", f"{protein:.2f} g")
            st.metric("🍞 Carbs", f"{carbs:.2f} g")
            st.metric("🥑 Fats", f"{fats:.2f} g")

    else:
        st.error("No foods found.")import streamlit as st
import requests

st.set_page_config(page_title="AI Nutrition Tracker", layout="centered")

# ---------------- UI ---------------- #
st.title("🥗 AI Nutrition Tracker")
st.write("Search foods from USDA database with accurate nutrition facts.")

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
    data = response.json()

    if "foods" in data:
        return data["foods"]

    return []

# ---------------- USER INPUT ---------------- #
food_query = st.text_input("🍗 Search Food")

grams = st.number_input("⚖️ Enter grams", min_value=1, value=100)

# ---------------- SEARCH RESULTS ---------------- #
if food_query:

    foods = search_food(food_query)

    if foods:

        # create dropdown options
        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")

            brand = food.get("brandOwner", "")

            label = f"{description} ({brand})" if brand else description

            food_options[label] = food

        selected_label = st.selectbox(
            "Select exact food item",
            list(food_options.keys())
        )

        selected_food = food_options[selected_label]

        # ---------------- BUTTON ---------------- #
        if st.button("Get Accurate Nutrition"):

            nutrients = selected_food.get("foodNutrients", [])

            protein = carbs = fats = calories = 0

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

                # Fats
                elif name == "Total lipid (fat)":
                    fats = adjusted_value

                # Calories
                elif name == "Energy":
                    calories = adjusted_value

            # ---------------- RESULTS ---------------- #
            st.markdown("---")

            st.subheader(f"Nutrition Facts for {grams}g")

            st.success(selected_label)

            st.metric("🔥 Calories", f"{calories:.2f} kcal")
            st.metric("💪 Protein", f"{protein:.2f} g")
            st.metric("🍞 Carbs", f"{carbs:.2f} g")
            st.metric("🥑 Fats", f"{fats:.2f} g")

    else:
        st.error("No foods found.")import streamlit as st
import requests

st.set_page_config(page_title="AI Nutrition Tracker", layout="centered")

# ---------------- UI ---------------- #
st.title("🥗 AI Nutrition Tracker")
st.write("Search foods from USDA database with accurate nutrition facts.")

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
    data = response.json()

    if "foods" in data:
        return data["foods"]

    return []

# ---------------- USER INPUT ---------------- #
food_query = st.text_input("🍗 Search Food")

grams = st.number_input("⚖️ Enter grams", min_value=1, value=100)

# ---------------- SEARCH RESULTS ---------------- #
if food_query:

    foods = search_food(food_query)

    if foods:

        # create dropdown options
        food_options = {}

        for food in foods:

            description = food.get("description", "Unknown Food")

            brand = food.get("brandOwner", "")

            label = f"{description} ({brand})" if brand else description

            food_options[label] = food

        selected_label = st.selectbox(
            "Select exact food item",
            list(food_options.keys())
        )

        selected_food = food_options[selected_label]

        # ---------------- BUTTON ---------------- #
        if st.button("Get Accurate Nutrition"):

            nutrients = selected_food.get("foodNutrients", [])

            protein = carbs = fats = calories = 0

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

                # Fats
                elif name == "Total lipid (fat)":
                    fats = adjusted_value

                # Calories
                elif name == "Energy":
                    calories = adjusted_value

            # ---------------- RESULTS ---------------- #
            st.markdown("---")

            st.subheader(f"Nutrition Facts for {grams}g")

            st.success(selected_label)

            st.metric("🔥 Calories", f"{calories:.2f} kcal")
            st.metric("💪 Protein", f"{protein:.2f} g")
            st.metric("🍞 Carbs", f"{carbs:.2f} g")
            st.metric("🥑 Fats", f"{fats:.2f} g")

    else:
        st.error("No foods found.")
