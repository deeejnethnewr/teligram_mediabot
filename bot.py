import os
from pyrogram import Client, filters
from pytube import Playlist
import yt_dlp
from keep_alive import keep_alive
import shutil

API_ID = int(os.getenv("API_ID", "1234567"))  # Replace default with yours
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

app = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

keep_alive()  # Start the web server to keep Replit alive

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Hello! Send me a YouTube playlist, Google Drive, or Dailymotion link.")

@app.on_message(filters.text & filters.private)
async def downloader(client, message):
    url = message.text.strip()

    await message.reply("Starting download... please wait.")
    
    if "youtube.com/playlist" in url:
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                filename = video.streams.get_highest_resolution().download()
                await message.reply_video(filename)
                os.remove(filename)
        except Exception as e:
            await message.reply(f"Error downloading playlist: {e}")

    elif "drive.google.com" in url:
        try:
            # Use yt_dlp to download google drive links too
            ydl_opts = {"outtmpl": "./%(title)s.%(ext)s"}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl.prepare_filename(info)
                await message.reply_document(filename)
                os.remove(filename)
        except Exception as e:
            await message.reply(f"Error downloading Google Drive file: {e}")

    elif "dailymotion.com" in url:
        try:
            ydl_opts = {"outtmpl": "./%(title)s.%(ext)s"}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl.prepare_filename(info)
                await message.reply_video(filename)
                os.remove(filename)
        except Exception as e:
            await message.reply(f"Error downloading Dailymotion video: {e}")

    else:
        await message.reply("Please send a valid YouTube playlist, Google Drive, or Dailymotion link.")

app.run()
