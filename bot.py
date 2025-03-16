import os
import yt_dlp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is missing.")
    exit(1)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 Hi! Send me a Facebook video URL, and I'll download it for you!")

@dp.message()
async def download_fb_video(message: types.Message):
    url = message.text
    chat_id = message.chat.id

    if "facebook.com" not in url:
        await message.answer("❌ Please send a valid Facebook video URL.")
        return

    await message.answer("🔄 Downloading video... Please wait.")

    try:
        ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send the video to the user
        video = FSInputFile("video.mp4")
        await bot.send_video(chat_id, video)

        # Delete the file after sending
        os.remove("video.mp4")

    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")

async def main():
    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
