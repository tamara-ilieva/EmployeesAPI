import json

from flask import Flask, request, jsonify

app = Flask(__name__)

# json.loads -> od json vo python dict
# json.dumps -> od python dict vo json

@app.route("/", methods=["GET"])
def home_page():
    return "Calculator API"


@app.route("/add", methods=["POST"])
def add_numbers():
    data = json.loads(request.data)
    if "num1" not in data.keys() or "num2" not in data.keys():
        return jsonify({"error": "Please enter 2 numbers"}), 400

    first_number = data.get("num1")
    second_number = data.get("num2")
    return {"result": first_number + second_number}


@app.route("/subtract", methods=["POST"])
def subtract_numbers():
    data = json.loads(request.data)
    if "num1" not in data.keys() or "num2" not in data.keys():
        return "Please enter 2 numbers"

    first_number = data.get("num1")
    second_number = data.get("num2")
    return {"result": first_number - second_number}


if __name__ == "__main__":
    app.run()
