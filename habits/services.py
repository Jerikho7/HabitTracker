import requests
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN


def send_telegram_notification(chat_id, message):
    """Функция отправки сообщения через телеграм-бота."""
    params = {"text": message, "chat_id": chat_id}

    try:
        response = requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params, timeout=5)
        response.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Ошибка при отправке в Telegram: {e}")
