import streamlit as st
from utils.common import s3_upload, ask_model

def captureData():
        # unique key generation for widgets
        widget_id = (id for id in range(1, 100_00))

        # upload pictures
        st.write("Food picture(s)")
        st.write("Press upload button once the pictures are added.")
        documentImage = st.file_uploader("image(s): ", key=next(widget_id))


           # Layout with columns
        left_column, right_column = st.columns([2, 2])  # Adjust the width ratio of columns
        with left_column:
            if documentImage: 
                bytes_data = documentImage.getvalue()
                st.image(documentImage)
        with right_column:
            if documentImage is not None:
                documentImageUploaded = st.button("Upload & extract data", key=next(widget_id))
                if documentImageUploaded:
                    response = s3_upload(documentImage)
                    st.write(response)
                    source_img =  documentImage.name
                    input_query = '''You are an food image analyzer. Give me ontology about this picture in this format : Food Name, Ingredients, Popular in Countries,Popular in Events, Popular in Weather, Food temprature, Allergens, Dietary Preferences/Restrictions, Calories,Funfact/Inspiring Quote'.
                    Example : 'Pad Thai',	'Rice noodles, shrimp, tofu, eggs, bean sprouts, peanuts, tamarind sauce',	'Thailand',	'Any event', 'winter,fall','Hot','Peanuts, shellfish, eggs',	'Pescatarian, Gluten-free (with rice noodles)'.	'300-400 kcal'" .
                    Response should have only 2 format. A color coded table for human read and A color coded json format '''
                    st.write(ask_model(source_img, input_query))
                
                

        
