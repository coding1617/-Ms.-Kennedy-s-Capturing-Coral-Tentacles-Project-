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

from AddUserFile import AddUserFile
class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin App")  
        self.move(0,0)

        self.generalLayout = QGridLayout()
        # layout = QVBoxLayout()

        self.addUserButton = QPushButton("Add User")
        self.addUserButton.clicked.connect(self.recordInfo)
        self.deleteUserButton = QPushButton("Delete User")
        self.deleteUserButton.clicked.connect(self.deleteRow)
        #self.editUserButton = QPushButton("Edit User")

        self.buttonGridLayout = QGridLayout()
        self.buttonGridLayout.addWidget(self.addUserButton, 0, 0)
        self.buttonGridLayout.addWidget(self.deleteUserButton, 0, 1)
        #self.buttonGridLayout.addWidget(self.editUserButton, 0, 2)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Code"])
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")


        # Bring back later:
        # header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.generalLayout.addLayout(self.buttonGridLayout, 0, 0)
        self.generalLayout.addWidget(self.tableWidget, 1, 0)

        self.setLayout(self.generalLayout)
        
        load_dotenv('config.env')
        self.DBConnect()
        
    def DBConnect(self):
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM users")

            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
    
    def deleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:             
                question = QMessageBox()
                response = question.question(self,'', "Are you sure you want to delete the row?", question.Yes | question.No)
                
                if response == question.Yes:
                    nameForQuery = item[0].text()
                    
                    try:
                        mydb = mc.connect(
                            host=os.environ.get('HOST'),
                            user = os.getenv('NAME'),
                            password=os.getenv('PASSWORD'), 
                            database=os.getenv('DATABASE')             
                        )
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
        self.g.submitButton.clicked.connect(self.gatheringInfo)
        #self.g.submit_shortcut.activated.connect(self.gatheringInfo)

        self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
        self.g.show()
                      
    def gatheringInfo(self):  
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
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