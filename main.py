import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PHOTO_FILE_ID = os.getenv("PHOTO_FILE_ID")

if not all([BOT_TOKEN, CHANNEL_ID, PHOTO_FILE_ID]):
    raise ValueError("❌ لطفاً BOT_TOKEN، CHANNEL_ID و PHOTO_FILE_ID را در env تنظیم کن.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status != "left":
            sent_msg = await message.answer_photo(PHOTO_FILE_ID)
            await asyncio.sleep(30)
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=sent_msg.message_id)
            except Exception as e:
                print(f"خطا در حذف پیام: {e}")
        else:
            await message.reply("❌ لطفاً اول عضو کانال بشو تا بتونم ادامه بدم.")
    except Exception as e:
        await message.reply("⚠️ خطا در بررسی عضویت. لطفاً بعداً امتحان کن.")
        print(f"Error checking membership: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
