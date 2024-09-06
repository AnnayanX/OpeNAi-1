from flask import Flask, request, jsonify, send_from_directory
from telegram import Update, Bot
import os
import requests

app = Flask(__name__)

# Access environment variables
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

bot = Bot(token=TELEGRAM_API_TOKEN)

def send_ip_to_user(ip_address):
    message = f"New visitor with IP: {ip_address}"
    bot.send_message(chat_id=CHAT_ID, text=message)

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
    return send_from_directory('static', 'index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    chat_id = update.message.chat_id
    if update.message.text == '/start':
        bot.send_message(chat_id=chat_id, text="I am working")
    elif update.message.text.startswith('/ask'):
        query = update.message.text[len('/ask '):]
        answer = get_openai_response(query)
        bot.send_message(chat_id=chat_id, text=answer)
    return jsonify(success=True)

@app.route('/notify_ip', methods=['POST'])
def notify_ip():
    ip_address = request.remote_addr
    send_ip_to_user(ip_address)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
