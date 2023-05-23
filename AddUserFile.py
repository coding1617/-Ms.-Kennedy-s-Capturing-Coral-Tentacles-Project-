from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from datetime import date

import string
import random 

# https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/ 

class AddUserFile(QWidget):
    submitButton = None
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add User") 
        icon_pixmap = QPixmap("Actual Final Logo.png")
        self.setWindowIcon(QIcon(icon_pixmap)) 

        layout = QGridLayout()
        
        self.name_of_person_Label = QLabel("Name:")
        self.name_of_person_Display = QLineEdit()
        self.name_of_person_Display.setPlaceholderText("Enter the name here")
        
        self.code_Label = QLabel("Code:")
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
        self.actual_code_Label = QLabel(res)
        
        self.submitButton = None
        self.submitButton = QPushButton("Submit")
        self.submit_shortcut = QShortcut(Qt.Key_Return, self)
        
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)
        
        layout.addWidget(self.name_of_person_Label, 0, 0)
        layout.addWidget(self.name_of_person_Display, 0, 1)
        layout.addWidget(self.code_Label, 1, 0)
        layout.addWidget(self.actual_code_Label, 1, 1)
        layout.addWidget(self.submitButton, 2, 0)
        
        # print(self.name_of_person_Display.text())
        
        self.setLayout(layout)

        self.setStyleSheet(
            "QLabel {"
            " color: #00adb5;"
            " font-family: 'Lucida Sans Typewriter';"
            # " font-size: 15px;"
            " font-size: 17px;"
            " font-weight: bold;"
            "}"

            "QPushButton {"
            " color: white;"
            " background-color: #3f72af;"
            " font-family: 'Lucida Sans Typewriter';"
            # " font-size: 15px;"
            " font-size: 17px;"
            " font-weight: bold;"
            " border-radius: 10px;"
            " padding: 10px 20px;"
            "}"

            "QPushButton:hover {"
            " background-color: #00adb5;"
            "}"

            "QLineEdit {"
            # " font-size: 15px;"
            " font-size: 17px;"
            " font-family: 'Lucida Sans Typewriter';"
            "}"

        )
 
    def get_user_name(self):
        return self.name_of_person_Display.text()
    
    def get_code(self):
        return self.actual_code_Label.text()