import streamlit as st
import pandas as pd

def showData():
   # Read the CSV file
   df = pd.read_csv('food_data.csv')

   # Streamlit app
   st.title("My Food Data Table")

   # Display the DataFrame in a nice table format
   st.dataframe(df)