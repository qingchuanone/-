import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError
from models.models import db, User

@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://flask_user:Flask.114514@120.24.149.69/DB_1919810?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.init_app(app)

    with app.app_context():
        yield app


@pytest.fixture(autouse=True)
def session(app):
    """
    自动提供 db.session
    """
    with app.app_context():
        yield db.session
        # 测试完成后清理测试数据
        db.session.query(User).filter(
            User.account.in_(["pytest_mysql_user", "pytest_duplicate"])
        ).delete(synchronize_session=False)
        db.session.commit()


def test_create_user_mysql():
    user = User(account="pytest_mysql_user", password="123456", role="admin")
    db.session.add(user)
    db.session.commit()

    result = User.query.filter_by(account="pytest_mysql_user").first()
    assert result is not None
    assert result.account == "pytest_mysql_user"
    assert result.role == "admin"


def test_unique_account_mysql():
    user1 = User(account="pytest_duplicate", password="111", role="user")
    user2 = User(account="pytest_duplicate", password="222", role="user")

    db.session.add(user1)
    db.session.commit()

    db.session.add(user2)
    with pytest.raises(IntegrityError):
        db.session.commit()
    # 捕获异常后，必须回滚 session，避免 PendingRollbackError
    db.session.rollback()