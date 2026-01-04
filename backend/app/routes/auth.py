from flask import Blueprint, request, jsonify
from app.db import db, connect_db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    connect_db()

    try:
       
        existing = db.user.find_first(where={'email': email})
        if existing:
            return jsonify({"error": "User already exists"}), 400

        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

       
        user = db.user.create(data={
            'username': username,
            'email': email,
            'password': hashed.decode('utf-8')
        })
        
        return jsonify({"message": "User created!", "user_id": user.id}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    connect_db()

    user = db.user.find_unique(where={'email': email})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401