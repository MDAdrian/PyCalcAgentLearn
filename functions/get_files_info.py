import os
from google.genai import types
from config import MAX_CHARS

    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def get_files_info(working_directory, directory="."):
    """
    List files in a directory relative to a working directory, safely.

    Returns:
        str: A formatted list of files or an error string starting with "Error:".
    """
    try:
        # Build the full path
        full_path = os.path.join(working_directory, directory)

        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)

        # Ensure the target directory stays within the working directory
        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if it is a valid directory
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a valid directory'

        # List directory entries
        entries = os.listdir(abs_target_dir)

        # Build formatted string lines
        lines = []
        for entry in sorted(entries):
            entry_path = os.path.join(abs_target_dir, entry)
            is_dir = os.path.isdir(entry_path)
            size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
            lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        # Catch any unexpected exception and return an error string
        return f"Error: {str(e)}"


def get_file_content(working_directory, file_path):
    try:
        # Build the full path
        full_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure the target directory stays within the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if file is not a file or not found
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) > MAX_CHARS:
                truncated = file_content_string[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return truncated
            return file_content_string

    except Exception as e:
        # Catch any unexpected exception and return an error string
        return f"Error: {str(e)}"