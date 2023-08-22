import openai
import os
from dotenv import load_dotenv
import argparse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_log_files(directory='.'):
    logs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.log'):
                with open(os.path.join(root, file), 'r') as log_file:
                    logs.append(log_file.read())
    return logs

def chunk_text(text, size=2000):
    return [text[i:i+size] for i in range(0, len(text), size)]

def ingest_logs(directory, server_type, server_function):
    model_name = "gpt-3.5-turbo-16k"
    logs = get_log_files(directory)

    # Combine all logs into a single string
    all_logs = "\n".join(logs)

    # Truncate logs to fit within model's token limit
    MAX_TOKENS = 16300  # Setting a slightly lower limit to account for other message tokens
    truncated_logs = all_logs[:MAX_TOKENS]  # Slice the string to fit the limit

    context_info = f"You are analyzing logs from a {server_type} server which serves the function of {server_function}."
    messages = [
        {"role": "system", "content": context_info},
        {"role": "user", "content": f"Ingest the following logs for analysis:\n{truncated_logs}"}
    ]

    response = openai.ChatCompletion.create(model=model_name, messages=messages)
    return messages

def stream_logs_to_chatgpt(logs, brief):
    model_name = "gpt-3.5-turbo-16k"
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
            
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            )
            # Print the assistant's response (the last message in the response).
            print(response['choices'][0]['message']['content'].strip())

def main():
    parser = argparse.ArgumentParser(description="Send log files to ChatGPT for debugging.",
                                     epilog="During the stream of logs, you can press the 'q' key followed by 'Enter' to stop the stream, or use CTRL+C to interrupt it.")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--brief", action="store_true", help="Provide a concise summary of the main issues in the logs.")
    group.add_argument("--verbose", action="store_true", help="Provide a detailed analysis of the logs.")
    
    args = parser.parse_args()

    if args.brief or args.verbose:
        logs = get_log_files()
        stream_logs_to_chatgpt(logs, brief=args.brief)
    else:
        server_type = input("Please specify the type of server: ")
        server_function = input("Please specify the server's function: ")
        log_directory = input("Specify the directory to look for log files in: ")

        messages = ingest_logs(log_directory, server_type, server_function)
        interactive_chat(messages)

if __name__ == '__main__':
    main()