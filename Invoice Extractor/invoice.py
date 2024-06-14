# Importing libraries

import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables

load_dotenv()

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# Load model & get response

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

# Fetching the details of an Image

def input_image_details(uploaded_file):
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
    
# Streamlit UI

st.set_page_config(page_title = "MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input = st.text_input("Input Prompt: ",key = "input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type = ["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image.", use_column_width = True)

submit = st.button("Submit")

input_prompt = """
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Rresponse is")
    st.write(response)