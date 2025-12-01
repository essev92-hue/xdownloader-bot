import os
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes
)

BOT_TOKEN = os.getenv("8590724019:AAFG4moTxBjOOj3wUXvPRg5vYbBb582lPRM")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable tidak ditemukan. Tambahkan BOT_TOKEN di Railway Variables.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Kirimkan link video dari:\n"
        "- Twitter / X\n"
        - TikTok (tanpa watermark)\n"
        "- YouTube\n"
        "- Facebook\n"
        "- Instagram\n\n"
        "Saya akan mengunduh kualitas terbaik otomatis."
    )

async def process_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("Sedang mengambil kualitas terbaik...")

    try:
        # TikTok no-watermark fix
        if "tiktok.com" in url:
            ydl_opts = {
                "format": "bestvideo*+bestaudio/best",
                "outtmpl": "video_best.%(ext)s",
                "merge_output_format": "mp4",
                "socket_timeout": 30,
                "retries": 20,
                "fragment_retries": 20,
                "skip_unavailable_fragments": True,
                "no_warnings": True,
                "postprocessors": [{
                    "key": "ModifyChapters",
                    "remove_sponsor_segments": ["all"]
                }],
                "params": {"extractor_args": {"tiktok": {"noprogress": [""]}}},
            }
        else:
            # General downloader untuk semua platform
            ydl_opts = {
                "format": "bestvideo*+bestaudio/best",
                "outtmpl": "video_best.%(ext)s",
                "merge_output_format": "mp4",
                "socket_timeout": 30,
                "retries": 20,
                "fragment_retries": 20,
                "skip_unavailable_fragments": True,
                "no_warnings": True
            }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # pastikan .mp4
            final_file = "video_final.mp4"
            if not filename.endswith(".mp4"):
                os.rename(filename, final_file)
            else:
                final_file = filename

        await update.message.reply_video(video=open(final_file, "rb"))
        os.remove(final_file)

    except Exception as e:
        await update.message.reply_text(f"Terjadi error:\n{e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_video))
    app.run_polling()

if __name__ == "__main__":
    main()
