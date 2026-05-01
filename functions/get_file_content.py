import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    content = ""
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

        valid_abs_directory = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid_abs_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        existing_file = os.path.exists(abs_file_path) or os.path.isfile(abs_file_path)
        if not existing_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        content = f"Error: {e}"
    
    return f"Result for current file:\n{content}"

