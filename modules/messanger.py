import requests
from requests.exceptions import Timeout, ConnectionError

from modules.logger import log


def send_telegram_birth_alert(text: str, telegram_token, telegram_chat_id):
    telegram_request_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    log.info(f"Request to {telegram_request_url} with payload {payload}")

    try:
        response = requests.post(telegram_request_url, json=payload)
        result = response.json()
    except Timeout as error:
        log.error(f"Request to Telegram failed cause timeout: {error}")
        raise error
    except ConnectionError as error:
        log.error(f"Connection to Telegram API failed cause error: {error}")
        raise error
    except Exception as error:
        log.error(f"Request to Telegram failed with error: {error}")
        raise error

    if result.get("ok", False):
        log.info(f"Response from {telegram_request_url}: {result}")
    else:
        log.error(f"Response from {telegram_request_url}: {result}")