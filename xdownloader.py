import os
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set. Set BOT_TOKEN sebelum menjalankan.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Kirim link video Twitter/X atau TikTok — saya akan mengunduh kualitas terbaik tanpa limit."
    )

async def analyze_and_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("Memproses... mengambil kualitas terbaik tanpa limit...")

    try:
        ydl_opts = {
            "format": "bestvideo*+bestaudio/best",
            "outtmpl": "video_no_limit.%(ext)s",
            "merge_output_format": "mp4",
            "socket_timeout": 30,
            "retries": 20,
            "fragment_retries": 20,
            "skip_unavailable_fragments": True,
            "no_warnings": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            final_name = "video_no_limit.mp4"
            if not filename.endswith(".mp4"):
                os.rename(filename, final_name)
            else:
                final_name = filename

        await update.message.reply_video(video=open(final_name, "rb"))
        os.remove(final_name)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_and_download))
    app.run_polling()

if __name__ == "__main__":
    main()
