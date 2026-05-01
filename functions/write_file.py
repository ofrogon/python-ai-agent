import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_abs_directory = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid_abs_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        existing_directory = os.path.isdir(abs_file_path)
        if existing_directory:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

    except Exception as e:
        content = f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
