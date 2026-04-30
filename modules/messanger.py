import requests
from modules.conf import App
from modules.logger import log


def send_telegram_birth_alert(text: str):
    app = App("conf/app.yaml")
    telegram_request_url = f"https://api.telegram.org/bot{app.telegram_token}/sendMessage"
    payload = {
        "chat_id": app.telegram_chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    log.info(f"Request to {telegram_request_url} with payload {payload}")

    response = requests.post(telegram_request_url, json=payload)
    result = response.json()

    log.info(f"Response from {telegram_request_url}: {result}")