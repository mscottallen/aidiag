import openai
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def stream_logs_to_chatgpt(brief):
    model_name = "gpt-3.5-turbo"
    logs = get_log_files()
    
    for log in logs:
        chunks = chunk_text(log)
        for chunk in chunks:
            
            if brief:
                instruction = "Extract only the main issues or critical points from the following logs:"
            else:
                instruction = "Analyze the following logs and provide a detailed response:"
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. The user is a full stack developer and the logs you're analyzing come from their servers. Provide information assuming they have full control and knowledge of the system, avoiding references to third-party administrators."
                },
                {"role": "user", "content": f"{instruction}\n{chunk}"}
            ]
            
            try:
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=messages
                )
                # Print the assistant's response (the last message in the response).
                print(response['choices'][0]['message']['content'].strip())

                # Check for 'q' key input
                key_input = input("Press 'q' to stop the stream or any other key to continue...")
                if key_input == 'q':
                    print("Stopping the stream...")
                    return
            except KeyboardInterrupt:
                print("\nStream interrupted by user.")
                return

def main():
    parser = argparse.ArgumentParser(description="Send log files in the current directory to ChatGPT for debugging.",
                                     epilog="During the stream of logs, you can press the 'q' key followed by 'Enter' to stop the stream, or use CTRL+C to interrupt it.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", action="store_true", help="Provide a concise summary of the main issues in the logs.")
    group.add_argument("--verbose", action="store_true", help="Provide a detailed analysis of the logs.")
    args = parser.parse_args()

    if args.brief:
        stream_logs_to_chatgpt(brief=True)
    else:
        stream_logs_to_chatgpt(brief=False)

if __name__ == '__main__':
    main()
