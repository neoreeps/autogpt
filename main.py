import os
import streamlit as st
from utils import AutoGPT


# Set up the layout of the Streamlit app
st.set_page_config(page_title="Content GPT Writer", layout="wide")
st.title("Auto Content")
st.markdown("### Email and Code and Content Generator")

# Add a sidebar for settings
with st.sidebar:
    # Add radio buttons for choosing GPT engine and content type, and a text input for API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI API key here")
    gpt_engine_choice = st.radio("Choose GPT engine:", ("gpt-3.5-turbo", "gpt-4"))
    content_type = st.radio("Select the type of content to generate or improve:", ("code", "email", "general"))

# Load API key from environment variables if not provided
if not api_key:
    api_key = os.getenv('OPENAI_API_KEY')

# Create an instance of the AutoGPT class
auto_gpt = AutoGPT(api_key, gpt_engine_choice, content_type)

# Add text inputs for entering topic and existing content
topic = st.text_input("Enter a topic or leave it blank to rewrite existing content. Note: any content below will override this field:",  # noqa
                      help="Enter a descripton of your idea here and then select generate to create the content.")
content = st.text_area("OR paste your existing content here if you want to improve it:", height=300,
                       help="Type or paste your existing content here and then select generate to rewrite it.")
auto_gpt.system = st.text_area("Edit the system prompt below, the default is shown:",
                               auto_gpt.system,
                               height=200)

st.write(auto_gpt.system)
# Add a "Generate Content" button
if st.button("Generate Content"):
    if not api_key:
        # Display an error message if API key is not provided
        st.title("Please enter your OpenAI API key in the sidebar first!")
    else:
        with st.spinner("Generating ..."):
            # Get the input text to send to the OpenAI API
            if content:
                gpt_input = content
            else:
                if topic:
                    gpt_input = auto_gpt.get_topic(topic)
                else:
                    gpt_input = auto_gpt.get_topic("")
            # Send request to the OpenAI API and display the generated content
            response = auto_gpt.send(gpt_input)
            st.write(response)
