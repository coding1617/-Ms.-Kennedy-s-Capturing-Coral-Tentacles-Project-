import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import platform

import string
import random 

import mysql.connector as mc
import os
from dotenv import load_dotenv
from PIL import Image as ImagePIL
from datetime import date, datetime
import pandas as pd

from AddUserFile import AddUserFile

from basic_styling import *
from connectToDatabase import *
from config import *

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin App") 
        icon_pixmap = QPixmap("Actual Final Logo.png")
        self.setWindowIcon(QIcon(icon_pixmap)) 
        self.move(0,0)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QColor(66, 22, 161))  
        self.setPalette(palette)

        self.generalLayout = QGridLayout()

        self.addUserButton = QPushButton("Add User")
        self.addUserButton.clicked.connect(self.recordInfo)
        self.addUserButton.setFixedWidth(300)
        self.deleteUserButton = QPushButton("Delete User")
        self.deleteUserButton.clicked.connect(self.deleteRow)
        self.deleteUserButton.setFixedWidth(300)
        self.changeAdminCodeButton = QPushButton("Change Admin Code")
        self.changeAdminCodeButton.clicked.connect(self.changeAdminCode)
        self.changeAdminCodeButton.setFixedWidth(300)
        
        self.buttonGridLayout = QGridLayout()
        self.buttonGridLayout.addWidget(self.addUserButton, 0, 0)
        self.buttonGridLayout.addWidget(self.deleteUserButton, 0, 1)
        self.buttonGridLayout.addWidget(self.changeAdminCodeButton, 0, 2)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Code"])
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setStyleSheet(
            "border: 1px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
            " font-family: 'Lucida Sans Typewriter';"
        )
        
        self.adminName_Label = QLabel()
        self.adminCode_Label = QLabel()
        self.adminCode_Label.setStyleSheet(
            " margin-left: 10px;"
        )
        
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.export)
        
        self.buttonGridLayout.addWidget(self.adminName_Label, 1, 0)
        self.buttonGridLayout.addWidget(self.adminCode_Label, 1, 1)

        self.generalLayout.addLayout(self.buttonGridLayout, 0, 0)
        self.generalLayout.addWidget(self.tableWidget, 1, 0)
        self.generalLayout.addWidget(self.exportButton, 2, 0)

        # Shortcuts
        self.delete_shortcut = QShortcut(Qt.Key_Delete, self)
        self.delete_shortcut.activated.connect(self.deleteRow)

        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.quit_shortcut.activated.connect(self.close)
        

        self.setLayout(self.generalLayout)
        
        load_dotenv('config.env')
        self.DBConnect()

        self.setStyleSheet(
            "QLabel {"
            " color: #00adb5;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 17px;"
            " font-weight: bold;"
            "}"

            "QPushButton {"
            " color: white;"
            " background-color: #3f72af;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 17px;"
            " font-weight: bold;"
            " border-radius: 15px;"
            " padding: 10px 20px;"
            " margin: 10px;"
            "}"

            "QPushButton:hover {"
            " background-color: #00adb5;"
            "}"

            "QLineEdit {"
            " font-size: 17px;"
            " font-family: 'Lucida Sans Typewriter';"
            "}"
        )
        
    def DBConnect(self):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute("SELECT users_name FROM users WHERE users_name = '%s'" % getAdmin())
            myresult = mycursor.fetchall()
            userName = ''.join(myresult[0])
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % getAdmin())
            myresult2 = mycursor.fetchall()
            code = ''.join(myresult2[0])
            
            self.adminCode_Label.clear()
            self.adminName_Label.setText("Username: %s" % userName)
            self.adminCode_Label.setText("Code: %s" % code)
            
            mycursor.execute("SELECT * FROM users")

            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            
            for row_number, row_data in enumerate(result[1:]):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    # Only user name is selectable
                    if column_number != 0:
                        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

                    self.tableWidget.setItem(row_number, column_number, item)

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
    
    def deleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                msg = QMessageBox(QMessageBox.Warning, "Warning", "Please select an entry to delete.")
                msg.setStyleSheet(get_basic_styling())
                msg.exec_()
            else:             
                question = QMessageBox()
                response = question.question(self,'', "Are you sure you want to delete the row?", question.Yes | question.No)
                
                if response == question.Yes:
                    nameForQuery = item[0].text()
                    
                    try:
                        mydb = connectToDatabase()
                        mycursor = mydb.cursor()
                        
                        sql_delete = "DELETE FROM users WHERE users_name = %s"
                        sql_data = (nameForQuery,)

                        mycursor.execute(sql_delete, sql_data)
                    
                        mydb.commit()
                        mydb.close()
                    except mydb.Error as e:
                        print("Failed To Connect to Database")
                    self.tableWidget.removeRow(currentRow)
                else:
                    question.close()
                    
    def recordInfo(self):   
        self.g = AddUserFile()
        self.g.submitButton.clicked.connect(self.checkBeforeGatheringInfo)
        self.g.submit_shortcut.activated.connect(self.checkBeforeGatheringInfo)

        self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
        self.g.show()

    def checkBeforeGatheringInfo(self):
        nameExists = False
        
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).text() == self.g.get_user_name():
                nameExists = True

        if nameExists or self.g.get_user_name == 'RESEARCHTEACHER':
            msg = QMessageBox(QMessageBox.Critical, "Error", "Username already exists.")
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()
        else:
            self.gatheringInfo()
    
    def export(self):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()

            mycursor.execute("Select users_name, users_code from users")

            result = mycursor.fetchall()
            
            all_users_name = []
            all_users_code = []
            
            for user_name, user_password in result:
                all_users_name.append(user_name)
                all_users_code.append(user_password)
            
            dictionary = {
                "NAME": all_users_name, "CODE": all_users_code
            }

            df = pd.DataFrame(dictionary)
            if platform.system() == 'Windows':
                df.to_csv("C:\\temp\CoralAllUsers.csv", na_rep="None")
            else:
                df.to_csv(os.path.expanduser("~/Desktop/AllUsers.csv"))
            
            msg = QMessageBox(QMessageBox.Warning, "Notice", "Check your desktop for the csv file!\n*Windows: see temp folder in C: drive*")
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
                                
    def changeAdminCode(self):  
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            randomGen = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
            mycursor.execute("UPDATE users SET users_code = '%s' WHERE users_name = '%s'" % (randomGen, getAdmin()))
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % getAdmin())
            myresult3 = mycursor.fetchall()
            
            code = ''.join(myresult3[0])
            
            mydb.commit()
            
            self.DBConnect()
            mydb.close()
        except mydb.Error as e:
            print("Failed To Connect to Database")
            
    def gatheringInfo(self):  
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute(
                "INSERT INTO users VALUES (%s, %s)", 
                (
                    self.g.get_user_name(), self.g.get_code()
                )
            )
            
            self.tableWidget.resizeRowsToContents()
            mydb.commit()
            
            self.DBConnect()
            self.g.close()
            mydb.close()
            
        except mydb.Error as e:
            print("Failed To Connect to Database")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()    
    window.activateWindow()
    sys.exit(app.exec_())