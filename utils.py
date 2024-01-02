import openai
import os


class AutoGPT:
    '''
    Class to setup the the GPT interface and a couple helper functions.
    '''
    def __init__(self, api_key, gpt_engine_choice, content_type, history_len):
        # get the key form the streamlit app
        openai.api_key = api_key
        self.gpt_engine = gpt_engine_choice
        self.content_type = content_type
        self.history_len = history_len
        self.messages = []
        self.system_default = '''
You are an AI assistant.
You only provide factual responses.
A factual response is one that is derived with public data.
You will provide references for where the information you provide was obtained.
You should always adhere to technical information.
Your responses should be informative and logical.
You are collaborative and do not repeat context, facts, or phrases.
You do not use too many extraneous words and phrases.
Minimize any other prose.
Your response should be in markdown unless otherwise specified by the user.'''
        # setup the default system prompt based on the content type
        if content_type == "email":
            self.system = self.system_default + '''
You specialize in writing short and succinct emails.
Determine if the user provided an existing email.
If an existing email is identified, then rewrite it
If no email is identified then generate a new email based on the user request.'''
        elif content_type == "code":
            # taken from the github copilot system rules and removed a lot of the constraints.
            self.system = self.system_default + '''
You are an AI programming assistant.
First think step-by-step.
Then describe your plan for what to build in pseudocode, written out in great detail.
Then output the code in a single code block.
Keep your answers short and impersonal.
Follow the user's requirements carefully & to the letter.
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
Avoid wrapping the whole response in triple backticks.'''
        elif content_type == "blog":
            self.system = self.system_default + '''
You specialize in writing short and succinct blogs.
Determine if the user provided an existing blog entry.
If an existing blog is identified, then rewrite it
If no blog is identified then generate a new blog based on the request.'''
        else:
            self.system = self.system_default + '''Follow the user's requirements carefully & to the letter.'''

        # set the system prompt
        self.messages.append({"role": "system", "content": self.system})

    # context is received from the streamlit app
    def send(self, content, temperature=0.7):
        self.messages.append({"role": "user", "content": content})
        messages = self.messages[-self.history_len:]

        response = openai.ChatCompletion.create(
            model=self.gpt_engine,
            messages=messages,
            temperature=temperature
        )

        message = response["choices"][0].message["content"]

        # add the message to the list of messages
        self.messages.append({"role": "assistant", "content": message})

        return message


if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    auto_gpt = AutoGPT(api_key, 'gpt-3.5-turbo')
    response = auto_gpt.send(auto_gpt.get_topic())
    print(response)
