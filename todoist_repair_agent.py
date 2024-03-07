import os
import pydantic
from chatbot import ChatBot


SYSTEM_PROMPT = \
        "Your task is to fix the FAULTY_INPUT such that it can be parsed into the JSON_SCHEMA." + \
        "\nUse the ERROR_MSG to create a FIXED_INPUT." + \
        "\nThe FIXED_INPUT should be in the same format as the FAULTY_INPUT." + \
        "\nYou are only allowed to respond in json format."


def parse_base_model_with_retries(
    raw_response: str, base_model: pydantic.BaseModel, retries: int = 3
) -> pydantic.BaseModel:
    """
    Parses the raw response using the specified base model with retries.

    Args:
        raw_response (str): The raw response to parse.
        base_model (pydantic.BaseModel): The base model to use for parsing.
        retries (int, optional): The number of retries to attempt. Defaults to 3.

    Returns:
        pydantic.BaseModel: The parsed base model.

    Raises:
        ValueError: If the parsing fails after the specified number of retries.
    """

    openai_api_key = os.getenv('OPENAI_API_KEY', None)
    chatbot = ChatBot(openai_api_key)
    chatbot.set_system_prompt(None, SYSTEM_PROMPT)

    updated_input_str = raw_response

    for _ in range(retries):
        try:
            return base_model.parse_raw(updated_input_str)
        except Exception as exception:
            updated_input_str = chatbot.send(
                    "assistant", _format_fix_prompt(updated_input_str, base_model, exception), 0.70, 15
            )
            print(f"Could not parse input.\nOriginal: {raw_response}\nTry to update the input to: {updated_input_str}") # noqa

    raise ValueError(
        f"Failed to repair with retries.\nOriginal input: {raw_response}\nTry to update the input to: {updated_input_str}" # noqa
    )


def _format_fix_prompt(
    updated_input_str: str,
    base_model: pydantic.BaseModel,
    exception: Exception,
) -> str:
    """
    Formats the fix prompt with the JSON schema, faulty input, error message, and fixed input.

    Args:
        updated_input_str (str): The updated input string.
        base_model (pydantic.BaseModel): The base model used for validation.
        exception (Exception): The exception raised during validation.

    Returns:
        str: The formatted fix prompt.

    """
    return f'''
JSON_SCHEMA:
{base_model.schema()}

FAULTY_INPUT:
{updated_input_str}

ERROR_MSG:
{exception}
FIXED_INPUT:'''.strip()
