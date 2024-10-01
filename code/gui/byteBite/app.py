import streamlit as st
from streamlit_option_menu import option_menu
from options.capture import captureData
from options.menu import menu
from options.data import showData
from streamlit import set_page_config
set_page_config(layout="wide")

# Add custom CSS for styling
st.markdown("""
   <style>
   .icon { color: orange !important; font-size: 25px !important; }
   .nav-link { font-size: 25px !important; text-align: left !important; margin: 0px !important; }
   .nav-link:hover { background-color: #eee !important; }
   .nav-link-selected { background-color: blue !important; }
   </style>
""", unsafe_allow_html=True)

# Create the horizontal menu
selected = option_menu(
   menu_title=None,  # Hide the title if not needed
   options=["Capture Metadata","Food Metadata", "Personalized menu"],
   icons=["camera","database", "patch-check-fill"],
   menu_icon="cast",
   default_index=0,
   orientation="horizontal"
)
# Navigate to the selected page
if selected == "Capture Metadata":
   captureData()
elif selected == "Food Metadata":
   showData()
elif selected == "Personalized menu":
   menu()