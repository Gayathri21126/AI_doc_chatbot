import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": user_question}
    ]
)

answer = response.choices[0].message.content
st.set_page_config(page_title="AI Document Chatbot", layout="centered")

st.write("Upload a PDF and ask questions about its content.")
load_dotenv(dotenv_path=".env")
qa_pipeline = pipeline("question-answering")

st.title("📄 AI Document Chatbot")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if uploaded_file:
    text = extract_text(uploaded_file)
    st.success("Document uploaded successfully!")

    question = st.text_input("Ask a question about the document:")

    if question:
       with st.spinner("Thinking..."):
        result = qa_pipeline(
            question=question,
            context=text[:2000]
        )
        answer = result['answer']

    st.write("### Answer:")
    st.success(answer)
