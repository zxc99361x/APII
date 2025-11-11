from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 這裡的名字必須是 'auth'
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# --- 建立 /api/auth/register 路由 ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({ "error": "Email, password 和 username 都是必須的" }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({ "error": "這個 Email 已經被註冊" }), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "使用者註冊成功！",
            "user": { "id": new_user.id, "username": new_user.username, "email": new_user.email }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({ "error": "資料庫儲存失敗", "details": str(e) }), 500

# --- 建立 /api/auth/login 路由 ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({ "error": "Email 和 password 都是必須的" }), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({ "error": "無效的憑證" }), 401

    is_password_correct = bcrypt.check_password_hash(user.password_hash, password)
    if not is_password_correct:
        return jsonify({ "error": "無效的憑證" }), 401

    # [FIX] 這裡必須是字串
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "登入成功！",
        "access_token": access_token,
        "user": { "id": user.id, "username": user.username, "email": user.email }
    }), 200

# --- 建立 /api/me 路由 ---
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id) 

    if not user:
        return jsonify({ "error": "找不到該使用者" }), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200