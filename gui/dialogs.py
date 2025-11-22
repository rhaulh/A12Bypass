# gui/dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class CustomMessageBox(QDialog):
    def __init__(self, title, message, serial_number, parent=None):
        super().__init__(parent)
        self.serial_number = serial_number
        self.setWindowTitle(title)
        self.setFixedSize(450, 300)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #27ae60;
            margin-bottom: 15px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 14px;
            color: #2c3e50;
            margin-bottom: 20px;
            padding: 10px;
        """)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)
        
        # Serial Number highlight
        serial_label = QLabel(f"Serial: {self.serial_number}")
        serial_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #e74c3c;
            background-color: #fdf2f2;
            padding: 10px;
            border: 2px solid #e74c3c;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        serial_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(serial_label)
        
        # Info text
        info_text = QLabel("Click 'Proceed to Order' to continue with the activation process")
        info_text.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 20px;
        """)
        info_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.proceed_btn = QPushButton("Proceed to Order")
        self.proceed_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.proceed_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.proceed_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class ActivationResultDialog(QDialog):
    def __init__(self, title, message, is_success=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 350)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout()
        
        # Icon and Title
        title_label = QLabel(title)
        if is_success:
            title_label.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                color: #27ae60;
                margin-bottom: 20px;
            """)
        else:
            title_label.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                color: #e74c3c;
                margin-bottom: 20px;
            """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 16px;
            color: #2c3e50;
            margin-bottom: 30px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #ddd;
        """)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)
        
        # Additional info for failure
        if not is_success:
            info_label = QLabel("This is a normal process. All you need to do is try again multiple times for your device to activate.")
            info_label.setStyleSheet("""
                font-size: 14px;
                color: #7f8c8d;
                font-style: italic;
                margin-bottom: 20px;
                padding: 10px;
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
            """)
            info_label.setWordWrap(True)
            info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label)
        
        # OK Button
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
