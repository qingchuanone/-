from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.models import User,db
from app import app


"""
获取所有的用户信息
"""
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    result = [{"id": u.id, "account": u.account, "role": u.role} for u in users]
    return jsonify(result)



"""
用于登录的接口
"""
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # 1. 判断请求体是否为空
    if not data:
        return jsonify({"msg": "请求体不能为空"}), 400

    # 2. 获取参数
    account = data.get("account")
    password = data.get("password")

    # 3. 判断参数是否为空
    if not account or not password:
        return jsonify({"msg": "account 和 password 不能为空"}), 400

    # 4. 根据 account 查询用户
    user = User.query.filter_by(account=account).first()

    # 5. 用户不存在
    if not user:
        return jsonify({"msg": "账号或密码错误"}), 401

    # 6. 校验加密密码（关键点）
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "账号或密码错误"}), 401

    # 7. 登录成功
    return jsonify({
        "msg": "登录成功",
        "user": {
            "id": user.id,
            "account": user.account,
            "role": user.role
        }
    }), 200


"""
用户注册 / 新增接口
"""
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # 1. 判断请求体是否为空
    if not data:
        return jsonify({"msg": "请求体不能为空"}), 400

    # 2. 获取参数
    account = data.get("account")
    password = data.get("password")
    role = data.get("role", "user")  # 默认普通用户

    # 3. 判断参数是否为空
    if not account or not password:
        return jsonify({"msg": "account 和 password 不能为空"}), 400

    # 4. 判断账号是否已存在
    exist_user = User.query.filter_by(account=account).first()
    if exist_user:
        return jsonify({"msg": "账号已存在"}), 409

    # 5. 密码加密
    password_hash = generate_password_hash(password)

    # 6. 创建新用户
    new_user = User(
        account=account,
        password=password_hash,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "注册成功"}), 200


"""删除用户接口"""
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    删除用户接口，只有管理员可以操作
    需要在请求头中传入管理员账号和密码进行认证
    """
    auth = request.get_json()
    if not auth:
        return jsonify({"msg": "请求体不能为空"}), 400

    admin_account = auth.get("account")
    admin_password = auth.get("password")

    if not admin_account or not admin_password:
        return jsonify({"msg": "账号和密码不能为空"}), 400

    # 验证管理员身份
    admin = User.query.filter_by(account=admin_account).first()
    if not admin or admin.role != "admin" or not check_password_hash(admin.password, admin_password):
        return jsonify({"msg": "权限不足或账号密码错误"}), 403

    # 查询要删除的用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "用户不存在"}), 404

    # 删除用户
    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": f"用户 {user.account} 已删除"}), 200