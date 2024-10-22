import os

from dotenv import load_dotenv
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from quart import Quart, jsonify, render_template, request
from db import init_db

load_dotenv()

# Quart (аналог Flask)
app = Quart(__name__)


# Telegram Bot токен
TOKEN = os.getenv('TOKEN')
USER_CHAT_ID = os.getenv('USER_CHAT_ID')  # Используйте реальный chat_id, полученный через команду /start

# Настройка бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


# Подключение к базе данных SQLite
def save_to_db(name, email, phone, message):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    # Вставляем данные формы в таблицу
    cursor.execute('''
        INSERT INTO form_submissions (name, email, phone, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, message))

    conn.commit()
    conn.close()


# Асинхронная функция для отправки сообщения пользователю
async def send_message(text):
    try:
        await bot.send_message(chat_id=os.getenv('USER_CHAT_ID'), text=text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer("Привет! Теперь я могу отправлять тебе сообщения.")
    print(f"Chat ID пользователя {message.from_user.username}: {message.chat.id}")


# Quart маршрут для обработки формы
@app.route('/submit-form', methods=['POST'])
async def submit_form():
    data = await request.form  # Получаем данные формы
    name = data['name']
    email = data['email']
    phone = data['phone']
    message = data['message']
    tg = data['tg']

    # Сохраняем данные в базу данных
    save_to_db(name, email, phone, message)

    # Формируем текст сообщения для отправки в бота
    text = f"Получено новое сообщение с сайта:\n\n" \
           f"Имя: {name}\n" \
           f"Почта: {email}\n" \
           f"Телефон: {phone}\n" \
           f"Сообщение: {message}\n" \
           f"Телеграм: {tg}"

    # Отправляем сообщение в Telegram
    await send_message(text)

    return jsonify({"status": "success", "message": "Форма успешно отправлена!"})


# Quart маршрут для отображения HTML
@app.route('/')
async def index():
    return await render_template('index.html')


# Запуск Telegram бота
async def run_bot():
    await dp.start_polling()


# Основной асинхронный запуск Quart и бота
async def main():
    bot_task = asyncio.create_task(run_bot())  # Запускаем бота в отдельной задаче
    quart_task = asyncio.create_task(app.run_task())  # Запускаем Quart сервер
    await asyncio.gather(bot_task, quart_task)


if __name__ == "__main__":

    # Инициализация базы данных
    init_db()

    asyncio.run(main())
