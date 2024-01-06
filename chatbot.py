from openai import OpenAI

import os


class ChatBot:
    '''
    Class to setup the the GPT interface and a couple helper functions.
    '''
    def __init__(self, api_key, gpt_engine_choice):
        print("\ninit chatbot\n")
        # get the key form the streamlit app
        self.client = OpenAI(api_key=api_key)
        self.gpt_engine = gpt_engine_choice
        self.messages = ['']  # initialize the messages list
        self.system_default = \
            "You are an AI assistant." + \
            "\nYou only provide factual responses." + \
            "\nA factual response is one that is derived with public data." + \
            "\nYou will provide references for where the information you provide was obtained." + \
            "\nYou should always adhere to technical information." + \
            "\nYour responses should be informative and logical." + \
            "\nYou are collaborative and do not repeat context, facts, or phrases." + \
            "\nYou do not use too many extraneous words and phrases." + \
            "\nMinimize any other prose." + \
            "\nYour response should be in markdown unless otherwise specified by the user."

    def set_system_prompt(self, content_type, ext_prompt):
        # setup the default system prompt based on the content type
        if content_type == "general":
            prompt = self.system_default
        elif content_type == "email":
            prompt = self.system_default + \
                    "\nYou specialize in writing short and succinct emails." + \
                    "\nDetermine if the user provided an existing email." + \
                    "\nIf an existing email is identified, then rewrite it." + \
                    "\nIf no email is identified then generate a new email based on the user request."
        elif content_type == "code":
            # taken from the github copilot system rules and removed a lot of the constraints.
            prompt = self.system_default + \
                    "\nYou are an expert programmer and specialize in writing computer software." + \
                    "\nFirst think step-by-step." + \
                    "\nThen describe your plan for what to build in pseudocode, written out in great detail." + \
                    "\nThen output the code in a single code block." + \
                    "\nKeep your answers short and impersonal." + \
                    "\nFollow the user's requirements carefully & to the letter." + \
                    "\nUse Markdown formatting in your answers." + \
                    "\nMake sure to include the programming language name at the start of the Markdown code blocks." + \
                    "\nAvoid wrapping the whole response in triple backticks."
        elif content_type == "blog":
            prompt = self.system_default + \
                    "\nYou specialize in writing short and succinct blogs." + \
                    "\nDetermine if the user provided an existing blog entry." + \
                    "\nIf an existing blog is identified, then rewrite it." + \
                    "\nIf no blog is identified then generate a new blog based on the request."
        elif content_type == "todoist":
            prompt = ""
        else:
            # This allows for a custom prompt
            prompt = ""

        # add the extension prompt
        prompt += ext_prompt
        self.messages[0] = {"role": "system", "content": prompt}

    def send(self, role, content, temperature, history_len):
        self.messages.append({"role": role, "content": content})
        messages = self.messages[-history_len:]

        response = self.client.chat.completions.create(model=self.gpt_engine,
                                                       messages=messages,
                                                       temperature=temperature)

        message = response.choices[0].message.content.strip()

        # add the message to the list of messages
        self.messages.append({"role": "assistant", "content": message})

        return message

    def set_message_content(self, index, content):
        self.messages[index]["content"] = content


if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    auto_gpt = ChatBot(api_key, 'gpt-3.5-turbo')
    response = auto_gpt.send(auto_gpt.get_topic())
    print(response)
