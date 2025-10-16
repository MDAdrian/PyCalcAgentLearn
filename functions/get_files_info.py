import os

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
