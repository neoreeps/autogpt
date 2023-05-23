import openai
import os


class GPT4AutoCoder:
    def __init__(self, api_key, gpt_engine_choice):
        # get the key form the streamlit app
        openai.api_key = api_key
        self.gpt_engine_choice = gpt_engine_choice

    # questions is received from the streamlit app
    def ask_gpt3(self, question):
        response = openai.ChatCompletion.create(
            model= self.gpt_engine_choice,
            messages=[
                {"role": "system", "content": "You are a helpful python coding AI who will generate code and provide suggestions for Python projects based on the user's input or generate ideas and code if the user doesn't provide an idea. start the code block with 'python' word. "},
                {"role": "user", "content": question}
            ]
        )

        # this part tries to parse the code from the response
        try:
            generated_text = response["choices"][0]["message"]["content"]
            print("GENERATED TEXT: " + generated_text)
            generated_text = generated_text[:generated_text.rfind('```')]
            return generated_text.split('python', 1)[1]
        except IndexError:
            for i in range(2):
                response = self.ask_gpt3(question)
                try:
                    return generated_text.split('python', 1)[1]
                except IndexError:
                    print("Error: GPT-3 failed to generate code. Please try again.")
                    pass

    # this part is used to get the project idea from the user
    def get_project_idea(self, user_input):
        if user_input == "":
            return "Generate a Python project idea and provide sample code . Write the code in one code block between triple backticks."
        else:
            return f"Generate code for the Python project '{user_input}' . Write the code in one code block between triple backticks. comment the code."
  

if __name__ == "__main__":
    api_key = "<your_api_key>"
    auto_coder = GPT4AutoCoder(api_key)
    auto_coder.run()

