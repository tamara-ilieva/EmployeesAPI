import sqlite3
import pymongo
from bson.objectid import ObjectId
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_mongo_db():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["flaskapp"]
    return db
db = get_mongo_db()

def get_sqlite_connection():
    connect = sqlite3.connect("chinook.db")
    cursor = connect.cursor()
    return cursor, connect


@app.route('/')
def hello_world():
    return 'Python Course 2 AVRSM'

#Да се дополни flask апликацијата со CRUD методи за табелата artists
#Da se kreiraat CRUD metodi za bilo koja tabela od bazata chinook.db

@app.route('/get-artists', methods=["GET"])
def get_artists():
    cursor, connect = get_sqlite_connection()
    sql = "SELECT * FROM artists"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


@app.route('/add-artist', methods=["POST"])
def add_artist():
    request_data = json.loads(request.data)
    artist_name = request_data.get("artist_name")
    cursor, connect = get_sqlite_connection()
    cursor.execute("INSERT INTO artists (Name) VALUES (?)", (artist_name,))
    connect.commit()
    return {"message": "Thank you for adding a new artist"}


@app.route('/update-artist', methods=["PUT"])
def update_artist():
    request_data = json.loads(request.data)
    artist_id = request_data.get("artist_id")
    name = request_data.get("name")

    if not artist_id or not name:
        return jsonify({"error": "All fields ('artist_id', 'name') are required"}), 400

    try:
        connect = sqlite3.connect("chinook.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE artists SET Name=? WHERE ArtistId=?", (name,artist_id))
        connect.commit()
        connect.close()

        return jsonify({"message": "Artist updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete-artist', methods=["POST"])
def delete_artist():
    request_data = json.loads(request.data)
    artist_id = request_data.get("artist_id")

    if not artist_id:
        return jsonify({"error": "'artist_id' is required"}), 400

    try:
        cursor, connect = get_sqlite_connection()
        cursor.execute("DELETE FROM artists WHERE ArtistId=?", (artist_id,))
        connect.commit()
        connect.close()

        return jsonify({"message": "Artist deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Da se kreiraat CRUD metodi za kolekcijata Company - name, address, num_of_employees (mongodb)
@app.route('/get-companies', methods=["GET"])
def list_companies():
    company_collection = db["companies"]
    comp = list(company_collection.find())
    for e in comp:
        del e['_id']
    return comp

@app.route('/create-company', methods=["POST"])
def create_company():
    request_data = json.loads(request.data)
    name = request_data.get("name")
    address = request_data.get("address")
    num_of_employees = request_data.get("num_of_employees")

    try:
        company_collection = db["companies"]
        company = {
            "name": name,
            "address": address,
            "num_of_employees": num_of_employees,
        }
        company_collection.insert_one(company)

    except Exception as e:
        print(e)
        return f"Could not add employee {name} {address} - {num_of_employees}. Please try again later..."
    return f"Successfully added employee {name} {address} - {num_of_employees}"


@app.route('/update-company-employees/<id>', methods=["PUT"])
def update_company(id):
    request_data = json.loads(request.data)
    num_of_employees = request_data.get("num_of_employees")
    company_collection = db["companies"]
    query = {"_id": ObjectId(id)}
    new_values = {"$set": {"num_of_employees": num_of_employees}}
    company_collection.update_one(query, new_values)
    return "Successfully updated"


@app.route('/delete-company/<id>', methods=["DELETE"])
def delete_company(id):
    company_collection = db["companies"]
    query = {"_id": ObjectId(id)}
    company_collection.delete_one(query)
    return "Successfully deleted"



if __name__ == '__main__':
    app.run()

# GET chitanje na podatoci
# POST metod - zapishuvanje na podatoci
# PUT - updaterinje na podatoci/ izmena
# DELETE - brishenje na podatoci
