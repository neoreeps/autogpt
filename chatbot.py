import pydantic
from datetime import datetime
from openai import OpenAI
from logger import get_logger


class ChatBot:
    '''
    A class representing a chatbot powered by GPT.

    Attributes:
        api_key (str): The API key for accessing the GPT service.
        gpt_engine_choice (str): The choice of GPT engine to use (default: "gpt-4-1106-preview").
        client (OpenAI): The OpenAI client for making API requests.
        gpt_engine (str): The selected GPT engine.
        messages (list): The list of chat messages.
        system_default (str): The default system prompt.

    Methods:
        __init__(self, api_key, gpt_engine_choice="gpt-4-1106-preview"): Initializes the ChatBot instance.
        set_todoist_prompt(self, react_model: pydantic.BaseModel, question: str) -> str: Sets the prompt for a Todoist task.  # noqa
        set_system_prompt(self, content_type, ext_prompt): Sets the system prompt based on the content type.
        send(self, role, content, temp, hist_len): Sends a message to the chatbot and receives a response.
        set_message_content(self, index, content): Sets the content of a message in the chat.

    '''

    def __init__(self, api_key, gpt_engine_choice="gpt-4-1106-preview"):
        '''
        Initializes a ChatBot instance.

        Args:
            api_key (str): The API key for accessing the GPT service.
            gpt_engine_choice (str): The choice of GPT engine to use (default: "gpt-4-1106-preview").
        '''
        log = get_logger(__name__)
        log.info(f"Init chatbot...{gpt_engine_choice}\n")
        # get the key form the streamlit app
        self.client = OpenAI(api_key=api_key)
        self.gpt_engine = gpt_engine_choice
        self.messages = ['']  # initialize the messages list
        self.system_default = \
            "You are an AI assistant." + \
            f"\nThe current date and time is: {datetime.now()}" + \
            "\nYou only provide factual responses." + \
            "\nA factual response is one that is derived with public data." + \
            "\nYou will always provide references for where the information you provide was obtained." + \
            "\nYou should always adhere to technical information." + \
            "\nYour responses should be informative and logical." + \
            "\nYou are collaborative and do not repeat context, facts, or phrases." + \
            "\nYou do not use too many extraneous words and phrases." + \
            "\nMinimize any other prose." + \
            "\nYour response should be in markdown unless otherwise specified by the user."

    def set_todoist_prompt(self, react_model: pydantic.BaseModel, question: str) -> str:
        '''
        Sets the prompt for a Todoist task.

        Args:
            react_model (pydantic.BaseModel): The reactive model for the task.
            question (str): The question or task description.

        Returns:
            str: The system prompt for the Todoist task.
        '''
        prompt = "You are a getting things done (GTD) agent." + \
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
        '''
        Sets the system prompt based on the content type.

        Args:
            content_type (str): The type of content (e.g., "general", "document", "code", "todoist").
            ext_prompt (str): The extension prompt specific to the content type.
        '''
        # setup the default system prompt based on the content type
        if content_type == "general":
            prompt = self.system_default
        elif content_type == "document":
            prompt = self.system_default + \
                "\nYou are a professional document writing assistant." + \
                "\nYou are an expert in writing documents." + \
                "\nOnly use the provided documents in {document1} and {document2} to generate the output document."
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
        elif content_type == "todoist":
            prompt = "You are a getting things done (GTD) assistant."
        else:
            # This allows for a custom prompt
            prompt = ""

        # add the extension prompt
        prompt += ext_prompt
        self.messages[0] = {"role": "system", "content": prompt}

    def send(self, role, content, temp, hist_len):
        '''
        Sends a message to the chatbot and receives a response.

        Args:
            role (str): The role of the message ("assistant" or "user").
            content (str): The content of the message.
            temp (float): The temperature for generating the response.
            hist_len (int): The length of chat history to consider.

        Returns:
            str: The response from the chatbot.
        '''
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
        '''
        Sets the content of a message in the chat.

        Args:
            index (int): The index of the message.
            content (str): The new content for the message.
        '''
        self.messages[index]["content"] = content
