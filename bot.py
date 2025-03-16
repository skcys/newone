import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your bot token here
TOKEN = os.getenv("AAGrtViOlLd51IHSEUknqEXLGb2KMNC2FaU")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a Facebook video URL, and I'll download it for you!")

def download_facebook_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "facebook.com" not in url:
        update.message.reply_text("Please send a valid Facebook video URL.")
        return

    update.message.reply_text("Downloading video, please wait...")

    # Set up yt_dlp options
    ydl_opts = {
        'outtmpl': 'facebook_video.mp4',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send the video to the user
        with open("facebook_video.mp4", "rb") as video:
            update.message.reply_video(video)

        os.remove("facebook_video.mp4")  # Clean up

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")
        logger.error(f"Error downloading video: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_facebook_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
