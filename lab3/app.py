from typing import OrderedDict
from flask import Flask, request, make_response, jsonify
import pymysql
from decimal import Decimal
import subprocess
import os


def queryDatabase(queryString, insert=False, value=()):
    conn = pymysql.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database='dbms_lab3'
                    )

    cursor = conn.cursor()
    if(insert == True):
        query = queryString
        cursor.execute(query, value)
        return True

    if(insert == False):
        query = queryString

        cursor.execute(query)
        rows = cursor.fetchall()
        count = 0
        lst = []
        for row in rows:
            if(count == 10):
                break
            lst.append(row)
            count += 1
        return lst


app = Flask(__name__)

# GET routes

@app.route('/', methods=["GET"])
def createDatabase():
    databaseFile = file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.py')
    print(databaseFile)
    result = subprocess.run(["python", databaseFile], capture_output=True)
    return str(result)

@app.route('/customers', methods=["GET"])
def getCustomers():
    result = queryDatabase("SELECT * FROM labour_force")
    
    lst = []
    for tuple in result:
        customer = OrderedDict()
        customer["customerID"] = tuple[0]
        customer["Gender"] = tuple[1]
        customer["Age"] = tuple[2]
        customer["AnnualIncome"] = Decimal(tuple[3])
        customer["SpendingScore"] = tuple[4]
        customer["Profession"] = tuple[5]
        customer["WorkExperience"] = tuple[6]
        customer["FamilySize"] = tuple[7]
        lst.append(customer)

    return (lst)

@app.route('/customer/<customer_id>', methods=["GET"])
def getCustomer(customer_id):
    result = queryDatabase(f"SELECT * FROM labour_force WHERE `customerID` ={customer_id}")
    if(len(result) > 0):
        for tuple in result:
            customer = OrderedDict()
            customer["customerID"] = tuple[0]
            customer["Gender"] = tuple[1]
            customer["Age"] = tuple[2]
            customer["AnnualIncome"] = Decimal(tuple[3])
            customer["SpendingScore"] = tuple[4]
            customer["Profession"] = tuple[5]
            customer["WorkExperience"] = tuple[6]
            customer["FamilySize"] = tuple[7]
            return customer
        
    return "No customer has that id #"


@app.route('/highest_income_report', methods=["GET"])
def highestIncome():
    result = queryDatabase("SELECT `customerID`, `profession`, MAX(`annual_income`) as MaxIncome FROM `labour_force` WHERE `profession` IS NOT NULL AND `profession` != '' GROUP BY `profession`")
    lst = []
    for data in result:
        customer = OrderedDict()
        customer['CustomerID'] = data[0]
        customer['AnnualIncome'] = round(int(data[2]),2)
        customer['Profession'] = data[1]
        lst.append(customer)

    return lst

@app.route('/total_income_report', methods=["GET"])
def totalIncome():
    result = queryDatabase("SELECT `profession`, SUM(`annual_income`) as TotalIncome FROM `labour_force` WHERE `profession` IS NOT NULL AND `profession` !='' GROUP BY `profession`;")
    lst = []
    for data in result:
        customer = OrderedDict()
        customer['AnnualIncome'] = Decimal(data[1])
        customer['Profession'] = data[0]
        lst.append(customer)
    return lst


@app.route('/average_work_experience', methods=["GET"])
def avgWorkExperience():
    result = queryDatabase("SELECT `profession`, AVG(`work_experience`) as AverageExperience FROM `labour_force`  WHERE `annual_income` > 50000 AND `age` < 35 AND `profession` IS NOT NULL AND `profession` != '' GROUP BY `profession`;")
    lst = []
    for data in result:
        customer = OrderedDict()
        customer['AverageExperience'] = int(data[1])
        customer['Profession'] = data[0]
        lst.append(customer)
    
    return lst

@app.route('/average_spending_score/<profession>', methods=["GET"])
def avgSpendingScore(profession):
    result = queryDatabase(f"SELECT `gender`, AVG(`spending_score`) as AVERAGESPENDINGSCORE FROM `labour_force` WHERE `profession`='{profession}' GROUP BY `gender`;")
    lst = []
    for data in result:
        customer = OrderedDict()
        customer['Gender'] = data[0]
        customer['AverageSpendingScore'] = int(data[1])
        lst.append(customer)
    return lst

# POST routes

@app.route("/add_customer", methods=["POST"]) 
def add_customer():
    customerObject = request.get_json()
    id = customerObject['CustomerID']
    gender = customerObject['Gender']
    age = customerObject['Age']
    ai = customerObject['AnnualIncome']
    ss = customerObject['SpendingScore']
    prof = customerObject['Profession']
    we = customerObject['WorkExperience']
    fs = customerObject['FamilySize']

    value = (gender, int(age), int(ai), int(ss), prof, int(we), int(fs))
    populate_query ="INSERT INTO labour_force (gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    result = queryDatabase(populate_query, True, value)

    response = jsonify({"message":"Record inserted successfully!"})
    response.status = 200
    return response

# PUT routes 

@app.route('/update_profession/<customer_id>', methods=["PUT"])
def updateProfession(customer_id):
    data = request.get_json()
    result = queryDatabase(f"UPDATE labour_force SET `profession`='{data['Profession']}' WHERE `customerID`={customer_id};")
    response = jsonify({'message':f'CustomerID #{customer_id} was updated successfully!'})
    response.status = 200
    return response

if __name__ == '__main__':
    app.run(debug=True)