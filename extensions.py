from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # <-- 新增
from flask_jwt_extended import JWTManager  # <-- 新增

# 我們先「宣告」有這個工具，但還沒「初始化」
db = SQLAlchemy()
bcrypt = Bcrypt()  # <-- 新增
jwt = JWTManager() # <-- 新增