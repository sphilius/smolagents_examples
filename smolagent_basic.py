from smolagents import CodeAgent, HfApiModel
import os
from dotenv import load_dotenv

def run_agent_query(question: str) -> str:
    # Load environment variables from .env file
    load_dotenv() # Keep this here if each call might be in a different context
                    # or move it outside if .env is loaded once globally.

    # API key is implicitly used by HfApiModel if not passed directly,
    # assuming it's configured in smolagents or huggingface_hub libraries
    # from environment variables like HF_TOKEN.
    # No explicit api_key variable is used in HfApiModel instantiation in the original.

    model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
    agent = CodeAgent(tools=[], model=model)
    answer = agent.run(question)
    return answer

if __name__ == "__main__":
    # Get API key from environment variables - for the main execution block
    # This is mostly for the direct execution scenario.
    # HfApiModel typically picks up HF_TOKEN from the environment automatically.
    load_dotenv()
    api_key = os.getenv("HF_TOKEN") # This line is actually not strictly necessary for HfApiModel
                                    # if HF_TOKEN is already set in the environment.
    if not api_key and not os.getenv("HF_TOKEN"):
        print("HF_TOKEN environment variable not found. Please set it in your .env file or environment.")
    else:
        question = "What is the cube of 2?"
        answer = run_agent_query(question)
        print(f"The answer to '{question}' is: {answer}")