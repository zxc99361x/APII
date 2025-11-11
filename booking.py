from flask import Blueprint, request, jsonify
from models import Booking, User, Course # <-- 匯入所有模型
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# 建立一個新的藍圖 (Blueprint)
booking_bp = Blueprint('booking', __name__, url_prefix='/api')

# --- 1. [POST] 預約課程 ---
# 我們把 course_id 放在 URL 中
@booking_bp.route('/book/<int:course_id>', methods=['POST'])
@jwt_required() # <-- [保全] 必須要登入才能預約
def book_course(course_id):
    # 1. 取得使用者身分
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # 2. 檢查課程是否存在
    course = Course.query.get(course_id)
    if not course:
        return jsonify({ "error": "找不到這門課程" }), 404

    # 3. [關鍵] 檢查是否已經預約過
    existing_booking = Booking.query.filter_by(user_id=user.id, course_id=course.id).first()
    if existing_booking:
        return jsonify({ "error": "你已經預約過這門課程" }), 409 # 409 = Conflict

    # 4. 建立預約
    new_booking = Booking(
        user_id=user.id,
        course_id=course.id
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({
            "message": "課程預約成功！",
            "booking": {
                "id": new_booking.id,
                "course_name": course.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({ "error": "資料庫儲存失敗", "details": str(e) }), 500

# --- 2. [GET] 取得我預約的所有課程 (受保護) ---
@booking_bp.route('/my_bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    # 1. 取得使用者身分
    user_id = get_jwt_identity()

    # 2. [關鍵] 透過 user_id 查詢 bookings 表格
    # .filter_by() 會找出所有符合條件的紀錄
    bookings = Booking.query.filter_by(user_id=user_id).all()

    if not bookings:
        return jsonify({ "message": "你尚未預約任何課程", "bookings": [] }), 200

    # 3. 整理要回傳的資料
    result = []
    for booking in bookings:
        # booking.course 是我們在 models.py 中定義的「反向關聯」
        # 它讓你可以直接從 booking 物件抓到 course 的資料
        result.append({
            "booking_id": booking.id,
            "course_id": booking.course.id,
            "course_name": booking.course.name,
            "teacher": booking.course.teacher,
            "booking_date": booking.booking_date.isoformat() # 轉換日期格式
        })

    return jsonify(result), 200