import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python script with the path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to pass to the Python script (default is None)",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

        valid_abs_directory = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid_abs_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        existing_file = os.path.exists(abs_file_path) or os.path.isfile(abs_file_path)
        if not existing_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args != None:
            command.extend(args)

        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"

        if result.stdout == None and result.stderr == None:
            output += "No output produced"

        if result.stdout != None:
            output += f"STDOUT: {result.stdout}"

        if result.stderr != None:
            output += f"STDERR: {result.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
