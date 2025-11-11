from extensions import db

# --- 這就是你的第一個資料庫模型 ---
# db.Model 是 SQLAlchemy 的一個基礎類別
class User(db.Model):
    # __tablename__ 告訴 SQLAlchemy 資料表要叫什麼名字
    __tablename__ = 'users'

    # --- 定義欄位 ---
    # db.Integer 是一個整數
    # primary_key=True 代表這是「主鍵」(Unique ID)
    id = db.Column(db.Integer, primary_key=True)

    # db.String(80) 是一個最多 80 字的字串
    # unique=True 代表這個欄位的值不能重複
    # nullable=False 代表這個欄位不能是空的
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 我們不存密碼原文，只存「加密後的雜湊值」
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # 這是一個輔助函式，當你 print(user) 時會顯示有意義的資訊
    def __repr__(self):
        return f'<User {self.username}>'
    
# (請貼在 User 類別的下面)

class Course(db.Model):
    # 表格名稱
    __tablename__ = 'courses'

    # --- 定義欄位 ---
    id = db.Column(db.Integer, primary_key=True)

    # 課程名稱 (例如: "Python 後端入門")
    name = db.Column(db.String(100), nullable=False) 

    # 課程描述
    description = db.Column(db.Text, nullable=True) # Text 代表可接受長篇文字

    # 授課老師
    teacher = db.Column(db.String(100), nullable=False)

    # 課程價格 (我們用「整數」來存「分」，例如 1000 分 = 10 元，以避免浮點數誤差)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Course {self.name}>'