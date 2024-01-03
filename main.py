import os
import streamlit as st
from utils import AutoGPT


# Set up the layout of the Streamlit app
st.set_page_config(page_title="Content GPT Writer", layout="wide")
st.title("Auto Content")
st.write('See the code: https://github.com/neoreeps/autogpt')

# Predefine variables
tone = 'professional'
client = 'coworker'
lang = 'python'

# Add a sidebar for settings
with st.sidebar:
    # Add radio buttons for choosing GPT engine and content type, and a text input for API key
    api_key = os.getenv('OPENAI_API_KEY', None)
    if not api_key:
        api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI APIkey here")
    gpt_engine_choice = st.selectbox("Choose GPT engine:", ("gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo"))
    temperature = st.slider("Select the temperature (entropy): ", 0.0, 1.0, 0.7)
    history_len = st.slider("Select the history length:", 1, 25, 15)
    content_type = st.radio("Select the type of content to generate or improve:",
                            ("general", "code", "email", "blog"))

    if content_type == "email":
        tone = st.selectbox("Select the tone of the email:", ("professional", "funny", "negative", "friendly"))
        client = st.radio("Select the audience for the email:",
                          ('boss', 'coworker', 'executive', 'engineer', 'direct report'))
    elif content_type == "code":
        lang = st.radio("Select the initial language of the code: \
                \n(Note: you may convert code at any time by simply asking the assistant to convert the code)",
                        ("python", "c/c++", "bash", "html", "javascript", "r"))

    # clear the session state if the user changes the content type
    if 'auto_gpt' in st.session_state:
        del st.session_state.auto_gpt


# Create an instance of the AutoGPT class
if 'auto_gpt' not in st.session_state:
    st.session_state.auto_gpt = AutoGPT(api_key, gpt_engine_choice)

# Get the instance of the AutoGPT class
auto_gpt = st.session_state.auto_gpt

# Add text inputs for entering topic and existing content
st.markdown(f"### {content_type.upper()} Content Generator")

# Update the system prompt for email tone or code language
if content_type == "email":
    ext_prompt = \
        f"\nThe tone of the email shall be {tone}." + \
        f"\nThe email shall be written to target the following audience: {client}."

elif content_type == "code":
    ext_prompt = \
        f"\nIf there is existing code, first identify the language and then rewrite it in {lang}." + \
        f"\nIf this is new code, then write it only in {lang} unless another language was requested."
else:
    ext_prompt = "\nFollow the user's requirements carefully & to the letter."

# Set the system prompt
auto_gpt.set_system_prompt(content_type, ext_prompt)

# Allow the user to update the prompt
with st.expander("Edit the system prompt below, the default is shown:"):
    prompt = st.text_area("System Prompt:",
                          auto_gpt.messages[0]["content"],
                          height=200)
    auto_gpt.set_system_prompt(content_type, prompt)

message = st.chat_message("assistant")
message.write("Hello Human!")
content = st.chat_input("Type your request or paste your existing content here if you want to improve it:")
if content:
    message.write(content)
    with st.spinner("Thinking..."):
        message.write(auto_gpt.send(content, temperature, history_len))

if st.button("Clear"):
    auto_gpt.messages = auto_gpt.messages[:1]
    message.empty()
    content = ""
