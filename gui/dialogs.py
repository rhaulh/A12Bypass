# gui/dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class CustomMessageBox(QDialog):
    def __init__(self, title, message, serial_number, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(450, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)
        QLabel(title, self, alignment=Qt.AlignCenter, styleSheet="font-size:20px; font-weight:bold; color:#27ae60").addTo(layout)
        QLabel(message, self, alignment=Qt.AlignCenter).addTo(layout)

        serial_label = QLabel(f"Serial: {serial_number}", self, alignment=Qt.AlignCenter,
                              styleSheet="font-size:16px; font-weight:bold; color:#e74c3c; background:#fdf2f2; padding:10px; border:2px solid #e74c3c; border-radius:5px")
        layout.addWidget(serial_label)

        btn_layout = QHBoxLayout()
        QPushButton("Cancel", clicked=self.reject, styleSheet="background:#95a5a6;color:white;padding:10px 20px").addTo(btn_layout)
        QPushButton("Proceed to Order", clicked=self.accept, styleSheet="background:#27ae60;color:white;padding:10px 20px").addTo(btn_layout)
        layout.addLayout(btn_layout)

class ActivationResultDialog(QDialog):
    def __init__(self, title, message, is_success=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 350)
        self.setModal(True)

        layout = QVBoxLayout(self)
        color = "#27ae60" if is_success else "#e74c3c"
        QLabel(title, self, alignment=Qt.AlignCenter, styleSheet=f"font-size:24px; font-weight:bold; color:{color}").addTo(layout)
        QLabel(message, self, alignment=Qt.AlignCenter, styleSheet="background:#f8f9fa;padding:15px;border:1px solid #ddd;border-radius:8px").addTo(layout)

        btn = QPushButton("OK", clicked=self.accept, styleSheet="background:#3498db;color:white;padding:12px 30px")
        h = QHBoxLayout(); h.addStretch(); h.addWidget(btn); h.addStretch()
        layout.addLayout(h)