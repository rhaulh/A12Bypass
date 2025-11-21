# main.py
import sys
from PyQt5.QtWidgets import QApplication
from core.detector import DeviceDetector
from utils.helpers import hide_console

if __name__ == "__main__":
    hide_console()
    app = QApplication(sys.argv)
    app.setApplicationName("Cybercity A12 Bypass")
    window = DeviceDetector()
    window.show()
    sys.exit(app.exec_())