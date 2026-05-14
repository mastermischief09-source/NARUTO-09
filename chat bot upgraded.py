import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from flask import Flask
from threading import Thread
import os

# =========================
# KEEP RENDER WEB SERVICE ALIVE
# =========================

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =========================
# TOKENS
# =========================

BOT_TOKEN = os.getenv("Bot_Token")
GROQ_API_KEY = os.getenv("Groq_API")

# =========================
# CHAT FUNCTION
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",

        "messages": [
            {
                "role": "system",
                "content": "Reply naturally and casually like a normal human conversation."
            },

            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
        else:
            bot_reply = f"API Error 😢\n{result}"

    except Exception as e:
        bot_reply = f"Error 😢\n{e}"

    await update.message.reply_text(bot_reply)

# =========================
# START BOT
# =========================

print("Groq AI Chat Bot Running...")

app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

app_bot.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

app_bot.run_polling()