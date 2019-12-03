#!usr/bin/env python3

import mysql.connector as sql
from datetime import date, datetime
from os import environ


def json_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def db_connect():
    try:
        db = sql.connect(user=environ['MYSQL_USER'], password=environ['MYSQL_PASSWORD'], host="db", database=environ['MYSQL_DB_NAME'])
        cursor = db.cursor()

        return db, cursor
    except sql.Error as er:
        if er.errno == sql.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with username or password")
        elif er.errno == sql.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exit")
        else:
            print(er)

def date_today_s():
    return date.today().strftime('%Y-%m-%d')
