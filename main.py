import os
import sys
import click
from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f" * Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f" * Response tokens: {response.usage_metadata.candidates_token_count}\n")
    print(f"Response: \n{response.text}")


if __name__ == "__main__":

    main()
