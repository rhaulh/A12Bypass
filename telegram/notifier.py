# telegram/notifier.py
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from security.monitor import security_monitor

class TelegramNotifier:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

    def send_message(self, text):
        if security_monitor.check_proxy_usage():
            return False
        try:
            r = requests.post(f"{self.base_url}/sendMessage",
                              data={'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML'}, timeout=10)
            return r.status_code == 200
        except:
            return False

    def send_activation_success(self, model, serial, imei):
        msg = f"DEVICE ACTIVATED SUCCESSFULLY\nModel: {model}\nSerial: {serial}\nIMEI: {imei}"
        return self.send_message(msg)

    def send_activation_failed(self, model, serial, imei, reason):
        msg = f"DEVICE ACTIVATION FAILED\nModel: {model}\nSerial: {serial}\nIMEI: {imei}\nReason: {reason}"
        return self.send_message(msg)

telegram_notifier = TelegramNotifier()