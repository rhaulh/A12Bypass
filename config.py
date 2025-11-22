# config.py
TELEGRAM_BOT_TOKEN = "8410516214:AAGGiXuKLBw5Qd-UxfUHx1fdeQauBTsi-LI"
TELEGRAM_CHAT_ID = "918985092"

# Base URL
BASE_API_URL = "https://boletikapp.com/a12/"

# Enpoints
MODEL_URL = "checkModel.php?model="
AUTH_URL = "checkAuthorized.php?model="
SQL_URL = "getSqlite.php?model="
PAYLOAD_URL = "/getPayload.php?guid="

# Endpoints with parameters
CHECK_MODEL_URL = f"{BASE_API_URL}{MODEL_URL}"
CHECK_AUTH_URL = f"{BASE_API_URL}{AUTH_URL}"
GET_SQLITE_URL = f"{BASE_API_URL}{SQL_URL}"




CONTACT_URL = "https://fb.com/rhaulh"