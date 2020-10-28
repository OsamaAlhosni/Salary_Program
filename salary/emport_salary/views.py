from django.shortcuts import render
import sqlite3
from sqlite3 import Error
from employee.models import Salary
from django.contrib.auth.models import User


def create_conn(database):
    conn = None

    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn


def select_salary(conn):
    cur = conn.cursor()
    # SELECT * FROM Salary_8_2020
    cur.execute('SELECT * FROM Salary_8_2020')
    emp_salary = cur.fetchall()
    # cur.execute('INSERT INTO employee_salary (user_id, sMonth, sYear,base_salary,total_salary,total_Diesc,net_salary,overtime,health_care,solfa1,solfa2) SELECT EmpID, sMonth, sYear,base_salary,total_salary,Total_Disc,net_salary,overtime,health_care,solfa1,solfa2  FROM Salary_8_2020 WHERE EmpID IN  (SELECT EmpID FROM Employee) ')
    cur.execute('INSERT INTO employee_salary (user_id, sMonth, sYear,base_salary,total_salary,total_Diesc,net_salary,overtime,health_care,solfa1,solfa2) SELECT  id,sMonth,sYear,base_salary,total_salary,Total_Disc,net_salary,overtime,health_care,solfa1,solfa2 FROM Salary_8_2020  INNER JOIN auth_user u on EmpID = username ')    
    rows = cur.fetchall()
    for row in rows:

        print(row)


def start_emport(request):
    if request.method == "POST":
        database = 'D:\Projects\Salary_Program\salary\db.sqlite3'
        conn = create_conn(database)
        with conn:
            select_salary(conn)
        return render(request, 'emport_salary.html', {'Msg': 'Start Emport'})
    else:
        return render(request, 'emport_salary.html', {'Msg': 'emport salary'})
