import asyncio
import logging
import json
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "ТВОЙ_ТОКЕН_БОТА"  # Вставьте сюда токен бота
WEB_APP_URL = "https://tennis-bangtao.vercel.app"  # Ваша ссылка на Vercel

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ SQLite ---
def init_db():
    conn = sqlite3.connect("tennis.db")
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    ''')
    
    # Таблица матчей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            location TEXT,
            max_players INTEGER DEFAULT 4,
            score TEXT DEFAULT NULL,
            status TEXT DEFAULT 'open'
        )
    ''')
    
    # Записи на матчи
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            match_id INTEGER,
            user_id INTEGER,
            PRIMARY KEY (match_id, user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# --- ОБРАБОТЧИКИ ТЕЛЕГРАМ ---
@dp.message(CommandStart())
async def start(message: types.Message):
    # Сохраняем пользователя
    conn = sqlite3.connect("tennis.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)",
        (message.from_user.id, message.from_user.full_name, message.from_user.username)
    )
    conn.commit()
    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🎾 Открыть Tennis Club", web_app=WebAppInfo(url=WEB_APP_URL))
    ]])
    
    await message.answer(f"Привет, {message.from_user.first_name}! Добро пожаловать в Bangtao Tennis Club.", reply_markup=kb)

# Обработка действий из Mini App (web_app_data)
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    action = data.get("action")
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    conn = sqlite3.connect("tennis.db")
    cursor = conn.cursor()

    if action == "create_match":
        cursor.execute(
            "INSERT INTO matches (datetime, location, max_players) VALUES (?, ?, ?)",
            (data["datetime"], data["location"], data["max_players"])
        )
        conn.commit()
        await message.answer(f"✅ Новый матч создан!\n📅 {data['datetime']}\n📍 {data['location']}")

    elif action == "join":
        match_id = data["match_id"]
        cursor.execute("INSERT OR IGNORE INTO registrations (match_id, user_id) VALUES (?, ?)", (match_id, user_id))
        conn.commit()
        await message.answer(f"🎾 {user_name}, вы успешно записались на матч!")

    elif action == "set_score":
        match_id = data["match_id"]
        score = data["score"]
        cursor.execute("UPDATE matches SET score = ?, status = 'finished' WHERE id = ?", (score, match_id))
        conn.commit()
        await message.answer(f"🏆 Счет матча #{match_id} сохранен: {score}")

    conn.close()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
