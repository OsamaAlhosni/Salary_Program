from django.shortcuts import render
import sqlite3
from sqlite3 import Error

def create_conn(database):
    conn = null
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn

def select_salary(conn):
    cur = conn.cursor()
    cur.execute('select * from Salary')
    rows = cur.fetchall()
    for row in rows:
        print(row)

def start_emport(request):
    if request.method == "POST":
        database = 'D:\Projects\salary_pro\salary\db.sqlite3'
        conn = create_conn(database)
        with conn:
            select_salary(conn)
        return render(request,'emport_salary',{'Msg': 'Start Emport'})
    else:
        return render(request,'emport_salary.html',{'Msg': 'emport salary'})



