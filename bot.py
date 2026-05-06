import telebot
from telebot import types
from sentiment import analyze_sentiment
from youtube_api import get_video_id, get_comments
import os
from dotenv import load_dotenv
from pathlib import Path
import requests

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# VPN orqali ishlash uchun
session = requests.Session()
session.trust_env = False

bot = telebot.TeleBot(
    os.getenv("TELEGRAM_TOKEN"),
    threaded=False
)
print("🚀 Bot ishga tushdi!")

def log_message(user, text, result):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{user}: {text} -> {result}\n")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 YouTube tahlil", "✍️ Matn tahlil")
    markup.add("ℹ️ Help")
    bot.send_message(
        message.chat.id,
        "Salom! 🤖 Men sentiment botman!\n\n"
        "📊 *YouTube tahlil* — video URL yuboring\n"
        "✍️ *Matn tahlil* — istalgan matn yuboring\n"
        "ℹ️ *Help* — yordam",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_msg(message):
    bot.send_message(
        message.chat.id,
        "📌 *Qanday ishlatish:*\n\n"
        "1️⃣ *YouTube tahlil* tugmasini bosing\n"
        "2️⃣ YouTube video havolasini yuboring\n"
        "3️⃣ Bot izohlarni tahlil qilib natija beradi\n\n"
        "✍️ Yoki shunchaki matn yuboring!",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "📊 YouTube tahlil")
def youtube_mode(message):
    bot.send_message(message.chat.id, "🔗 YouTube video havolasini yuboring:")

@bot.message_handler(func=lambda m: m.text == "✍️ Matn tahlil")
def text_mode(message):
    bot.send_message(message.chat.id, "✍️ Tahlil qilmoqchi bo'lgan matningizni yuboring:")

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text
    username = message.from_user.username or "unknown"
    video_id = get_video_id(text)

    if video_id:
        msg = bot.send_message(message.chat.id, "⏳ Izohlar yuklanmoqda...")
        try:
            comments = get_comments(video_id, max_results=50)
            if not comments:
                bot.edit_message_text("❌ Izohlar topilmadi.", message.chat.id, msg.message_id)
                return
            bot.edit_message_text(
                f"🔍 {len(comments)} ta izoh tahlil qilinmoqda...",
                message.chat.id,
                msg.message_id
            )
            results = [analyze_sentiment(c) for c in comments]
            pos = results.count("😊 Positive")
            neg = results.count("😔 Negative")
            neu = results.count("😐 Neutral")
            total = len(results)
            reply = (
                f"📊 *Tahlil natijasi:*\n\n"
                f"😊 Positive: {pos} ({pos*100//total}%)\n"
                f"😔 Negative: {neg} ({neg*100//total}%)\n"
                f"😐 Neutral:  {neu} ({neu*100//total}%)\n\n"
                f"📝 Jami: {total} ta izoh"
            )
            bot.edit_message_text(
                reply,
                message.chat.id,
                msg.message_id,
                parse_mode="Markdown"
            )
            log_message(username, text, reply)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato: {str(e)}", message.chat.id, msg.message_id)
            print(f"❌ Xato: {e}")
    else:
        try:
            result = analyze_sentiment(text)
            bot.send_message(message.chat.id, f"Natija: {result}")
            log_message(username, text, result)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Xato: {str(e)}")
            print(f"❌ Xato: {e}")

bot.infinity_polling(timeout=60, long_polling_timeout=60)