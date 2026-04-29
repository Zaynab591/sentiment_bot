from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from sentiment import analyze_sentiment, generate_pro_reply

TOKEN = "8719431891:AAFyv8XeSo0XhuPegsBGpaPtjF4CE3svadI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Salom! Men professional kulgili AI botman.\n\nMenga yozing — men tahlil + hazil qilaman 😎"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    sentiment = analyze_sentiment(text)
    reply = generate_pro_reply(text, sentiment)

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🚀 Professional Funny AI Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()