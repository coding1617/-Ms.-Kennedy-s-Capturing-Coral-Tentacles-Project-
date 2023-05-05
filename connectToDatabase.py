import mysql.connector as mc
import os

def connectToDatabase():
    mydb = mc.connect(
        host=os.environ.get('HOST'),
        user=os.getenv('NAME'),
        password=os.getenv('PASSWORD'), 
        database=os.getenv('DATABASE')             
    )