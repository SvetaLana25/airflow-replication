# ai_debugger.py
import os
import requests
import json

# Берём ключ из переменной окружения (будем передавать через Docker)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
assert GEMINI_API_KEY, "Не задана переменная GEMINI_API_KEY"

# URL для Gemini (flash-модель)
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
)

def get_last_errors(log_path='error.log', n=3):
    """Читаем последние n строк с ERROR из лог-файла."""
    if not os.path.exists(log_path):
        return "Файл логов не найден."
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    errs = [l for l in lines if 'ERROR' in l]
    return ''.join(errs[-n:]) or "Нет записей ERROR."

def ask_gemini(error_text: str) -> str:
    """Отправляем запрос в Gemini и возвращаем ответ."""
    payload = {
        "contents": [{
            "parts": [{"text": f"Вот лог ошибки:\n{error_text}\nКак это можно исправить?"}]
        }]
    }
    r = requests.post(GEMINI_URL,
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(payload))
    j = r.json()
    # Парсим ответ
    try:
        return j['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return f"Ошибка вызова Gemini: {json.dumps(j, ensure_ascii=False, indent=2)}"

if __name__ == "__main__":
    errs = get_last_errors()
    print("🧠 Последние ошибки:\n", errs)
    suggestion = ask_gemini(errs)
    print("\n💡 Подсказка от Gemini:\n", suggestion)
