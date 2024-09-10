import re
from spellchecker import SpellChecker
import sys
import time
from gradio_client import Client
from streamlit_chat import message
import streamlit as st
import time
from Text_Extraction import extract_text
import os

# Set the page configuration with a new icon
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",  # You can replace this with a URL to a new icon if desired
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a Streamlit app built with ❤️"
    }
)

# Add a sidebar with some information
with st.sidebar:
    st.title("🤖 Chatbot Interface")
    st.markdown(
        """
        This is a chatbot interface built using Streamlit.
        You can interact with the chatbot and get responses.
        """
    )
    st.title("Help")
    st.markdown("### How to Use")
    st.markdown("1. Type your message in the input box.\n2. Upload documents if needed.\n3. Click 'Send' to get a response.")

# Define a function to generate chatbot responses
def generate_response(user_input):
    # Your logic to generate responses, e.g., calling an API or a model
    response = "This is a placeholder response."  # Replace with actual response generation logic
    return response

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# Define a function to handle user input and update the chat history
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append({"message": user_input, "is_user": True})
        with st.spinner("Generating response..."):
            response = generate_response(user_input)
        st.session_state.history.append({"message": response, "is_user": False})
        st.session_state.user_input = ""

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    st.title("Chatbot Interface")
    st.markdown("Welcome to the chatbot! Type your message below and get a response.")
    st.text_input("You:", key="user_input", on_change=handle_input)
    if st.button("Clear Chat"):
        st.session_state.history = []

with col2:
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        # Process the uploaded file
        if uploaded_file.type == "application/pdf":
            from PyPDF2 import PdfFileReader
            import io
            pdf_reader = PdfFileReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extract_text()
            st.session_state.document_text = text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            import docx
            doc = docx.Document(uploaded_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            st.session_state.document_text = text
        elif uploaded_file.type == "text/plain":
            text = str(uploaded_file.read(), "utf-8")
            st.session_state.document_text = text

        st.markdown("### Uploaded Document Content")
        st.text_area("Document Text", st.session_state.document_text, height=200)

# Display chat history with alternating colors for user and chatbot messages
for chat in st.session_state.history:
    if chat["is_user"]:
        message(chat["message"], is_user=True)
    else:
        message(chat["message"], is_user=False)

# Add some custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: white;
        color: #007BFF;
        border: 2px solid #007BFF;
    }
    .stTextInput input {
        padding: 10px;
        font-size: 16px;
        border: 2px solid #007BFF;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add some animation using Streamlit components
st.markdown(
    """
    <div style="text-align: center;">
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_kpyi8jti.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop  autoplay></lottie-player>
    </div>
    """,
    unsafe_allow_html=True,
)
