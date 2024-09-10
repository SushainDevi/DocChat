import streamlit as st
from gradio_client import Client

# Set the page configuration
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Define a function to create the Gradio client
@st.cache_resource
def create_client():
    yourHFtoken = "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"
    client = Client("Qwen/Qwen1.5-110B-Chat-demo", hf_token=yourHFtoken)
    return client

# Define a function to generate chatbot responses
def generate_response(user_input):
    client = create_client()
    # Prepare chat history in the required format
    history = [(msg["message"], "user" if msg["is_user"] else "assistant") for msg in st.session_state.history]
    try:
        result = client.submit(
            query=user_input,
            history=history,
            system="You are a helpful assistant.",
            api_name="/model_chat"
        )
        response = "".join([chunk[1][0][1] for chunk in result])
    except Exception as e:
        response = f"Error: {e}"
    return response

# Define a function to handle user input and update the chat history
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append({"message": user_input, "is_user": True})
        response = generate_response(user_input)
        st.session_state.history.append({"message": response, "is_user": False})
        st.session_state.user_input = ""

# Layout for chat input and history
st.title("Chatbot Interface")
st.markdown("Type your message below and get a response.")

st.text_input("You:", key="user_input", on_change=handle_input)

if st.button("Clear Chat"):
    st.session_state.history = []

# Display chat history with alternating colors for user and chatbot messages
for chat in st.session_state.history:
    if chat["is_user"]:
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Assistant:** {chat['message']}")
