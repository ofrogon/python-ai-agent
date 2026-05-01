import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    result = ""
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

        valid_abs_directory = os.path.commonpath([abs_working_directory, abs_directory]) == abs_working_directory
        if not valid_abs_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        existing_directory = os.path.exists(abs_directory)
        if not existing_directory:
            return f'Error: "{directory}" is not a directory'

        directory_content = os.listdir(abs_directory)
        more_content_info = []
        for content in directory_content:
            full_path_content = os.path.join(abs_directory, content)
            more_content_info.append(f" - {content}: file_size={os.path.getsize(full_path_content)}, is_dir={os.path.isdir(full_path_content)}")

        result = '\n'.join(more_content_info)
    except Exception as e:
        result = f"Error: {e}"

    return f"Result for current directory:\n{result}"

