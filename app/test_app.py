# app/test_app.py
import os

def test_bot_token():
    token = os.getenv("BOT_TOKEN")
    assert token and token.startswith("77"), "❌ BOT_TOKEN не задан или некорректен"
    print("✅ BOT_TOKEN проверен и валиден.")

if __name__ == "__main__":
    test_bot_token()
