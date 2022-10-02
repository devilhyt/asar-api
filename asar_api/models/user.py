from typing import Optional
from pydantic import BaseModel, Extra
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)


class UserSchema(BaseModel, extra=Extra.forbid):
    id: Optional[int]
    username: str
    password: str
    
class UserChangePasswordSchema(BaseModel, extra=Extra.forbid):
    password: str
    new_password: str


def init():
    # db.session.add(User(username="admin", password="admin"))
    user = User(username='admin')
    user.set_password('admin')
    db.session.add(user)
    user = User(username='user')
    user.set_password('user')
    db.session.add(user)
    # db.session.add(User(username="user", password="user"))
    db.session.commit()
