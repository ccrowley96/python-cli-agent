import os

from google.genai import types
from utils import is_within_directory

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in the specified directory along with their sizes",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory.  If not provided, lists files in the working directory itself.",
            )
        },
    ),
)


def get_files_info(working_dir, directory="."):
    full_path = os.path.join(working_dir, directory)

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    if not is_within_directory(working_dir, full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    file_details_list = []
    try:
        listdir_res = os.listdir(full_path)

        for file in listdir_res:
            file_path = os.path.join(full_path, file)
            is_dir = os.path.isdir(file_path)

            file_details_list.append(
                f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={is_dir}"
            )

        return "\n".join(file_details_list)
    except Exception as e:
        return f"Error: {e}"
