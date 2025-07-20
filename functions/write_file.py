import os

from google.genai import types

from utils import is_within_directory

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get contents from",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The file contents to write"
            ),
        },
    ),
)


def write_file(working_dir, file_path, content):
    try:
        full_file_path = os.path.realpath(os.path.join(working_dir, file_path))

        if not is_within_directory(working_dir, full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        target_dir = os.path.dirname(full_file_path)
        os.makedirs(target_dir, exist_ok=True)

        with open(full_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
