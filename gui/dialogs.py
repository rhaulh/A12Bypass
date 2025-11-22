from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class CustomMessageBox(QDialog):
    def __init__(self, title, message, serial_number, parent=None):
        super().__init__(parent)

        uic.loadUi("gui/custom_message_box.ui", self)

        # Set data
        self.labelTitle.setText(title)
        self.labelMessage.setText(message)
        self.labelSerial.setText(f"Serial: {serial_number}")

        # Connect buttons
        self.btnCancel.clicked.connect(self.reject)
        self.btnProceed.clicked.connect(self.accept)

class ActivationResultDialog(QDialog):
    def __init__(self, title, message, is_success=True, parent=None):
        super().__init__(parent)

        uic.loadUi("gui/activation_result_dialog.ui", self)

        # Set fields
        self.labelTitle.setText(title)
        self.labelMessage.setText(message)

        # Success or failure color
        if is_success:
            self.labelTitle.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #27ae60;
                margin-bottom: 20px;
            """)
            self.labelInfo.setVisible(False)
        else:
            self.labelTitle.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #e74c3c;
                margin-bottom: 20px;
            """)
            self.labelInfo.setVisible(True)

        # Connect button
        self.btnOk.clicked.connect(self.accept)
