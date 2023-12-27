# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Dental Advisor")

st.header("Gemini Dental Advisor")
option = st.selectbox(
    'Choose radiograph type',
    ('Bitewing', 'Periapical', 'Panoramic X-rays'))
input=st.text_input("Any additional info that you want to share",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png","tiff","dicom"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the " + option+" radiograph")

input_prompt = """
               You are a dental expert in understanding Dental Radiology for Disease Identification.
               You will receive input images as bitewings and periapical radiographs &
               you will have to identify dental diseases and build a report.
               you have automatically detect and report on occlusal and interproximal caries, measure bone loss in bitewings, 
               and identify periapical pathology in periapical radiographs while also determining the teeth present.
               Scope:
1.	Bitewing Radiographs:
•	Disease Identification: Detect occlusal and interproximal caries.
•	Bone Loss Measurement: Quantify bone loss levels, crucial for periodontal disease assessment.
•	Teeth present: Identify the teeth which are present or absent in the radiograph.
2.	Periapical Radiographs:
•	Disease Identification: Detect occlusal and interproximal caries, and periapical pathology.
•	Bone Loss Measurement: As in bitewing radiographs.
Teeth present: Identify the teeth which are present or absent in the radiograph.
•	Automatically identify individual teeth in the radiographs.
•	Detect the presence and extent of dental diseases (caries, bone loss, periapical pathology) using ML algorithms.
Radiology Report Generation:
•	Generate a detailed radiology report based on the analysis.
•	Include information about identified diseases, affected teeth, and severity levels.

Note: please don't provide the name, age, sex, date or any personal information of patients.
               """

## If ask button is clicked
final_input="Radiosgraph type is "+option+ "Additional info: "+input

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,final_input)
    st.subheader("The Response is")
    st.write(response)
