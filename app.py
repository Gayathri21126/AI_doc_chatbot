import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI

# Load environment variables
load_dotenv()

# Page config (must be first Streamlit command)
st.set_page_config(page_title="AI Document Chatbot", layout="centered")

# Initialize OpenAI client
client = OpenAI()

# UI Header
st.title("📄 AI Document Chatbot")
st.markdown("Upload a PDF and ask questions about its content.")

# Demo warning (OPTION 3)
st.warning("⚠️ Demo mode: AI responses may be limited due to API quota.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Function to extract text from PDF
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# Process uploaded file
if uploaded_file:
    text = extract_text(uploaded_file)

    if text.strip() == "":
        st.error("⚠️ Could not extract text from this PDF.")
    else:
        st.success("✅ Document uploaded successfully!")

        # User input
        user_question = st.text_input("Ask a question about the document:")

        if user_question:
            with st.spinner("🤖 Thinking..."):

                prompt = f"""
                Answer the question based only on the document below.

                Document:
                {text[:3000]}

                Question:
                {user_question}
                """

                try:
                    # Try OpenAI API
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    answer = response.choices[0].message.content

                except Exception as e:
                    # Fallback (OPTION 2)
                    answer = "⚠️ AI response unavailable (API quota exceeded).\n\n"

                    if user_question.lower() in text.lower():
                        answer += "📌 A related section was found in the document."
                    else:
                        answer += "❌ No direct match found. Try rephrasing your question."

                # Display answer
                st.markdown("### 📢 Answer")
                st.success(answer)
