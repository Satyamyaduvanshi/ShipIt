import bcrypt
from flask import Flask, jsonify, request
from prisma import Prisma, errors

app = Flask(__name__)
prisma = Prisma()

# --- Helper Functions ---
async def get_prisma():
    """Helper to ensure Prisma is connected before every request."""
    if not prisma.is_connected():
        await prisma.connect()
    return prisma

# --- Routes ---

@app.route('/')
def home():
    return jsonify({
        "server": "ShipIt API",
        "status": "Running",
        "message": "Welcome to the ShipIt backend!"
    })

@app.route('/register', methods=['POST'])
async def register():
    """
    Registers a new user.
    Expects JSON: { "username": "...", "email": "...", "password": "..." }
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("username", "email", "password")):
            return jsonify({"error": "Missing required fields"}), 400

        client = await get_prisma()

        # Securely hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the user in the database
        new_user = await client.user.create(
            data={
                "username": data['username'],
                "email": data['email'],
                "hashed_password": hashed_password
            }
        )

        return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

    except errors.UniqueViolationError:
        # Prisma throws this if username or email already exists
        return jsonify({"error": "Username or email already taken"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
async def login():
    """
    Logs in a user.
    Expects JSON: { "email": "...", "password": "..." }
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("email", "password")):
            return jsonify({"error": "Missing email or password"}), 400

        client = await get_prisma()

        # Find the user by email
        user = await client.user.find_unique(where={"email": data['email']})

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify the password
        if bcrypt.checkpw(data['password'].encode('utf-8'), user.hashed_password.encode('utf-8')):
            # In a real app, you would generate and return a JWT token here.
            # For now, we'll just return a success message and the user ID.
            return jsonify({"message": "Login successful", "user_id": user.id}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
