# AI Coding Agent

This project implements an AI coding agent that interacts with the user via a command-line interface. It leverages the Gemini API to understand user requests and perform actions such as listing files, reading file content, writing files, and running Python files.

## Key Components

*   **config.py**: Configuration settings for the agent.
*   **main.py**: The main entry point, responsible for parsing user input, interacting with the Gemini API, and calling functions.
*   **utils.py**: Utility functions.
*   **functions**: Directory containing implementations for callable functions like file I/O and code execution.

## Usage

To use the agent, you will need a Gemini API key.  Set the `GEMINI_API_KEY` environment variable with your key, then run `python main.py <your_prompt>` from the command line.

Example: `python main.py "List files in the current directory"`