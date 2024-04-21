#1. Field to enter the Job Description
#2. Upload PDF
#3. PDF to Image --> Processing --> Google Gemini Pro
#4. Multiple Prompts (templates)


from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64 # type: ignore
import io # type: ignore
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Prompt will play a major role in the project
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        # Converting the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to Bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format = "JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type" : "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode() # encode to base64
        }]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit Application
    
st.set_page_config(page_title="ATS Resume Scanner")
st.header("Application Tracking System")

targeted_roles = st.text_input("Targeted Roles (sep by comma): ", key="role")

skill_set = st.text_input("Enter your skills separated by comma", key="skills")

job_description = st.text_area("Job Description: ", key = "input")

uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type = ["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded Successfully :)")


action1 = st.button("Summary of the Resume")
action2 = st.button("How can the resume be improved?")
action3 = st.button("Percentage Match with the job description %")

input_prompt1 = f"""
                    You are an experienced HR with technical experience
                    in the field of {targeted_roles}. The user is experienced in the following skills: {skill_set}.
                    Your task is to review the provided resume against the
                    job description for the roles mentioned.  
                    Please share your professional evaluation on whether the
                    candidate's profile aligns with the job description.
                    Highlight the strengths and weaknesses of the applicant in
                    relation to the specified job description.
                
                """


input_prompt2 = f"""
                    You are a technical HR manager with expertise in {targeted_roles}. The user is experienced in the following skills: {skill_set}.
                    Your role is to scrutinize the resume in light of the job description and skills provided.
                    Share your insights on the candidate's suitability for the role from a HR perspective. Additionally, offer practical advice on enhancing the candidate's skills
                    and identify areas where the candidate can be improved.
                """

input_prompt3 = f"""
                    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of {targeted_roles} and ATS functionality. 
                    Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
                    the job description for each of the {targeted_roles}. 
                    First the output should come as percentage and then keywords missing in new line and last final thoughts at the bottom.
                """


if action1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, job_description)
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume")

if action2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt2)
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume")

if action3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt3)
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume")