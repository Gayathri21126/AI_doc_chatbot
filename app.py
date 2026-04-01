import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set page config FIRST
st.set_page_config(page_title="AI Document Chatbot", layout="centered")

# Initialize OpenAI client
client = OpenAI()

# UI
st.title("📄 AI Document Chatbot")
st.write("Upload a PDF and ask questions about its content.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Function to extract text
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Process file
if uploaded_file:
    text = extract_text(uploaded_file)
    st.success("Document uploaded successfully!")

    user_question = st.text_input("Ask a question about the document:")

    if user_question:
        with st.spinner("Thinking..."):

            prompt = f"""
            Answer the question based on the document below.

            Document:
            {text[:3000]}

            Question:
            {user_question}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content

            st.write("### Answer:")
            st.success(answer)
