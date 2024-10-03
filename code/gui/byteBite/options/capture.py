import streamlit as st
from utils.common import s3_upload, ask_model

# Functions


def captureData():
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
                response = s3_upload(documentImage)
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
            source_img =  documentImage.name
            input_query = '''You are an food image analyzer. Give me ontology about this picture in this format : Food Name, Ingredients, Popular in Countries,Popular in Events, Popular in Weather, Food temprature, Allergens, Dietary Preferences/Restrictions, Calories,Funfact/Inspiring Quote'.
            Example : 'Pad Thai',	'Rice noodles, shrimp, tofu, eggs, bean sprouts, peanuts, tamarind sauce',	'Thailand',	'Any event', 'winter,fall','Hot','Peanuts, shellfish, eggs',	'Pescatarian, Gluten-free (with rice noodles)'.	'300-400 kcal'" .
            Response should have only 2 format. A table for human read and A color coded json format '''
            st.write(ask_model(source_img, input_query))
    
        elif selected_option == "Interactive mode":
            # Interactive mode
            st.subheader("Interactive mode")
            st.write("Use the chat option to interact with AI assistant")
            prompt = st.text_area("What's up?", key="chat_input", height=100)
            if prompt:
                st.write("Agent:", prompt)
                source_img = documentImage.name
                input_query = prompt
                st.write(ask_model(source_img, input_query))
        else:
            # please select an option
            st.write("Select one of the above options")

      