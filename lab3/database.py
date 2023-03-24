import pymysql
import openpyxl
import csv
import os

sqlScriptString = ""
csvFile = file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Customers.csv')

with open(csvFile, 'r') as file:
    reader = csv.reader(file)

    conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                )

    # create a cursor object
    cursor = conn.cursor()

    # execute a CREATE DATABASE query

    query1 = "DROP DATABASE IF EXISTS dbms_lab3;"
    query2 = "CREATE DATABASE dbms_lab3;"
    query3 = "USE dbms_lab3"
    query4 = "DROP TABLE IF EXISTS  labour_force;"
    query5 = """CREATE TABLE labour_force (
        `customerID` int(20) NOT NULL AUTO_INCREMENT,
        `gender` varchar(50) NOT NULL DEFAULT '',
        `age` int(20) NOT NULL DEFAULT 0,
        `annual_income` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        `spending_score` int(20) NOT NULL DEFAULT 0,
        `profession` varchar(50) NOT NULL DEFAULT '', 
        `work_experience` int(20) NOT NULL DEFAULT 0,
        `family_size` int(20) NOT NULL DEFAULT 0,
        PRIMARY KEY(`customerID`)
    );"""

    sqlScriptString += query1 + '\n' + query2 + '\n' +query3 + ";" + '\n' + query4 + '\n' + query5 + '\n'

    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    cursor.execute(query5)


    count = 0
    sqlScriptString += f"INSERT INTO labour_force (gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES " + '\n'
    for row in reader:
        if(count > 0):
            populate_query ="INSERT INTO labour_force (gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (row[1], int(row[2]), int(row[3]), int(row[4]), row[5], int(row[6]), int(row[7]))
            sqlScriptString += f"('{row[1]}', {row[2]}, {row[3]}, {row[4]}, '{row[5]}', {row[6]}, {row[7]})," + '\n'
            

            
            cursor.execute(populate_query, value)

        count += 1
    sqlScriptString = sqlScriptString.strip().rstrip()
    last_comma = sqlScriptString.rfind(',')
    sqlScriptString = sqlScriptString[:last_comma] + sqlScriptString[last_comma+1:]
    sqlScriptString += ";"


    conn.commit()

            # close cursor and connection
    cursor.close()
    conn.close()


print("Database populated!")

with open('database.sql', 'w') as sqlFile:
    sqlFile.write(sqlScriptString)