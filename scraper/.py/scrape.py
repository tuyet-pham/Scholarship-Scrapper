#!usr/bin/env python
# mysql.connector & it's corresponding error code for to be able to connect to the mysql database
#
# The following code is to 'insert into' the scraped scholarships ONLY. 
# This script is not used for the scholarships that are pending for removal or acceptance.
#
# The following packages :
#   $ pip install MySQL-python
#   $ pip install mysql-connector-python

import mysql.connector as sql
import sys, os
from mysql.connector import errorcode
import csv 
from datetime import date
import datetime
import re

def scrape(usern, passwd, hostl, databasen):
    try:
        conx = sql.connect(user=usern, password=passwd , host=hostl, database=databasen)
        cursor = conx.cursor()

        time=date.today()
        filename='scan_'+str(time)+'.csv'
        reader = csv.reader(open(filename))

        i = 0
        # for each row in the csv file the cursor will make a relation in the table `Scholarship` with name, URL, amount and deadline.
        for row in reader:
            if i==0:
                i=i+1
                continue
            else:
                cursor.execute("INSERT INTO Scholarship (name, url, amount, deadline ) VALUES (%s,%s,%s,%s)", (row[0], row[1], int(row[2]), row[3]))

        cursor.execute("UPDATE Scholarship set deadline = NULL where deadline = '1000-01-01';")
        cursor.execute("UPDATE Scholarship set amount = NULL where amount = 0;")


        print("Successful Scrape! Scraped filename : %s" %filename)
        # Close 
        conx.commit()
        cursor.close()
        conx.close()
    except sql.Error as er:
        if er.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with username or password")
        elif er.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exit")
        else:
            print(er)


# This function formats the date from 
def toDate(date_str):
    if date_str=='Varies' or date_str=='varies':
        return '1000-01-01'
    else:
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        return datetime_obj.date() 

def toAmount(amount):
    if amount=='Varies' or amount=='varies' or amount=='' or amount==' ':
        return 0
    else:
        line = re.sub('[Variesv!,@#$ ]', '', amount)
        if line == '':
            line = 0
        return int(line)
