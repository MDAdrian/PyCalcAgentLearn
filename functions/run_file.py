import os
import subprocess
import sys
from google.genai import types

def format_completed_process(completed: subprocess.CompletedProcess) -> str:
    """Return a readable summary of the subprocess output."""
    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()

    # Handle empty output clearly
    if not stdout and not stderr:
        return "No output produced."

    parts = []
    if stdout:
        parts.append(f"STDOUT:\n{stdout}")
    if stderr:
        parts.append(f"STDERR:\n{stderr}")

    if completed.returncode != 0:
        parts.append(f"Process exited with code {completed.returncode}")

    return "\n\n".join(parts)


def run_python_file(working_directory, file_path, args=None) -> str:
    """Run a Python file and return formatted output as a string."""
    if args is None:
        args = []

    try:
        # Build and resolve paths
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure the file is within the working directory
        try:
            inside = os.path.commonpath([abs_file_path, abs_working_dir]) == abs_working_dir
        except ValueError:
            inside = False

        if not inside:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # File existence and type validation
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the subprocess
        cmd = [sys.executable, abs_file_path, *args]
        completed = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        return format_completed_process(completed)

    except subprocess.TimeoutExpired as e:
        return f'Error: Timeout after 30 seconds while running "{file_path}"'
    except Exception as ex:
        return f'Error: Failed to execute "{file_path}" because: {ex}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file from a file path and return formatted output as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path where to read the file conntent. File path may contain directory as well. Mandatory to provide.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to pass to the function. If ommited, will execute the file without args.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
