import os
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import seaborn as sns
import PyPDF2
import together
import speech_recognition as sr
import time
import streamlit as st

# Set Together API Key
together.api_key = "a0d24deea53c9fa31fdc6b3a8e2de768e80fe0a036e7a4aa88c33b289b1b21bd"

# Streamlit app title
st.title("🦾 Data Analyst Agent")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "txt", "pdf", "png", "jpg", "jpeg"])

# Handle uploaded file
if uploaded_file is not None:
    file_name = uploaded_file.name
    st.success(f"File '{file_name}' uploaded successfully!")

    file_ext = file_name.split(".")[-1].lower()

    if file_ext == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

    elif file_ext == "xlsx":
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)

    elif file_ext == "txt":
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Text Content", text, height=300)

    elif file_ext == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        st.text_area("Extracted PDF Text", text, height=300)

    elif file_ext in ["png", "jpg", "jpeg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        try:
            extracted_text = pytesseract.image_to_string(image)
            st.text_area("Extracted Text from Image", extracted_text, height=300)
        except pytesseract.TesseractNotFoundError:
            st.error("Tesseract OCR not installed or not found in PATH. Please install it.")

# Text input for questions
st.subheader("📣 Ask your question to the agent")
user_input = st.text_input("Type your question and hit Enter:")

# Query Together API and display response
if user_input:
    with st.spinner("Thinking..."):
        response = together.Complete.create(
            prompt=user_input,
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            max_tokens=500,
            temperature=0.7,
        )
        st.write(response['choices'][0]['text'])

# Optional: Text-to-speech input
st.subheader("🎙️ Speak your question (optional)")
if st.button("Record Audio"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.success(f"You said: {query}")

        response = together.Complete.create(
            prompt=query,
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            max_tokens=500,
            temperature=0.7,
        )
        st.write(response['choices'][0]['text'])

    except sr.UnknownValueError:
        st.error("Could not understand audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
