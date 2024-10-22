import os
from dotenv import load_dotenv
import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from quart import Quart, jsonify, render_template, request
from db import init_db

load_dotenv()

app = Quart(__name__)

TOKEN = os.getenv('TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def save_to_db(name, email, phone, message, tg):
    async with aiosqlite.connect('form_data.db') as db:
        await db.execute('''
            INSERT INTO form_submissions (name, email, phone, message, tg)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, message, tg))
        await db.commit()

async def send_message(text):
    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer("Привет, как только придёт сообщения с сайта я отправлю его сюда, в группу!")

@app.route('/submit-form', methods=['POST'])
async def submit_form():
    data = await request.form
    name = data['name']
    email = data['email']
    phone = data['phone']
    message = data['message']
    tg = data['tg'] if 'tg' in data else ''  # Задаем значение по умолчанию, если tg отсутствует

    if not tg:  # Проверяем, если tg пустое, можно вернуть ошибку
        return jsonify({"status": "error", "message": "Поле Telegram не может быть пустым!"}), 400

    await save_to_db(name, email, phone, message, tg)

    text = f"Получено новое сообщение с сайта:\n\n" \
           f"Имя: {name}\n" \
           f"Почта: {email}\n" \
           f"Телефон: {phone}\n" \
           f"Сообщение: {message}\n" \
           f"Телеграм: {tg}"

    await send_message(text)

    return jsonify({"status": "success", "message": "Форма успешно отправлена!"})

@app.route('/')
async def index():
    return await render_template('index.html')

async def run_bot():
    await dp.start_polling()

async def main():
    bot_task = asyncio.create_task(run_bot())
    quart_task = asyncio.create_task(app.run_task())
    await asyncio.gather(bot_task, quart_task)

if __name__ == "__main__":
    init_db()
    asyncio.run(main())
