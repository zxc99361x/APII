from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity # <-- [修改]

# 建立一個藍圖
# 'auth' 是這個藍圖的名字
# url_prefix='/api/auth' 代表這個檔案中所有的路由都會自動加上 /api/auth 的前綴
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# --- 建立 /api/auth/login 路由 ---
@auth_bp.route('/login', methods=['POST'])
def login():
    # 1. 獲取 JSON 資料
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 2. 檢查資料是否齊全
    if not email or not password:
        return jsonify({ "error": "Email 和 password 都是必須的" }), 400

    # 3. [關鍵] 檢查使用者是否存在
    # 我們用 email 去資料庫裡找人
    user = User.query.filter_by(email=email).first()

    if not user:
        # 為了安全，不要提示「使用者不存在」，統一說「憑證錯誤」
        return jsonify({ "error": "無效的憑證" }), 401 # 401 代表 "Unauthorized"

    # 4. [關鍵] 檢查密碼是否正確
    # bcrypt.check_password_hash() 會比較：
    # (資料庫中的雜湊值, 使用者這次輸入的明碼)
    is_password_correct = bcrypt.check_password_hash(user.password_hash, password)

    if not is_password_correct:
        return jsonify({ "error": "無效的憑證" }), 401

    # 5. [成功] 產生 JWT Token
    # "identity" 參數是告訴 JWT 這個 Token 是屬於 "誰" 的
    # 我們把 user.id 存進去，方便未來使用
    access_token = create_access_token(identity=str(user.id))

    # 6. 回傳 Token
    return jsonify({
        "message": "登入成功！",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200 # 200 代表 "OK"

# --- 建立 /api/me 路由 ---
@auth_bp.route('/me', methods=['GET'])
@jwt_required()  # <-- [關鍵] 加上這個「保全」！
def get_me():
    # 1. [關鍵] 讀取登機證上的身分 (我們在 login 時存的是 user.id)
    user_id = get_jwt_identity()

    # 2. 用這個 id 去資料庫裡找人
    user = User.query.get(user_id) # .get() 是「用 primary key 查找」的快捷方式

    if not user:
        return jsonify({ "error": "找不到該使用者" }), 404

    # 3. 回傳使用者資料 (注意：永遠不要回傳 password_hash)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200