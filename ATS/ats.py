import os
import io
import base64
import pdf2image
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Get response from Gemini API
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Fetching details about pdf
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Specify the path to the Poppler binary
        poppler_path = r'C:\Users\Harshit\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin'
        
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Streamlit UI
st.set_page_config(page_title = "ATS")
st.header("Application Tracking System")
input_text = st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Upload Your Resume(PDF)...", type = ["pdf"])

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit1 = st.button('Feedback on Resume')

submit2 = st.button('Percentage Match')

input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then in new line the keywords missing in resume and lastly final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")