from flask import Flask, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)


def get_db():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["flaskapp"]
    return db


db = get_db()

# COMPANY - name, address, num_of_employees

@app.route('/')
def hello_world():  # put application's code here
    return 'Python'


@app.route('/<name>')
def hello_name(name):
    return f"Hello {name}"


@app.route('/employees', methods=["GET"])
def list_employees():
    employees_collection = db["employees"]
    emps = list(employees_collection.find())
    for e in emps:
        del e['_id']
    return emps


@app.route('/create', methods=["POST"])
def create_employee():
    name = request.form.get("name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")

    employees_collection = db["employees"]
    employee = {
        "name": name,
        "last_name": last_name,
        "age": age,
    }
    employees_collection.insert_one(employee)
    return f"Successfully added employee {name} {last_name} - {age}"


@app.route('/update/<id>', methods=["PUT"])
def update_employee(id):
    age = request.form.get("age")
    employees_collection = db["employees"]
    query = {"_id": ObjectId(id)}
    new_values = {"$set": {"age": age}}
    employees_collection.update_one(query, new_values)
    return "Successfully updated"


@app.route('/delete/<id>', methods=["DELETE"])
def delete_employee(id):
    employees_collection = db["employees"]
    query = {"_id": ObjectId(id)}
    employees_collection.delete_one(query)
    return "Successfully deleted"


# GET chitanje na podatoci
# POST metod - zapishuvanje na podatoci
# PUT - updaterinje na podatoci/ izmena
# DELETE - brishenje na podatoci


if __name__ == '__main__':
    app.run()
