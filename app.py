from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Access environment variables set in Vercel
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')  # Use CHAT_ID here

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}'

def send_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    response = requests.post(url, data={'chat_id': chat_id, 'text': text})
    return response.json()

def get_openai_response(query):
    headers = {
        'Content-Type': 'application/json',
        'api-key': OPENAI_API_KEY,
    }
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': [
                    {
                        'type': 'text',
                        'text': 'You are an AI assistant that helps people find information.'
                    }
                ]
            },
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': query
                    }
                ]
            }
        ],
        'temperature': 0.7,
        'top_p': 0.95,
        'max_tokens': 800
    }
    try:
        response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        answer = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No response content')
        return answer
    except requests.RequestException as e:
        return f"Failed to make the request. Error: {e}"

@app.route('/')
def index():
    return 'Bot is running'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    if text == '/start':
        send_message(chat_id, "I am working")
    elif text.startswith('/ask'):
        query = text[len('/ask '):]
        answer = get_openai_response(query)
        send_message(chat_id, answer)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
