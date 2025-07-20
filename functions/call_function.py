from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    name = function_call_part.name

    if name is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="unknown", response={"error": "Function call missing name"}
                )
            ],
        )

    fn = function_map.get(name)

    if fn is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name, response={"error": f"Unknown function {name}"}
                )
            ],
        )
    else:
        keyword_args = function_call_part.args.copy() if function_call_part.args else {}
        keyword_args["working_dir"] = "."

        result = fn(**keyword_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name, response={"result": result}
                )
            ],
        )
