# security/monitor.py
import os
import time
import inspect
import threading
import ctypes
import winreg
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

DETECTED_THREATS = []

class SecurityMonitor:
    def __init__(self):
        self.suspicious_activities = []
        self.start_time = time.time()

    def check_code_injection(self):
        try:
            frames = inspect.stack()
            for frame in frames:
                if any(k in str(frame.code_context) for k in ['eval', 'exec', 'compile', '__import__']):
                    self.log_threat("Potential code injection", frame)
                    return True
        except: pass
        return False

    def check_api_sniffing(self):
        try:
            current = inspect.currentframe()
            for frame_info in inspect.getouterframes(current):
                for var_value in frame_info.frame.f_locals.values():
                    if TELEGRAM_BOT_TOKEN in str(var_value):
                        self.log_threat("Unauthorized token access", frame_info)
                        return True
        except: pass
        return False

    def check_proxy_usage(self):
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        for var in proxy_vars:
            if os.environ.get(var):
                self.log_threat(f"Proxy env var: {var}", None)
                return True
        if os.name == 'nt':
            try:
                key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                                   r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
                if winreg.QueryValueEx(key, "ProxyEnable")[0]:
                    self.log_threat("Windows proxy enabled", None)
                    return True
            except: pass
        return False

    def log_threat(self, message, frame_info):
        threat = {'message': message, 'timestamp': time.time(), 'frame': str(frame_info)}
        DETECTED_THREATS.append(threat)
        self.send_security_alert(threat)
        self.protective_action()

    def send_security_alert(self, threat_info):
        try:
            msg = f"SECURITY ALERT\nThreat: {threat_info['message']}\nTime: {time.ctime(threat_info['timestamp'])}"
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg}, timeout=10)
        except: pass

    def protective_action(self):
        print("SECURITY THREAT - EXITING")
        os._exit(1)

    def continuous_monitoring(self):
        while True:
            if self.check_code_injection() or self.check_api_sniffing() or self.check_proxy_usage():
                break
            time.sleep(5)

security_monitor = SecurityMonitor()

def start_security_thread():
    t = threading.Thread(target=security_monitor.continuous_monitoring, daemon=True)
    t.start()

def anti_debug():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            os._exit(1)
    except: pass