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

def stream_logs_to_chatgpt(brief, verbose):
    model_name = "gpt-3.5-turbo"
    logs = get_log_files()
    
    for log in logs:
        chunks = chunk_text(log)
        for chunk in chunks:
            instruction = "Analyze the following logs and provide a detailed response:" if verbose else "Summarize the main points of the following logs:"
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--brief', action='store_true', help='Only summarize the main points of the logs.')
    group.add_argument('--verbose', action='store_true', help='Provide a detailed response analyzing the logs.')
    args = parser.parse_args()

    stream_logs_to_chatgpt(args.brief, args.verbose)
