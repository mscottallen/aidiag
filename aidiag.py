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
    model_name = "gpt-3.5-turbo-16k"
    logs = get_log_files()

    # Combine all logs into a single string
    all_logs = "\n".join(logs)

    # Truncate logs to fit within model's token limit
    MAX_TOKENS = 16300  # Setting a slightly lower limit to account for other message tokens
    truncated_logs = all_logs[:MAX_TOKENS]  # Slice the string to fit the limit

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. The user is a full stack developer and the logs you're analyzing come from their servers. Remember the context of these logs for troubleshooting."
        },
        {"role": "user", "content": f"Ingest the following logs for analysis:\n{truncated_logs}"}
    ]

    response = openai.ChatCompletion.create(model=model_name, messages=messages)
    return messages

def stream_logs_to_chatgpt(brief):
    model_name = "gpt-3.5-turbo-16k"
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
            
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            )
            # Print the assistant's response (the last message in the response).
            print(response['choices'][0]['message']['content'].strip())


def interactive_chat(messages):
    model_name = "gpt-3.5-turbo-16k"
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
        # Default to verbose if no option is provided
        if not args.brief:
            args.verbose = True
        stream_logs_to_chatgpt(brief=args.brief)

if __name__ == '__main__':
    main()