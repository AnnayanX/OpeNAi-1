from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Access environment variables
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '7282854458:AAEgIt3OigoszFAFGnrYcnvJbIlRbDN9E4I')
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
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'query': query
    }
    response = requests.post(f'{OPENAI_ENDPOINT}/v1/query', headers=headers, json=data)
    return response.json().get('answer', 'No answer found.')

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
