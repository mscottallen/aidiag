import openai
import os
from dotenv import load_dotenv
import argparse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_log_files():
    logs = []
    for file in os.listdir():
        if file.endswith('.log'):
            with open(file, 'r') as log_file:
                logs.append(log_file.read())
    return logs

def chunk_text(text, size=2000):
    return [text[i:i+size] for i in range(0, len(text), size)]

def ingest_logs():
    model_name = "gpt-3.5-turbo"
    logs = get_log_files()
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. The user is a full stack developer and the logs you're analyzing come from their servers. Retain this context throughout the conversation."
        }
    ]

    for log in logs:
        chunks = chunk_text(log)
        for chunk in chunks:
            messages.append({"role": "user", "content": f"Ingesting log:\n{chunk}"})
            response = openai.ChatCompletion.create(model=model_name, messages=messages)
            messages.append({"role": "assistant", "content": response['choices'][0]['message']['content'].strip()})

    return messages

def interactive_chat(messages):
    model_name = "gpt-3.5-turbo"
    print("Logs have been ingested. What would you like to troubleshoot?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(model=model_name, messages=messages)
        print("Assistant:", response['choices'][0]['message']['content'].strip())

def main():
    parser = argparse.ArgumentParser(description="Send log files in the current directory to ChatGPT for debugging.",
                                     epilog="During the stream of logs, you can press the 'q' key followed by 'Enter' to stop the stream, or use CTRL+C to interrupt it.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--brief", action="store_true", help="Provide a concise summary of the main issues in the logs.")
    group.add_argument("--verbose", action="store_true", help="Provide a detailed analysis of the logs.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Engage in an interactive chat with the model after ingesting logs.")

    args = parser.parse_args()

    if args.interactive:
        messages = ingest_logs()
        interactive_chat(messages)
    else:
        if not args.brief and not args.verbose:
            args.verbose = True

        stream_logs_to_chatgpt(brief=args.brief)

if __name__ == '__main__':
    main()
