import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    content = generate_content(client, messages, verbose)
    print(content)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    # Execute tool calls via dispatcher and validate structure.
    tool_results = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        # Must have .parts[0].function_response.response
        try:
            payload = function_call_result.parts[0].function_response.response
        except Exception as e:
            raise RuntimeError(
                "call_function returned invalid types.Content: "
                "missing parts[0].function_response.response"
            ) from e

        if verbose:
            print(f"-> {payload}")

        tool_results.append(function_call_result)

    # Return a single item if only one function was called, otherwise a list.
    return tool_results[0] if len(tool_results) == 1 else tool_results


if __name__ == "__main__":
    main()
