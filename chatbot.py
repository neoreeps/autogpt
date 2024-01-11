import pydantic
from openai import OpenAI


class ChatBot:
    '''
    Class to setup the the GPT interface and a couple helper functions.
    '''
    def __init__(self, api_key, gpt_engine_choice="gpt-4-1106-preview"):
        print(f"\ninit chatbot...{gpt_engine_choice}\n")
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

    def set_todoist_prompt(self, react_model: pydantic.BaseModel, question: str) -> str:
        prompt = \
                "You are a getting things done (GTD) agent." + \
                f"\nIt is your job to accomplish the following task: {question}" + \
                "\nYou have access to multiple tools to accomplish this task." + \
                "\nSee the action in the json schema for the available tools." + \
                "\nIf you have insufficient information to answer the question," + \
                "you can use the tools to get more information." + \
                "\nAll your answers must be in json format and follow the following schema json schema:" + \
                f"{react_model.schema()}" + \
                "\nIf your json response asks me to preform an action, I will preform that action." + \
                "\nI will then respond with the result of that action." + \
                f"\nLet's begin to answer the question: {question}" + \
                "\nDo not write anything other than json!"
        return self.set_system_prompt("todoist", prompt)

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
            prompt = "You are a getting things done (GTD) assistant."
        else:
            # This allows for a custom prompt
            prompt = ""

        # add the extension prompt
        prompt += ext_prompt
        self.messages[0] = {"role": "system", "content": prompt}

    def send(self, role, content, temp, hist_len):
        self.messages.append({"role": role, "content": content})
        messages = self.messages[-hist_len:]

        response = self.client.chat.completions.create(model=self.gpt_engine,
                                                       messages=messages,
                                                       temperature=temp)

        message = response.choices[0].message.content.strip()

        # add the message to the list of messages
        self.messages.append({"role": "assistant", "content": message})

        return message

    def set_message_content(self, index, content):
        self.messages[index]["content"] = content
