from flask import Blueprint, request, jsonify
from models import Course, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')

# --- 1. [POST] 新增課程 (管理員限定) ---
@course_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({ "error": "權限不足，僅管理員可新增課程" }), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    teacher = data.get('teacher')
    price = data.get('price')

    if not name or not teacher or price is None:
        return jsonify({ "error": "課程名稱、老師和價格為必填" }), 400

    new_course = Course(
        name=name,
        description=description,
        teacher=teacher,
        price=price
    )

    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify({
            "message": "課程建立成功",
            "course": { "id": new_course.id, "name": new_course.name, "teacher": new_course.teacher }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({ "error": "資料庫儲存失敗", "details": str(e) }), 500

# --- 2. [GET] 取得所有課程 (公開) ---
@course_bp.route('/', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "teacher": course.teacher,
            "price": course.price
        })
    return jsonify(result), 200

# --- 3. [GET] 取得單一課程 (公開) ---
@course_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({ "error": "找不到這門課程" }), 404

    return jsonify({
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "teacher": course.teacher,
        "price": course.price
    }), 200