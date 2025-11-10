from flask import Flask, jsonify
from extensions import db, bcrypt, jwt # <-- 1. 匯入新工具
from models import User
import os
from dotenv import load_dotenv

# 匯入我們的新 API 藍圖
from auth import auth_bp # <-- 2. 匯入 API 檔案

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # --- 設定資料庫 ---
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL 沒設定在 .env 檔案中")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- 3. 設定 JWT 密鑰 ---
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        raise ValueError("JWT_SECRET_KEY 沒設定在 .env 檔案中")
    app.config['JWT_SECRET_KEY'] = jwt_secret

    # --- 4. 初始化所有工具 ---
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # --- 註冊 API 路由 ---
    @app.route("/")
    def get_hello_world():
        return jsonify({ "message": "Hello, World! 階段三成功了!" })

    # --- 5. 註冊我們的 API 藍圖 ---
    app.register_blueprint(auth_bp) # 這會掛載 auth.py 裡所有的路由

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)