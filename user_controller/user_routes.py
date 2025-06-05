import jwt
import socket
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate, ValidationError
from faker import Faker
from database_config import db  # ✅ Ensure this path is correct

user = Blueprint("user", __name__)

# -----------------------------
# Model: UserSignup
# -----------------------------
class UserSignup(db.Model):
    __tablename__ = 'user_signup'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(200))
    ip = db.Column(db.String(45))
    device = db.Column(db.String(100))

# -----------------------------
# Schema: for Validation
# -----------------------------
class UserSignupSchema(Schema):
    username = fields.String(required=True, validate=validate.Regexp(r'^[A-Za-z]+$'))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Regexp(r'^[789]\d{9}$'))
    password = fields.String(required=True, validate=validate.Length(min=8))

# -----------------------------
# Route: Insert User
# -----------------------------
@user.route('/insert', methods=['POST'])
def insert_user():
    data = request.get_json()  # 🐞 Set breakpoint here to inspect incoming data

    # Validate incoming data
    try:
        UserSignupSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check for existing user
    if UserSignup.query.filter((UserSignup.email == data['email']) | (UserSignup.phone == data['phone'])).first():
        return jsonify({"message": "Email or Phone already exists"}), 400

    # Generate custom ID and details
    count = UserSignup.query.count() + 1
    user_id = f"US000{count}"
    ip = Faker().ipv4()
    device = socket.gethostname()

    # Create and commit new user
    new_user = UserSignup(
        user_id=user_id,
        username=data['username'],
        email=data['email'],
        phone=data['phone'],
        password=generate_password_hash(data['password']),
        ip=ip,
        device=device
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User inserted successfully"}), 200

# -----------------------------
# Route: List Users
# -----------------------------
@user.route('/list', methods=['GET'])
def list_users():
    users = UserSignup.query.all()
    return jsonify([
        {
            "id": u.id,
            "user_id": u.user_id,
            "username": u.username,
            "email": u.email,
            "phone": u.phone,
            "ip": u.ip,
            "device": u.device
        } for u in users
    ]), 200

# -----------------------------
# Route: Login User
# -----------------------------
@user.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()  # 🐞 Set breakpoint here to inspect login data
    user = UserSignup.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"message": "Invalid credentials"}), 401

    payload = {
        'user_id': user.user_id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=2)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({"token": token}), 200
