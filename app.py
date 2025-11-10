from flask import Flask, jsonify
from extensions import db  # 匯入我們在 extensions.py 宣告的 db
from models import User    # 匯入我們剛建立的 User 模型
import os
from dotenv import load_dotenv

def create_app():
    # 1. 讀取 .env 檔案中的「保險箱」
    load_dotenv()

    app = Flask(__name__)

    # 2. 從「保險箱」讀取資料庫連線設定
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL 沒設定在 .env 檔案中")

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 關閉一個警告

    # 3. 把 Flask App 和 db「綁定」在一起 (初始化)
    db.init_app(app)

    # --- 4. 註冊你的 API 路由 ---
    @app.route("/")
    def get_hello_world():
        return jsonify({ "message": "Hello, World! 階段二成功了!" })

    # (我們未來會在這裡加上 /register, /login...)

    # --- 5. 回傳建立好的 app ---
    return app

# --- 這是新的啟動方式 ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)