import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import platform

import mysql.connector as mc
import os
from dotenv import load_dotenv
from PIL import Image as ImagePIL
from datetime import date, datetime
import pandas as pd

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin App")  
        self.move(0,0)

        self.generalLayout = QGridLayout()
        # layout = QVBoxLayout()

        self.addUserButton = QPushButton("Add User")
        self.deleteUserButton = QPushButton("Delete User")
        self.editUserButton = QPushButton("Edit User")

        self.buttonGridLayout = QGridLayout()
        self.buttonGridLayout.addWidget(self.addUserButton, 0, 0)
        self.buttonGridLayout.addWidget(self.deleteUserButton, 0, 1)
        self.buttonGridLayout.addWidget(self.editUserButton, 0, 2)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Code"])

        # Bring back later:
        # header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.generalLayout.addLayout(self.buttonGridLayout, 0, 0)
        self.generalLayout.addWidget(self.tableWidget, 1, 0)

        self.setLayout(self.generalLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()    
    window.activateWindow()
    sys.exit(app.exec_())