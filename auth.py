from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt

# 建立一個藍圖
# 'auth' 是這個藍圖的名字
# url_prefix='/api/auth' 代表這個檔案中所有的路由都會自動加上 /api/auth 的前綴
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# --- 建立 /api/auth/register 路由 ---
# methods=['POST'] 代表這個端點只接受 POST 請求
@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. 從請求中獲取 JSON 資料
    data = request.get_json()

    # 2. 從 JSON 中取出 email 和 password
    email = data.get('email')
    password = data.get('password')
    username = data.get('username') # 我們也順便拿一下 username

    # 3. 檢查資料是否齊全
    if not email or not password or not username:
        return jsonify({ "error": "Email, password 和 username 都是必須的" }), 400

    # 4. 檢查 Email 是否已被註冊
    if User.query.filter_by(email=email).first():
        return jsonify({ "error": "這個 Email 已經被註冊" }), 409

    # 5. [關鍵] 將密碼加密 (雜湊)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 6. 建立一個新的 User 物件
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    # 7. [關鍵] 將新使用者寫入資料庫
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback() # 如果出錯，就回復
        return jsonify({ "error": "資料庫儲存失敗", "details": str(e) }), 500

    # 8. 回傳成功的訊息
    return jsonify({
        "message": "使用者註冊成功！",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201 # 201 代表 "Created" (已建立)