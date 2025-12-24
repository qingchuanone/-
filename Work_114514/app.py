from flask import Flask
from models.models import db

app = Flask(__name__)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://flask_user:Flask.114514@120.24.149.69/DB_1919810?charset=utf8mb4"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# 导入路由，不放在开头是为了避免循环导入？    
import routes


if __name__ == "__main__":
    app.run(debug=True)
