import os

from google.genai import types

from config import MAX_CHARS
from utils import is_within_directory

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get contents from",
            )
        },
    ),
)


def get_file_content(working_dir, file_path):
    full_file_path = os.path.realpath(os.path.join(working_dir, file_path))

    if not is_within_directory(working_dir, full_file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_file_path, "r") as f:
            full_file_content_string = f.read()

            if len(full_file_content_string) > MAX_CHARS:
                full_file_content_string = (
                    full_file_content_string[:MAX_CHARS]
                    + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return full_file_content_string

    except Exception as e:
        return f"Error: {e}"
