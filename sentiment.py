import random

def analyze_sentiment(text: str) -> str:
    text = text.lower()

    positive = ["zo'r", "yaxshi", "super", "ajoyib", "👍", "🔥", "😍"]
    negative = ["yomon", "xafa", "norozi", "😭", "😡", "👎", "qiyin"]

    score = 0

    for w in positive:
        if w in text:
            score += 1

    for w in negative:
        if w in text:
            score -= 1

    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"


def generate_pro_reply(text: str, sentiment: str) -> str:

    if sentiment == "positive":
        jokes = [
            "😎 Bu energiya bilan siz WiFi signalni ham kuchaytirasiz 😂",
            "🔥 Server ham sizni ko‘rib motivatsiya oldi 🚀",
            "😂 Bu pozitivlik bilan siz TikTok algoritmini ham yutib yuborasiz"
        ]

        return f"""📊 Sentiment: Positive

🧠 Tahlil: foydalanuvchi yaxshi kayfiyatda

😂 AI fikri: {random.choice(jokes)}"""

    elif sentiment == "negative":
        jokes = [
            "😭 Hayot bugun ham ‘update failed’ dedi",
            "💀 System log: motivation.exe crashed",
            "😂 Bu holatda hatto calculator ham chalkashib qoladi"
        ]

        return f"""📊 Sentiment: Negative

🧠 Tahlil: stress yoki norozilik aniqlandi

😂 AI fikri: {random.choice(jokes)}"""

    else:
        jokes = [
            "🤖 Neytral kayfiyat — AI ham dam olyapti",
            "😐 Hech narsa aniq emas, lekin analiz davom etyapti",
            "😂 Bu gapni hatto Google ham 3 marta o‘ylab ko‘radi"
        ]

        return f"""📊 Sentiment: Neutral

🧠 Tahlil: aniq hissiyot yo‘q

😂 AI fikri: {random.choice(jokes)}"""