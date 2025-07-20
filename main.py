import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MAX_AGENT_ITERATIONS, system_prompt
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file,
    ]
)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Python CLI AI Agent")

    parser.add_argument("prompt", type=str, help="User prompt passed to AI agent")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    user_prompt = args.prompt

    api_key = os.environ.get("GEMINI_API_KEY")

    try:
        client = genai.Client(api_key=api_key)

        messages = [
            types.Content(role="User", parts=[types.Part(text=user_prompt)]),
        ]

        config = types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        )

        # Track agent loop
        current_iteration = 0

        while current_iteration < MAX_AGENT_ITERATIONS:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=config,
                )
            except Exception as e:
                print(f"[ERROR] Failed to generate content: {e}")
                break

            # Add LLM response to messages list
            if isinstance(response.candidates, list):
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)

            if args.verbose and response.usage_metadata:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            for fc in response.function_calls or []:
                try:
                    # Perform function call
                    result = call_function(fc, args.verbose)

                    # Add functional call response to messages list
                    messages.append(result)

                    if (
                        not result.parts
                        or not result.parts[0].function_response
                        or not isinstance(
                            result.parts[0].function_response.response, dict
                        )
                    ):
                        raise Exception(f"Failed function call: {fc.name}")

                    if args.verbose:
                        print(
                            f"-> {result.parts[0].function_response.response.get('result')}"
                        )

                except Exception as e:
                    print(f"[ERROR] While calling function '{fc.name}': {e}")
                    break

            current_iteration += 1

            if not response.function_calls and response.text:
                print(response.text)
                break
        else:
            print("[INFO] Agent reached max iterations with no final response.")

    except Exception as e:
        print(f"[FATAL ERROR] {e}")


if __name__ == "__main__":
    main()
