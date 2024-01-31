from dotenv import load_dotenv

load_dotenv()  #load all the environments variable from .env files

import streamlit as st
import os 
from PIL import Image

import  google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



## Function to load gemini pro vision api key

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_pro_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()        
        image_parts= [
            {
            
        "mime_type" : uploaded_file.type,
         "data" : bytes_data   
            } 
         ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploded")
            
        



## initalize the steamlit setup

st.set_page_config(page_title="Multi Language Extractor")
st.header("Multi Language Extractor")
input = st.text_input("Input prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image..." ,type=["jpg","jpeg","png"])

image = ""

if uploaded_file  is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image." , use_column_width=True)


submit = st.button("Tell me about the invoice")   


input_prompt="""
  You are an expert and understanding invoices.We will upload a image as invoices and you will have to answer any questions based on the upload invoice message

""" 


## if submit button is clicked 
if submit:
    image_data=input_image_details(uploaded_file)
    response = get_gemini_pro_response(input_prompt,image_data,input)
    st.subheader("The Reponse is")
    st.write(response)