import sqlite3
import pymongo
from bson.objectid import ObjectId
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# Da se kreiraat CRUD metodi za kolekcijata Company - name, address, num_of_employees (mongodb)
# Da se kreiraat CRUD metodi za bilo koja tabela od bazata chinook.db

# CRUD - C - create (post), R - read (get), U- update (put, patch), D - delete (delete)

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


@app.route('/employees', methods=["GET"])
def list_employees():
    employees_collection = db["employees"]
    emps = list(employees_collection.find())
    for e in emps:
        del e['_id']
    return emps


@app.route('/create-employee', methods=["POST"])
def create_employee():
    request_data = json.loads(request.data)
    # name = request.form.get("name")
    # last_name = request.form.get("last_name")
    # age = request.form.get("age")
    name = request_data.get("name")
    last_name = request_data.get("last_name")
    age = request_data.get("age")

    # TODO: validate data from user

    try:
        employees_collection = db["employees"]
        employee = {
            "name": name,
            "last_name": last_name,
            "age": age,
        }
        employees_collection.insert_one(employee)

    except Exception as e:
        print(e)
        return f"Could not add employee {name} {last_name} - {age}. Please try again later..."
    return f"Successfully added employee {name} {last_name} - {age}"

# 127.0.0.1:5000/update/45
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


@app.route('/get-albums', methods=["GET"])
def get_albums():
    cursor, connect = get_sqlite_connection()
    sql = "SELECT * FROM albums"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


@app.route('/add-album', methods=["POST"])
def add_album():
    # artist_id = request.form.get("artist_id")
    # title = request.form.get("title")
    request_data = json.loads(request.data)
    artist_id = request_data.get("artist_id")
    title = request_data.get("title")
    cursor, connect = get_sqlite_connection()
    cursor.execute("INSERT INTO albums (Title, ArtistId) VALUES (?, ?)", (title, artist_id))
    connect.commit()
    return {"message": "Thank you for adding a new album"}


@app.route('/update-album', methods=["PUT"])
def update_album():
    album_id = request.form.get("album_id")
    title = request.form.get("title")
    artist_id = request.form.get("artist_id")

    if not album_id or not title or not artist_id:
        return jsonify({"error": "All fields ('album_id', 'title', 'artist_id') are required"}), 400

    try:
        connect = sqlite3.connect("chinook.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE albums SET Title=?, ArtistId=? WHERE AlbumId=?", (title, artist_id, album_id))
        connect.commit()
        connect.close()

        return jsonify({"message": "Album updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete-album', methods=["POST"])
def delete_album():
    album_id = request.form.get("album_id")

    if not album_id:
        return jsonify({"error": "'album_id' is required"}), 400

    try:
        cursor, connect = get_sqlite_connection()
        cursor.execute("DELETE FROM albums WHERE AlbumId=?", (album_id,))
        connect.commit()
        connect.close()

        return jsonify({"message": "Album deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/greeting/<name>')
def hello_name(name):
    return f"Hello {name}"


if __name__ == '__main__':
    app.run()

# GET chitanje na podatoci
# POST metod - zapishuvanje na podatoci
# PUT - updaterinje na podatoci/ izmena
# DELETE - brishenje na podatoci
