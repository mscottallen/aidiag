import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def stream_logs_to_chatgpt():
    log_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.log')]
    
    for log_file in log_files:
        with open(log_file, 'r') as file:
            content = file.read()
            
            # Send content to ChatGPT
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Debug the following log content from file {log_file}:\n\n{content}",
                max_tokens=500  # Adjust as needed
            )
            
            print(f"Debugging response for {log_file}:")
            print(response.choices[0].text.strip())
            print("-------------------------------")

if __name__ == "__main__":
    stream_logs_to_chatgpt()
