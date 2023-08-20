import openai
import os
from dotenv import load_dotenv

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

def stream_logs_to_chatgpt():
    model_name = "gpt-3.5-turbo"  # or whatever the appropriate model is
    logs = get_log_files()
    
    for log in logs:
        chunks = chunk_text(log)
        for chunk in chunks:
            response = openai.Completion.create(
                model=gpt-3.5-turbo-16k,
                prompt=f"Analyze the following logs:\n{chunk}"
            )
            print(response.choices[0].text.strip())

stream_logs_to_chatgpt()
