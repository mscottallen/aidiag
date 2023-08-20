import openai
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_log_files():
    """Return the content of all log files in the current directory."""
    logs = []
    for file in os.listdir():
        if file.endswith('.log'):
            with open(file, 'r') as log_file:
                logs.append(log_file.read())
    return logs

def chunk_text(text, size=2000):
    """Divide a large text into chunks of a specified size."""
    return [text[i:i+size] for i in range(0, len(text), size)]

def stream_logs_to_chatgpt(brief):
    model_name = "gpt-3.5-turbo"
    logs = get_log_files()
    
    for log in logs:
        chunks = chunk_text(log)
        for chunk in chunks:
            instruction = "Summarize the main points of the following logs:" if brief else "Analyze the following logs and provide a detailed response:"
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. The user is a full stack developer and the logs you're analyzing come from their servers. Provide information assuming they have full control and knowledge of the system, avoiding references to third-party administrators."
                },
                {"role": "user", "content": f"{instruction}\n{chunk}"}
            ]
            
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            )
            
            # Print the assistant's response (the last message in the response).
            print(response['choices'][0]['message']['content'].strip())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream logs to ChatGPT for analysis.")
    parser.add_argument('--brief', action='store_true', default=False, help='Only summarize the main points of the logs.')
    parser.add_argument('--verbose', action='store_true', default=True, help='Provide a detailed response analyzing the logs (default behavior).')
    args = parser.parse_args()

    if args.brief:
        args.verbose = False

    stream_logs_to_chatgpt(args.brief)
