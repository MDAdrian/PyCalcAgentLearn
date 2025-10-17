import os
import sys
import click
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import available_functions


@click.command()
@click.argument("prompt", type=str)
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(prompt, verbose):
    print("Hello from pyagent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt
)
    )
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f" * Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f" * Response tokens: {response.usage_metadata.candidates_token_count}\n")
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Response: \n{response.text}")


if __name__ == "__main__":

    main()
