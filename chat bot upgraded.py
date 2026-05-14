import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8726421843:AAGq9mUvOcIOiFMuyGFiNQ__SWiEglgaj8I"
GROQ_API_KEY = "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"

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

    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, chat))

print("Groq AI Chat Bot Running...")
app.run_polling()