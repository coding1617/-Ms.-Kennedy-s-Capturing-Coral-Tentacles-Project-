import mysql.connector as mc

from config import *

def connectToDatabase():
    mydb = mc.connect(
        host=getHost(),
        user=getName(),
        password=getPass(), 
        database=getDB()             
    )

    return mydb