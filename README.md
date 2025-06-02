# How to Create Multi-Agents with SmolAgents

This repository contains example code files shown in the video tutorial about creating multi-agent systems using SmolAgents from Hugging Face.

https://youtu.be/XHijkFRd2TU

The examples demonstrate:

1. Basic CodeAgent - Getting started with a simple agent
2. SmolToolCallingAgent - Adding tool-calling capabilities 
3. SmolOllamaAgent - Using local Ollama models
4. SmolClaudeAgent - Integrating with Claude
5. SmolGeminiAgent - Working with Google's Gemini
6. SmolGradioAgent - Creating agent UIs with Gradio
7. SmolTools - Useful tools and utilities
8. SmolMultiAgent - Coordinating multiple agents
9. SmolBlogWriter - Building a blog writing system with agents

Each file shows a different aspect of building multi-agent systems with the SmolAgents library.

## Getting Started

This repository contains example Python scripts demonstrating the use of the SmolAgents library for building multi-agent systems.

### Environment Setup

It is highly recommended to use a Python virtual environment to manage dependencies and isolate this project from your global Python setup.

1.  **Create a virtual environment**:
    Navigate to the root directory of this repository and run:
    ```bash
    python -m venv venv
    ```
    (If you don't have `python` aliased to Python 3, you might need to use `python3 -m venv venv`)

2.  **Activate the virtual environment**:
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install dependencies**:
    Once the virtual environment is activated, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    Remember to update `requirements.txt` to specify package versions (e.g., `package_name==1.2.3`) for better reproducibility, as prompted in the file.

After these steps, you should be able to run the example scripts. Refer to the "Configuration" section below for setting up necessary API keys.

### Running the Examples

Once your environment is set up and configured (see "Configuration" section below), you can run any of the example Python scripts directly:

```bash
python smolagent_basic.py
python smol_toolcalling_agent.py
# etc.
```
Refer to the comments within each script for more details on what it demonstrates.

## Configuration

These examples often require API keys for various services (Hugging Face, Anthropic Claude, Google Gemini, Jina AI, OpenAI, etc.).
The scripts are generally configured to load these keys from environment variables.

1.  **Create a `.env` file**: Copy the `.env.example` file to a new file named `.env` in the root of the project:
    ```bash
    cp .env.example .env
    ```
2.  **Edit `.env`**: Open the `.env` file and add your actual API keys for the services you intend to use.

The scripts use the `python-dotenv` library to load these variables from the `.env` file automatically.
Refer to individual scripts or the `.env.example` file for the specific environment variables needed. For Ollama, configuration (like the API base URL) is often set directly within the script (e.g., `smol_ollama.py`).

## Running Tests

This project includes a testing strategy to ensure the examples and tools work as expected. (Detailed instructions on running tests will be added here once test implementations are finalized.)

The general approach includes:
- **Unit tests** for individual tools in the `smoltools/` directory (e.g., `python -m unittest smoltools/test_visitwebpage.py`).
- **Integration tests** for agent scripts in the `tests/` directory (e.g., `python -m unittest tests/test_smolagent_basic.py`).
- Tests can be discovered and run using `python -m unittest discover .` from the root directory.

(More specific instructions and any prerequisites for running tests, such as setting up mock environments or specific API keys for test accounts, will be detailed here.)

## Continuous Integration (CI)

For active development and to ensure the examples remain functional, setting up a Continuous Integration (CI) pipeline is recommended. CI can automate tasks like installing dependencies, running tests, and linting code on every commit or pull request.

A typical CI workflow (e.g., using GitHub Actions) for this project might involve the following steps:

1.  **Checkout Code**: Get the latest version of the repository.
2.  **Set up Python**: Prepare the Python environment, possibly testing against multiple Python versions.
3.  **Install Dependencies**: Install packages from `requirements.txt` within a virtual environment.
4.  **Linting (Optional)**: Check code style and quality using a linter like Flake8.
5.  **Run Tests**: Execute unit and integration tests (e.g., using `python -m unittest discover`). API keys for tests should be handled either by using mock services/responses or by providing dummy/test-specific keys securely to the CI environment.
6.  **Run Examples (Optional Smoke Test)**: Optionally, run a selection of the main example scripts to ensure they execute without crashing.

You could implement this by creating a workflow file (e.g., `.github/workflows/main.yml` for GitHub Actions) that defines these jobs and steps. This helps maintain code quality and catch issues early.
