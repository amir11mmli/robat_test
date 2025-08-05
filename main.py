import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberStatus
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PHOTO_FILE_ID = os.getenv("PHOTO_FILE_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
            sent = await message.answer_photo(PHOTO_FILE_ID, caption="✅ خوش اومدی به خانواده NoTrace 👻")
            await asyncio.sleep(30)
            await bot.delete_message(message.chat.id, sent.message_id)
        else:
            await message.answer("❗️برای ادامه، اول عضو کانال @NoTrace_1 شو.")
    except Exception:
        await message.answer("⚠️ خطا در بررسی عضویت یا اتصال به سرور.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)