import os
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_file import schema_run_python_file, run_python_file
from functions.write_files import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name

    # Ensure args is a dictionary
    args = dict(function_call_part.args or {})

    # Manually set the working directory argument
    args["working_directory"] = os.path.abspath("./calculator")

    # Dispatch table mapping function names to actual Python functions
    function_map = {
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file
    }

    # Check that the function name exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # Otherwise, call the corresponding function
    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        # Handle runtime errors gracefully
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Exception while executing: {str(e)}"},
                )
            ],
        )

    # Return structured success response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )