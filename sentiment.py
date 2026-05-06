from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("AIzaSyAnH1da3IlJvtRGRZ7l9eWwKxmvTTuclyM"))

def analyze_sentiment(text: str) -> str:
    prompt = f"""
Quyidagi matnning sentimentini aniqlang.
Faqat bitta so'z bilan javob bering: positive, negative yoki neutral.

Matn: {text}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    result = response.text.strip().lower()

    if "positive" in result:
        return "😊 Positive"
    elif "negative" in result:
        return "😔 Negative"
    else:
        return "😐 Neutral"