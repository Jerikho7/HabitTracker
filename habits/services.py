import requests
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN


def send_telegram_notification(chat_id, message):
    """Функция отправки сообщения через телеграм-бота."""
    params = {"text": message, "chat_id": chat_id}

    response = requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to send telegram message: {response.text}")
