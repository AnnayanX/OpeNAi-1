from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}"
CHAT_ID = os.getenv('CHAT_ID')

@app.route('/')
def index():
    user_ip = request.remote_addr
    send_telegram_message(CHAT_ID, f'New visitor from IP: {user_ip}')
    return 'Message sent to @Dhanrakshak with IP address.'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')

    if text == '/start':
        send_telegram_message(chat_id, 'I am working')
    
    return jsonify({'status': 'ok'})

def send_telegram_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
