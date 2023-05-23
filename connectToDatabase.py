import mysql.connector as mc
import os

from config import *

def connectToDatabase():
    mydb = mc.connect(
        host=getHost(),
        user=getName(),
        password=getPass(), 
        database=getDB()             
    )

    return mydb