import openai
import os


class EmailGPT:
    def __init__(self, api_key, gpt_engine_choice):
        # get the key form the streamlit app
        openai.api_key = api_key
        self.gpt_engine_choice = gpt_engine_choice

    # context is received from the streamlit app
    def send(self, content, temperature=0.7):
        system = '''
            You are a friendly assistant.
            You specialize in writing short and succinct professional emails.
            You are friendly and collaborative.
            You do not use too many extraneious words and phrases.
            Do not be too formal.
        '''
        response = openai.ChatCompletion.create(
            model=self.gpt_engine_choice,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": content}
            ],
            temperature=temperature
        )

        return response["choices"][0].message["content"]

    def get_email_topic(self, user_input=""):
        '''
        Obtain the topic of the desired email from user input.
        If no input is provided, generate a random topic.
        '''

        if user_input == "":
            return "Generate an email topic and create an example email."
        else:
            return f"Generate am email based on the following topic: '{user_input}'."


if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    auto_email = EmailGPT(api_key, 'gpt-3.5-turbo')
    response = auto_email.send(auto_email.get_email_topic())
    print(response)
