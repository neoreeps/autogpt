import openai
import os


class AutoGPT:
    '''
    Class to setup the the GPT interface and a couple helper functions.
    '''
    def __init__(self, api_key, gpt_engine_choice, content_type):
        # get the key form the streamlit app
        openai.api_key = api_key
        self.gpt_engine_choice = gpt_engine_choice
        self.content_type = content_type
        self.system = "You are an assistant"
        # setup the default system prompt based on the content type
        if content_type == "email":
            self.system = '''You are a friendly assistant.
You specialize in writing short and succinct emails.
You are collaborative and do not repeat context.
You do not use too many extraneious words and phrases.
Identify if the request is an existing email or a request for a new one.
If an existing, then rewrite it, otherwise generate a new email based on the request.
Minimize any other prose.'''
        elif content_type == "code":
            # taken from the github copilot system rules and removed a lot of the constraints.
            self.system = '''You are an AI programming assistant.
Follow the user's requirements carefully & to the letter.
Your responses should be informative and logical.
You should always adhere to technical information.
First think step-by-step.
Then describe your plan for what to build in pseudocode, written out in great detail.
Then output the code in a single code block.
Minimize any other prose.
Keep your answers short and impersonal.
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
Avoid wrapping the whole response in triple backticks.'''
        elif content_type == "general":
            self.system = '''You are a friendly assistant.'''

    # context is received from the streamlit app
    def send(self, content, temperature=0.7):
        response = openai.ChatCompletion.create(
            model=self.gpt_engine_choice,
            messages=[
                {"role": "system", "content": self.system},
                {"role": "user", "content": content}
            ],
            temperature=temperature
        )

        return response["choices"][0].message["content"]


if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    auto_gpt = AutoGPT(api_key, 'gpt-3.5-turbo')
    response = auto_gpt.send(auto_gpt.get_topic())
    print(response)
