import os
import subprocess
import logging
from ai_debugger import ask_gemini  # уже должен быть в проекте

logging.basicConfig(
    filename='deploy.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def summarize_readme(readme_path="README.md"):
    if not os.path.exists(readme_path):
        return "README.md not found"
    with open(readme_path, "r", encoding="utf-8") as f:
        return ask_gemini("Проанализируй описание проекта:\n" + f.read())

def analyze_structure():
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            if ".git" not in root:
                files.append(os.path.join(root, f))
    structure = "\n".join(files[:100])
    return ask_gemini("Вот структура проекта:\n" + structure)

def run_tests():
    result = subprocess.run(["pytest", "app/test_app.py"], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("✅ Тесты прошли успешно.")
    else:
        logging.error("❌ Ошибка при выполнении тестов:\n%s", result.stderr)
    return result

def deploy():
    try:
        result = subprocess.run(["docker-compose", "up", "--build", "-d"],
                                capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            logging.info("✅ Деплой успешно выполнен.")
        else:
            logging.error("❌ Ошибка при деплое:\n%s", result.stderr)
            logging.info("💡 Подсказка от Gemini:")
            logging.info(ask_gemini(result.stderr))
    except Exception as e:
        logging.error("❌ Исключение при деплое: %s", str(e))

if __name__ == "__main__":
    logging.info("🔍 Анализ README.md:")
    logging.info(summarize_readme())

    logging.info("📁 Анализ структуры проекта:")
    logging.info(analyze_structure())

    logging.info("🧪 Запуск тестов:")
    run_tests()

    logging.info("🚀 Запуск деплоя:")
    deploy()
