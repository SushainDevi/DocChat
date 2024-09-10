"""
import streamlit as st
import time
from Text_Extraction import extract_text
from gradio_client import Client
import os
from database import save_chat_to_db

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "Qwen1.5-110B-Chat"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "extracted_contents" not in st.session_state:
    st.session_state.extracted_contents = []

# Flag to track if the animation has been displayed
if "animation_displayed" not in st.session_state:
    st.session_state.animation_displayed = False

# Flag to track if a file is uploaded
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

@st.cache_resource
def create_client():
    hf_token = os.getenv("HF_Token")
    print(f'Loading the API gradio client for {st.session_state.hf_model}')
    client = Client("Qwen/Qwen1.5-110B-Chat-demo", hf_token=hf_token)
    return client

# AVATARS
av_us = '👤'
av_ass = "🤖"

### START STREAMLIT UI
st.image('https://www.chatbot.com/chatbot-ai-assist.d97fd6781d5adc0555046148733f2c09fb0a2114251276fcb575cef5765b25c2.png')
st.markdown("## DocChat", unsafe_allow_html=True)
st.markdown('---')

client = create_client()

# File uploader for users to upload multiple files
uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf", "docx", "csv", "jpg", "jpeg", "png"], accept_multiple_files=True)

# Process the uploaded files
if uploaded_files:
    file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    st.session_state.extracted_contents = []
    st.session_state.file_uploaded = True  # Set the flag to True
    
    for uploaded_file in uploaded_files:
        # Extract text from each file
        file_content = extract_text(uploaded_file)
        st.session_state.extracted_contents.append(file_content)
    
    # Combine the extracted content from all files
    combined_content = "\n\n".join(st.session_state.extracted_contents)

    # Typewriter animation for successful extraction (only run once)
    if not st.session_state.animation_displayed:
        def typewriter_animation(text):
            message_placeholder = st.empty()  # Create a placeholder for the message
            for i in range(len(text) + 1):
                message_placeholder.markdown(f"<div style='font-size:16px'>{text[:i]}</div>", unsafe_allow_html=True)
                time.sleep(0.05)  # Adjust speed of animation here
            st.markdown("---")  # Add a separator after the animation
            st.session_state.animation_displayed = True  # Set the flag to True

        typewriter_animation("TEXT EXTRACTED SUCCESSFULLY")

# Display chat history
if st.session_state.messages:
    st.markdown("## Chat History")
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=av_us):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=av_ass):
                st.markdown(message["content"])
    st.markdown("---")

# Accept user input
if myprompt := st.chat_input("Hi, I am DocChat. How can I assist you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)

    # Construct the prompt for the assistant
    if st.session_state.file_uploaded:
        # Document-focused prompt if files are uploaded
        context_prompt = (
            "You are a helpful assistant. "
            "For all user responses, make sure to provide answers in the context of the extracted text from the uploaded document(s). "
            "If necessary, generate responses based on general knowledge, but always relate it to the content provided."
        )
        # Combine the context prompt with the user's input and the extracted content
        combined_content = "\n\n".join(st.session_state.extracted_contents)
        full_prompt = f"{context_prompt}\n\nExtracted Content:\n{combined_content}\n\nUser: {myprompt}"
    else:
        # General prompt if no files are uploaded
        context_prompt = (
            "You are a helpful assistant. "
            "You can provide general knowledge responses to user queries, "
            "but always ensure the responses are helpful and accurate."
        )
        full_prompt = f"{context_prompt}\n\nUser: {myprompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        res = client.submit(
            query=full_prompt,
            history=[],
            system="You are a helpful assistant.",
            api_name="/model_chat"
        )
        
        for r in res:
            full_response = r[1][0][1]
            message_placeholder.markdown(r[1][0][1] + "▌")

        message_placeholder.markdown(full_response)      
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Save chat history to the database with all file names (if files were uploaded)
    if st.session_state.file_uploaded:
        save_chat_to_db(", ".join(file_names), st.session_state.messages)
    else:
        save_chat_to_db("No Files", st.session_state.messages)

"""
###################################################################################################################################################


import streamlit as st
import time
import os
from Text_Extraction import extract_text
from gradio_client import Client
from database import save_chat_to_db
from generate_file import generate_file  # Import the generate_file functions

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "Qwen1.5-110B-Chat"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "extracted_contents" not in st.session_state:
    st.session_state.extracted_contents = []

# Flag to track if the animation has been displayed
if "animation_displayed" not in st.session_state:
    st.session_state.animation_displayed = False

