from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Function to get the API key from the user
def get_api_key():
    st.title("Multi Language Extractor")
    st.markdown(
        """
        **Instructions:**

        1. Enter your Google API Key below.
        2. Provide an input prompt and upload an image.
        3. Click the "Tell me about the invoice" button to generate a response.
        """
    )

    api_key = st.text_input("Enter your Google API Key:", type="password")
    return api_key

# Function to configure Google API and Gemini Pro Vision
def configure_google_api(api_key):
    os.environ["GOOGLE_API_KEY"] = api_key
    import google.generativeai as genai
    genai.configure(api_key=api_key)

# Function to load Gemini Pro Vision API key
def initialize_gemini_pro_vision():
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

# Function to handle the main content
def main_content(model):
    # Input components
    input_text = st.text_input("Input prompt:", key="input")
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

    # Display the uploaded image
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Submit button
    submit = st.button("Tell me about the invoice")

    # If submit button is clicked
    if submit:
        try:
            if uploaded_file is not None:
                image_data = input_image_details(uploaded_file)
                response = get_gemini_pro_response(input_text, image_data, input_text)
                st.subheader("The Response is")
                st.write(response)
            else:
                st.warning("Please upload an image.")
        except FileNotFoundError as e:
            st.error(str(e))

# Function to handle the input image details
def input_image_details(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return image_parts

# Function to get Gemini Pro Vision response
def get_gemini_pro_response(prompt, image_data, input_text):
    response = model.generate_content([prompt, image_data[0], input_text])
    return response.text

# Run the app
if __name__ == "__main__":
    api_key = get_api_key()

    if not api_key:
        st.warning("Please enter your Google API Key.")
    else:
        configure_google_api(api_key)
        model = initialize_gemini_pro_vision()
        main_content(model)
