import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

BOT_TOKEN = "8629786380:AAFNsaF3kf9jTXDk3OYHnF9cmNQK88psi-c"
WEBAPP_URL = "https://tennis-bangtao.vercel.app/" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎾 Открыть Теннис Клуб", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("Добро пожаловать в теннисный клуб!", reply_markup=kb)

@dp.message(lambda msg: msg.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user_name = message.from_user.first_name
    
    if data.get("action") == "join":
        await message.answer(f"✅ Игрок **{user_name}** записался на матч!", parse_mode="Markdown")
    elif data.get("action") == "leave":
        await message.answer(f"❌ Игрок **{user_name}** отменил запись.", parse_mode="Markdown")
    elif data.get("action") == "set_score":
        score = data.get("score")
        await message.answer(f"🏆 **{user_name}** внес счет матча: `{score}`", parse_mode="Markdown")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
