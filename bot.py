import os
import telebot
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PROXY_API_KEY = os.getenv('PROXY_API_KEY')
BASE_URL = "https://api.proxyapi.ru/openai/v1/chat/completions"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_chat_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PROXY_API_KEY}"
    }
    data = {
        "model": "gpt-4-turbo",  # Изменено на gpt-4-turbo
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(BASE_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Ошибка API: {response.status_code} - {response.text}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    bot.reply_to(message, "Обрабатываю...")
    try:
        openai_response = get_chat_response(user_message)
        bot.send_message(message.chat.id, openai_response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен и ожидает сообщений...")
    bot.polling()