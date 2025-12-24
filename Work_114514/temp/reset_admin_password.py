import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models.models import db, User
from werkzeug.security import generate_password_hash

NEW_PASSWORD = "admin123"

with app.app_context():
    admin = User.query.filter_by(account="admin").first()
    if not admin:
        print("admin 用户不存在")
    else:
        admin.password = generate_password_hash(NEW_PASSWORD)
        db.session.commit()
        print("admin 密码已重置为：admin123")

# 请确保在运行此脚本之前，已经正确配置了 Flask 应用和数据库连接。
# 该脚本会检查是否存在 account 为 "admin" 的用户，如果存在，则将该用户的密码重置为 "admin123"。
# 请谨慎使用此脚本，确保在安全的环境中运行，并备份重要数据。
# python temp/reset_admin_password.py,在项目根目录下执行该脚本以重置 admin 用户的密码。