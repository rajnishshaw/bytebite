import streamlit as st
import pandas as pd
import numpy as np
import boto3
import requests


# Functions
# s3 upload function
def s3_upload(file, bucket, prefix):
    prefix_path = prefix + file.name
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(
            file,
            bucket,
            prefix_path
            )
        return prefix_path
    except:
        return None

# ask genAI model
def ask_model(source_img, input_query):
    api_gw_url = '<<API-URL>>'
    url = api_gw_url
    params = {'source_img': source_img, 'input_query': input_query}
    response = requests.get(url, params)
    return st.write(f"Assistant: {response.json()}")

def captureData():
        s3_bucket = '<<S3_BUCKET_NAME>>'
        s3_prefix = 'images/'
        
        # unique key generation for widgets
        widget_id = (id for id in range(1, 100_00))

        # upload pictures
        st.write("Food picture(s)")
        st.write("Press upload button once the pictures are added.")
        documentImage = st.file_uploader("image(s): ", key=next(widget_id))

        if documentImage: 
            bytes_data = documentImage.getvalue()
            st.image(documentImage)
    
        documentImageUploaded = st.button("upload", key=next(widget_id))
        if documentImage is not None:
            if documentImageUploaded:
                response = s3_upload(documentImage, s3_bucket, s3_prefix)
                st.write(response)
        # Define the options for the radio buttons
        options = ["None","Initial assessment","Interactive mode"]

        # Create a radio button for each option
        selected_option = st.radio("Select an option", options)
       
        # Handle the selected option
        if selected_option == "Initial assessment":
            # Initial assessment
            st.subheader("Initial assessment")
            st.write("Analyzing ...")
            source_img = s3_prefix + documentImage.name
            input_query = '''You are an food image analyzer. Give me ontology about this picture in this format : Food Name, Ingredients, Popular in Countries,Popular in Events, Popular in Weather, Food temprature, Allergens, Dietary Preferences/Restrictions, Calories,Funfact/Inspiring Quote'.
            Example : 'Pad Thai',	'Rice noodles, shrimp, tofu, eggs, bean sprouts, peanuts, tamarind sauce',	'Thailand',	'Any event', 'winter,fall','Hot','Peanuts, shellfish, eggs',	'Pescatarian, Gluten-free (with rice noodles)'.	'300-400 kcal'" .
            Response should have only 2 format. A table for human read and A color coded json format '''
            ask_model(source_img, input_query)
    
        elif selected_option == "Interactive mode":
            # Interactive mode
            st.subheader("Interactive mode")
            st.write("Use the chat option to interact with AI assistant")
            prompt = st.text_area("What's up?", key="chat_input", height=100)
            if prompt:
                st.write("Agent:", prompt)
                source_img = s3_prefix + documentImage.name
                input_query = prompt
                response = ask_model(source_img, input_query)
        else:
            # please select an option
            st.write("Select one of the above options")

      