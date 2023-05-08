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

from connectToDatabase import *
class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin App")  
        self.move(0,0)

        self.generalLayout = QGridLayout()

        self.addUserButton = QPushButton("Add User")
        self.addUserButton.clicked.connect(self.recordInfo)
        self.deleteUserButton = QPushButton("Delete User")
        self.deleteUserButton.clicked.connect(self.deleteRow)
        self.changeAdminCodeButton = QPushButton("ChangeAdminCode")
        self.changeAdminCodeButton.clicked.connect(self.changeAdminCode)
        
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


        # Bring back later:
        # header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        self.adminName_Label = QLabel()
        self.adminCode_Label = QLabel()
        
        self.exportButton = QPushButton("Export")
        load_dotenv('config.env')
        self.exportButton.clicked.connect(self.export)
        
        self.buttonGridLayout.addWidget(self.adminName_Label, 1, 0)
        self.buttonGridLayout.addWidget(self.adminCode_Label, 1, 1)

        self.generalLayout.addLayout(self.buttonGridLayout, 0, 0)
        self.generalLayout.addWidget(self.tableWidget, 1, 0)
        self.generalLayout.addWidget(self.exportButton, 2, 0)
        

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
            
            mycursor.execute("SELECT users_name FROM users WHERE users_name = '%s'" % os.getenv('ADMIN'))
            myresult = mycursor.fetchall()
            #print(myresult)
            #print(myresult[0])
            userName = ''.join(myresult[0])
            #print(userName)
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % os.getenv('ADMIN'))
            myresult2 = mycursor.fetchall()
            #print(myresult2)
            #print(myresult2[0])
            code = ''.join(myresult2[0])
            #print(code)
            self.adminCode_Label.clear()
            self.adminName_Label.setText("Username: %s" % userName)
            self.adminCode_Label.setText("Code: %s" % code)
            
            mycursor.execute("SELECT * FROM users")

            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            #print(result[1:])
            for row_number, row_data in enumerate(result[1:]):
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
    
    def export(self):
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
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
                df.to_csv("C:\\temp\AllUsers.csv", na_rep="None")
            else:
                df.to_csv(os.path.expanduser("~/Desktop/AllUsers.csv"))
            QMessageBox.about(self, "Warning", "Check your desktop for the csv file!")
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
                                
    def changeAdminCode(self):  
        
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
            mycursor = mydb.cursor()
            randomGen = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
            mycursor.execute("UPDATE users SET users_code = '%s' WHERE users_name = '%s'" % (randomGen, os.getenv('ADMIN')))
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % os.getenv('ADMIN'))
            myresult3 = mycursor.fetchall()
            print(myresult3)
            print(myresult3[0])
            code = ''.join(myresult3[0])
            print(code)
            #self.adminName_Label = QLabel("Username: %s" % userName)
            #self.adminCode_Label.setText("Code: %s" % "")
            #self.adminCode_Label.setText("Code: %s" % code)
            #self.tableWidget.resizeRowsToContents()
            mydb.commit()
            
            self.DBConnect()
            #self.g.close()
            mydb.close()
        except mydb.Error as e:
            print("Failed To Connect to Database")
            
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