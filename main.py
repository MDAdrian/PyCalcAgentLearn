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

    content = generate_content_loop(client, messages, verbose)
    print(content.text)


def generate_content_loop(client, messages, verbose=False, max_iters=20):
    """
    Multi-turn tool-use loop:
    - Calls client.models.generate_content repeatedly (up to max_iters).
    - Appends each candidate's content to messages.
    - Executes any function calls returned by the model.
    - Appends function responses back to messages as role="user".
    - Stops when a turn produces no function calls.

    Returns:
        The final model response object of the last iteration.
    """
    def _append_candidate_contents(response):
        """
        Append each candidate.content to messages, normalizing role to 'model'
        if needed (some SDKs already set this correctly).
        """
        candidates = getattr(response, "candidates", None) or []
        appended = 0
        for cand in candidates:
            content = getattr(cand, "content", None)
            if not content:
                continue
            # Ensure allowed role: 'user' or 'model'. For model output, force 'model'.
            role = getattr(content, "role", "model")
            if role not in ("user", "model"):
                role = "model"
            # Some SDKs need a fresh Content object; others allow reusing `content`.
            # Safest is to rebuild a Content using its parts and normalized role.
            messages.append(
                types.Content(
                    role=role,
                    parts=list(getattr(content, "parts", []) or [])
                )
            )
            appended += 1
        return appended

    def _extract_function_calls(response):
        """
        Get function calls from either response.function_calls (convenience)
        or by scanning candidate.content.parts for .function_call parts.
        """
        fc = getattr(response, "function_calls", None)
        if fc:
            return list(fc)

        calls = []
        for cand in getattr(response, "candidates", []) or []:
            content = getattr(cand, "content", None)
            if not content:
                continue
            for part in getattr(content, "parts", []) or []:
                fn_call = getattr(part, "function_call", None)
                if fn_call:
                    calls.append(fn_call)
        return calls

    last_response = None

    for step in range(max_iters):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,  # full conversation so far
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            last_response = response

            if verbose:
                um = getattr(response, "usage_metadata", None)
                if um:
                    print("Prompt tokens:", getattr(um, "prompt_token_count", "n/a"))
                    print("Response tokens:", getattr(um, "candidates_token_count", "n/a"))

            # 1) Append all candidate contents to the conversation
            _append_candidate_contents(response)

            # 2) Extract all function calls for this turn
            function_calls = _extract_function_calls(response)

            # 3) If no function calls -> we're done (model has produced final text)
            if not function_calls:
                break

            # 4) Execute each function call and append tool results as user message
            for function_call_part in function_calls:
                try:
                    function_call_result = call_function(function_call_part, verbose=verbose)
                except Exception as e:
                    # Surface tool-level exceptions clearly
                    raise RuntimeError(f"Tool execution failed for {getattr(function_call_part, 'name', '<unknown>')}: {e}") from e

                # Validate structure: must have .parts[0].function_response.response
                try:
                    payload = function_call_result.parts[0].function_response.response
                except Exception as e:
                    raise RuntimeError(
                        "call_function returned invalid types.Content: "
                        "missing parts[0].function_response.response"
                    ) from e

                if verbose:
                    print(f"-> {payload}")

                # Append the function_response back as a 'user' message
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_call_result.parts
                    )
                )

            # Loop continues to let the model react to the tool outputs

        except Exception as e:
            # Catch and report any iteration-level exceptions (API/logic/etc.)
            raise RuntimeError(f"generate_content_loop failed at step {step}: {e}") from e

    return last_response



if __name__ == "__main__":
    main()
