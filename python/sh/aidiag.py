import requests

API_URL = "https://api.openai.com/v2/engines/davinci/completions"
API_KEY = "YOUR_API_KEY"

def send_to_chatgpt(content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "aidiag/1.0"
    }
    data = {
        "prompt": content,
        "max_tokens": 150  # Adjust as needed
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response_json = response.json()
    return response_json['choices'][0]['text'].strip()