# Flag to track if a file is uploaded
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

@st.cache_resource
def create_client():
    hf_token = os.getenv("HF_Token")
    print(f'Loading the API gradio client for {st.session_state.hf_model}')
    client = Client("Qwen/Qwen1.5-110B-Chat-demo", hf_token=hf_token)
    return client

# AVATARS
av_us = '👤'
av_ass = "🤖"

### START STREAMLIT UI
st.image('https://www.chatbot.com/chatbot-ai-assist.d97fd6781d5adc0555046148733f2c09fb0a2114251276fcb575cef5765b25c2.png')
st.markdown("## DocChat", unsafe_allow_html=True)
st.markdown('---')

client = create_client()

# File uploader for users to upload multiple files
uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf", "docx", "csv", "jpg", "jpeg", "png"], accept_multiple_files=True)

# Process the uploaded files
if uploaded_files:
    file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    st.session_state.extracted_contents = []
    st.session_state.file_uploaded = True  # Set the flag to True
    
    for uploaded_file in uploaded_files:
        # Extract text from each file
        file_content = extract_text(uploaded_file)
        st.session_state.extracted_contents.append(file_content)
    
    # Combine the extracted content from all files
    combined_content = "\n\n".join(st.session_state.extracted_contents)

    # Typewriter animation for successful extraction (only run once)
    if not st.session_state.animation_displayed:
        def typewriter_animation(text):
            message_placeholder = st.empty()  # Create a placeholder for the message
            for i in range(len(text) + 1):
                message_placeholder.markdown(f"<div style='font-size:16px'>{text[:i]}</div>", unsafe_allow_html=True)
                time.sleep(0.05)  # Adjust speed of animation here
            st.markdown("---")  # Add a separator after the animation
            st.session_state.animation_displayed = True  # Set the flag to True

        typewriter_animation("TEXT EXTRACTED SUCCESSFULLY")

# Display chat history
if st.session_state.messages:
    st.markdown("## Chat History")
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=av_us):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=av_ass):
                st.markdown(message["content"])
    st.markdown("---")

# Accept user input
if myprompt := st.chat_input("Hi, I am DocChat. How can I assist you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)

    # Construct the prompt for the assistant
    context_prompt = (
        "You are a helpful assistant. "
        "For all user responses, make sure to provide answers in the context of the extracted text from the uploaded document(s). "
    )

    if st.session_state.file_uploaded:
        # Combine the context prompt with the user's input and the extracted content
        combined_content = "\n\n".join(st.session_state.extracted_contents)
        full_prompt = f"{context_prompt}\n\nExtracted Content:\n{combined_content}\n\nUser: {myprompt}"
    else:
        # General prompt if no files are uploaded
        full_prompt = f"{context_prompt}\n\nUser: {myprompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        res = client.submit(
            query=full_prompt,
            history=[],
            system="You are a helpful assistant.",
            api_name="/model_chat"
        )
        
        for r in res:
            full_response = r[1][0][1]
            message_placeholder.markdown(r[1][0][1] + "▌")

        message_placeholder.markdown(full_response)      
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Check for file format requests
    file_format = None  # Initialize file_format to None
    file_name = "output.pdf"  # Default file name

    if "pdf" in myprompt.lower():
        file_format = "pdf"
        file_name = "output.pdf"
    elif "doc" in myprompt.lower() or "docx" in myprompt.lower():
        file_format = "docx"
        file_name = "output.docx"

    # Only generate a file if the user explicitly requests it
    if file_format:
        def generate_file_from_response():
            content_to_generate = ""

            # Use the second-to-last generated model response for file generation
            if len(st.session_state.messages) >= 4 and st.session_state.messages[-2]["role"] == "assistant":
                content_to_generate = st.session_state.messages[-2]["content"]
            else:
                content_to_generate = st.session_state.extracted_contents[0]  # Fallback to first extracted content

            # Generate the file
            generated_file = generate_file(content_to_generate, file_format, file_name)
            with open(file_name, "rb") as f:
                st.download_button(label=f"Download {file_format.upper()} file", data=f, file_name=file_name, mime="application/octet-stream")
        # Call the function to generate the file
        generate_file_from_response()

    # Save chat history to the database with all file names (if files were uploaded)
    if st.session_state.file_uploaded:
        save_chat_to_db(", ".join(file_names), st.session_state.messages)
    else:
        save_chat_to_db("No Files", st.session_state.messages)