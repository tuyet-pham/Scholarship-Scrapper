import mysql.connector as sql
import sys, os
from mysql.connector import errorcode
from datetime import date


class dbScholarscrape():
    def __init__(self):
        try:
            self.conx = sql.connect(user='snow', password='Skylarstanley12', host='localhost', database='scholarscrape')
            self.cur = self.conx.cursor()

            print("Setup Done.") 
        except sql.Error as er:
            if er.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif er.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exit")
            else:
                print(er)
        
    def displayListing(self):
        self.cur.execute("SELECT * FROM Scholarship where amount ==")
        result = self.cur.fetchall()
        return result
    
        
    # Will be added into our db awaiting admin approval
    def requestListing(self, name, url, amount, deadline):
        return "hello"

    def displayBy(self):
        return "Hello"
