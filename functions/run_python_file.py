import os
import subprocess
from sys import stderr

from google.genai import types

from utils import is_within_directory


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The args to pass to the python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(working_dir: str, file_path: str, args=[]):
    full_file_path = os.path.realpath(os.path.join(working_dir, file_path))

    if not is_within_directory(working_dir, full_file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python3", full_file_path] + args,
            capture_output=True,
            timeout=30,
            text=True,
        )
        output = []
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        if len(stdout) == 0 and len(stderr) == 0:
            output.append("No output produced")
        else:
            if len(stdout) > 0:
                output.append(f"STDOUT: {completed_process.stdout}")
            if len(stderr) > 0:
                output.append(f"STDERROR: {completed_process.stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output)
    except Exception as e:
        return f"Error executing Python file: {e}"
