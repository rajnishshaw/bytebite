import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np
from utils.common import ask_model

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
           st.write((f"You are a helpful food event organizer and mindful about the budget and taste. Your task is to generate personalized recipe ideas based on the context : I want to order food for **{event_name}** on **{event_date}** for **{number_of_guests}** guests. "
                   f"This event is a **{event_type}**, and I would like to serve **{preferred_cuisine}** cuisine with **{meal_type}** style, "
                   f"preferably in **{menu_style}**. There are **{', '.join(dietary_restriction) if dietary_restriction else 'no'}** dietary restrictions to consider, "
                   f"and I’d like to include **{special_requests if special_requests else 'no special requests'}**. My budget for this event is **${total_budget}**. Give me menu recomendation and justify your selection for each item !. The response should be in table format with columns : Dish type, Item Name, Cost, Justification."))

           st.write(ask_model(None,f"You are a helpful food event organizer and mindful about the budget and taste. Your task is to generate personalized recipe ideas based on the context : I want to order food for **{event_name}** on **{event_date}** for **{number_of_guests}** guests. "
                   f"This event is a **{event_type}**, and I would like to serve **{preferred_cuisine}** cuisine with **{meal_type}** style, "
                   f"preferably in **{menu_style}**. There are **{', '.join(dietary_restriction) if dietary_restriction else 'no'}** dietary restrictions to consider, "
                   f"and I’d like to include **{special_requests if special_requests else 'no special requests'}**. My budget for this event is **${total_budget}**. Give me menu recomendation and justify your selection for each item !. The response should be in table format with columns : Dish type, Item Name, Cost, Justification."))

           
