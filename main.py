import streamlit as st
from main_self_improve_Class import GPT4AutoCoder
import os
import openai

st.set_page_config(page_title="GPT-4 Auto Coder", layout="wide")
st.title("GPT-4 Auto Coder and Self Improver 🤖")

# Sidebar
with st.sidebar:
    st.title("Settings")

    # API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI API key here")

    if api_key:
        st.session_state["OPENAI_API_KEY"] = api_key

    # GPT Engine choice
    gpt_engine_choice = st.radio(
        "Choose GPT engine:",
        ("gpt-3.5-turbo", "gpt-4")
    )
    # st.markdown("[![Foo](https://www.echohive.live/youtube.jpg)](http://google.com.au/)")
    st.title("Watch the [Video](https://youtu.be/rBQrdEoSbhk)")

    st.title("Download the [Code](https://www.patreon.com/posts/basic-files-gpt-80551058?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link)")

    st.title("Download the simultenous multiple improvements [Code](https://www.patreon.com/posts/all-files-gpt-4-80551109?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link)")

    st.title("Chat with us at [discord](https://discord.gg/PPxTP3Cs3G)")

auto_coder = GPT4AutoCoder(api_key, gpt_engine_choice)

user_input = st.text_input("Enter an idea for a Python project or leave it blank for a random suggestion:", help="enter a descripton of your idea here and then select the number of iterations for improvement. Then click on the 'Generate Code' button to get the code.")

code_input = st.text_area("OR paste your existing code here if you want to improve it:", height=300, help="type or paste your existing code here and then select the number of iterations for improvement. Then click on the 'Generate Code' button to get the code improved.")

num_attempts = st.number_input("Enter the number of iterations for improvement:", min_value=0, value=1, step=1, help="GPT will try to improve the code this many times. GPT will add new features, error catching, bug fixing, etc. to the code.")

if st.button("Generate Code"):
    if not st.session_state.get("OPENAI_API_KEY"):
        st.title("Please enter your OpenAI API key in the sidebar first!")
    with st.spinner("Generating code..."):
        if code_input:
            existing_code = code_input

            for attempt in range(1, num_attempts + 1):
                gpt3_question = f"The current code is:\n```\n{existing_code}\n``` Improve the following Python code (implement new ideas if necessary), including error catching and bug fixing. Write the entire code from scratch while implementing the improvements. Start the code block with a simple 'python' word. Comment about the changes you are making."
                response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)
                existing_code = response
                st.write("Iteration", attempt, "of", num_attempts, "code improvements completed.")
                st.code(response, language="python")
        else:
            if user_input:
                gpt3_question = GPT4AutoCoder(api_key, gpt_engine_choice).get_project_idea(user_input)
            else:
                gpt3_question = GPT4AutoCoder(api_key, gpt_engine_choice).get_project_idea("")

            response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)

            st.code(response, language="python")

            for attempt in range(1, num_attempts + 1):
                gpt3_question = f"The current code is:\n```\n{response}\n``` Improve the following Python code (implement new ideas if necessary), including error catching and bug fixing. Write the entire code from scratch while implementing the improvements. Start the code block with a simple 'python' word. Comment about the changes you are making."
                response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)
                st.code(response, language="python")
