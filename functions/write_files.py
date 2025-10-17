import os

def write_file(working_directory, file_path, content):
    """
    Safely writes content to a file inside the given working directory.

    Returns:
        str: Success message or an error string prefixed with "Error:".
    """

    try:
        # Build the full path
        full_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure the target file stays within the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        # If the target path is an existing directory, abort
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" because it is a directory'

        # Create parent directories if they don't exist
        file_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        # Write the file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as ex:
        return f'Error: Cannot write to "{file_path}" because {ex}'

