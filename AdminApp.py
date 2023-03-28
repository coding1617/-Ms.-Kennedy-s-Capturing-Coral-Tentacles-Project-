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
        layout = QVBoxLayout()
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()    
    window.activateWindow()
    sys.exit(app.exec_())