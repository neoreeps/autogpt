import os
import streamlit as st
from utils import EmailGPT

st.set_page_config(page_title="Email GPT Writer", layout="wide")
st.title("Email auto formatter and writer 🤖")

# Sidebar
with st.sidebar:
    st.title("Settings")

    # setup API key to override
    api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI API key here")

    # GPT Engine choice
    gpt_engine_choice = st.radio(
        "Choose GPT engine (your API KEY must have access to the model):",
        ("gpt-3.5-turbo", "gpt-4")
    )

# load key from env if not provided
if not api_key:
    api_key = os.getenv('OPENAI_API_KEY')

auto_email = EmailGPT(api_key, gpt_engine_choice)

user_input = st.text_input("Enter an email topic or leave it blank to rewrite an existing email.:",
                           help="Enter a descripton of your idea here and then select generate to create the email.")

email_input = st.text_area("OR paste your existing email here if you want to improve it:", height=300,
                           help="Type or paste your existing email here and then select generate to rewrite the email.")

if st.button("Generate Email"):
    if not api_key:
        st.title("Please enter your OpenAI API key in the sidebar first!")
    with st.spinner("Generating ..."):
        if email_input:
            gpt_input = f"The current email is:\n```\n{email_input}\n``` Rewrite the email."
            response = auto_email.send(gpt_input)
            st.write(response)
        else:
            if user_input:
                gpt_input = auto_email.get_email_topic(user_input)
            else:
                gpt_input = auto_email.get_email_topic("")

            response = auto_email.send(gpt_input)

            st.write(response)
