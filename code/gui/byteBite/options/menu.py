import streamlit as st
from utils.common import ask_model
import csv


def extract_text_from_text(file_path):
    extracted_text = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                extracted_text.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    return extracted_text

def menu():
   # Define options for dropdowns
   event_types = ['Corporate Event', 'Wedding', 'Birthday', 'Anniversary', 'Other']
   cuisines = ['Italian', 'Chinese', 'Indian', 'Mexican', 'American', 'Other']
   meal_types = ['Buffet', 'Sit-down', 'Family Style', 'Cocktail Style']
   menu_styles = ['Traditional', 'Modern', 'Fusion']
   dietary_restrictions = ['None', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Nut-Free', 'Halal', 'Kosher', 'Other']
   alcoholic_beverages = ['Yes', 'No']
   non_alcoholic_beverages = ['Yes', 'No']

   # Layout with columns
   left_column, right_column = st.columns([2, 2])  # Adjust the width ratio of columns

   with left_column:
       st.write("Please fill in the details for your event below:")
       
       with st.expander("Menu Preferences", expanded=True):
           preferred_cuisine = st.selectbox("Preferred Cuisine", cuisines)

           meal_type = st.selectbox("Meal Type", meal_types)
           menu_style = st.selectbox("Menu Style", menu_styles)
           dietary_restriction = st.multiselect("Dietary Restrictions", dietary_restrictions)
           special_requests = st.text_area("Special Requests")

           total_budget = st.number_input("Total Budget", min_value=50.0, step=100.0)
      
       with st.expander("Event Details", expanded=True):
           event_name = st.text_input("Event Name",value="Onboarding")
           event_date = st.date_input("Event Date")
           number_of_guests = st.number_input("Number of Guests", min_value=5, step=1)
           event_type = st.selectbox("Type of Event", event_types)

   with right_column:
       if st.button("Personalized menu"):
           extract_text = extract_text_from_text('food_data.csv')
           st.write((f"You are a skilled food event organizer, attentive to both budget and taste. Your task is to craft personalized menu recommendations based on the following context:"
                    f" Event Type: **{event_type}**"
                    f" Date: **{event_date}**"
                    f" Guests: **{number_of_guests}**"
                    f" Cuisine Preference: **{meal_type}**"
                    f" Serving Style: {menu_style}"
                    f" Dietary Restrictions: **{', '.join(dietary_restriction) if dietary_restriction else 'no'}**"
                    f" Special Requests: **{special_requests if special_requests else 'no special requests'}**"
                    f" Total : **${total_budget}**"
                    f" Using the provided menu data, generate a menu recommendation in table format with the following columns: Dish Type, Item Name, Cost, Justification. Ensure your selections align with the event's theme and budget."))
                            
           st.write(ask_model(None,(f"You are a skilled food event organizer, attentive to both budget and taste. Your task is to craft personalized menu recommendations based on the following context:"
                    f" Event Type: **{event_type}**"
                    f" Date: **{event_date}**"
                    f" Guests: **{number_of_guests}**"
                    f" Cuisine Preference: **{meal_type}**"
                    f" Serving Style: {menu_style}"
                    f" Dietary Restrictions: **{', '.join(dietary_restriction) if dietary_restriction else 'no'}**"
                    f" Special Requests: **{special_requests if special_requests else 'no special requests'}**"
                    f" Total Budget: **${total_budget}**"
                    f" Using the provided menu data, generate a menu recommendation in table format with the following columns: Dish Type, Item Name, Cost, Justification. Ensure your selections align with the event's theme and budget. Menu Data:\n\n {extract_text}")))

           


