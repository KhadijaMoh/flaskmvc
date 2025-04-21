from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from ..models.user import User
from flask_login import login_user

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return False, "That username is already taken."
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True, new_user

def login_user_controller(username, password, remember):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return True, user
    return False, None