from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


client = MongoClient("mongodb://localhost:27017/")  
db = client["user_database"]  
db.command("dropDatabase")
users_collection = db["users"]  
adminpass = generate_password_hash("noadminhere")
user = {"username": "admin", "password":adminpass }
users_collection.insert_one(user)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  
    username = data.get("username")
    password = data.get("password")

    
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists", "status": "error"}), 400

    print(type(password))
    hashed_password = generate_password_hash(password)

    
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully", "status": "success"}), 201


@app.route('/login', methods=['POST'])
def login():
   
    data = request.json  
    username = data.get("username")
    password = data.get("password")
    
    # for user in users_collection.find():  
    #     v = user.get("password")  
    #     vv = user.get("username")  
    #     print(v, ' ', vv)


    
    user = users_collection.find_one({"username": username})

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login Successful", "status": "success"}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "error"}), 401

if __name__ == '__main__':
    app.run(debug=True)
