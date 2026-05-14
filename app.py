import streamlit as st
import requests

st.set_page_config(page_title="AI Nutrition Tracker", layout="centered")

# ---------------- UI ---------------- #
st.title("🥗 AI Nutrition Tracker")

st.write("Enter a food item and grams to get nutrition facts.")

# ---------------- INPUTS ---------------- #
food_name = st.text_input("🍗 Food Name")

grams = st.number_input("⚖️ Grams", min_value=1, value=100)

# ---------------- USDA API ---------------- #
API_KEY = "P73wIVJPiCNTOFtegbe97NOAyX8cCif4fDzCwk07"

def get_food_data(food):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food,
        "pageSize": 1
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "foods" in data and len(data["foods"]) > 0:
        return data["foods"][0]

    return None

# ---------------- BUTTON ---------------- #
if st.button("Get Nutrition Facts"):

    food_data = get_food_data(food_name)

    if food_data:

        nutrients = food_data.get("foodNutrients", [])

        protein = carbs = fats = calories = 0

        for nutrient in nutrients:

            name = nutrient.get("nutrientName", "")

            value = nutrient.get("value", 0)

            # per 100g adjustment
            adjusted = (value * grams) / 100

            if name == "Protein":
                protein = adjusted

            elif name == "Carbohydrate, by difference":
                carbs = adjusted

            elif name == "Total lipid (fat)":
                fats = adjusted

            elif name == "Energy":
                calories = adjusted

        # ---------------- RESULTS ---------------- #
        st.markdown("---")

        st.subheader(f"Nutrition Facts for {grams}g of {food_name}")

        st.metric("🔥 Calories", f"{calories:.2f} kcal")
        st.metric("💪 Protein", f"{protein:.2f} g")
        st.metric("🍞 Carbs", f"{carbs:.2f} g")
        st.metric("🥑 Fats", f"{fats:.2f} g")

    else:
        st.error("Food not found.")
