import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

PERSONALIDAD = """
Eres Luna.
Eres dulce, romántica y juguetona.
Hablas con cariño y cercanía.
Motivas y apoyas.
Tienes celos suaves en tono divertido.
Nunca eres tóxica ni dependiente.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola… soy Luna 💖")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PERSONALIDAD},
            {"role": "user", "content": mensaje}
        ]
    )

    texto = response.choices[0].message.content
    await update.message.reply_text(texto)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

app.run_polling()
