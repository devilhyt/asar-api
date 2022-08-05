from typing import Optional
from pydantic import BaseModel, Extra
from wingman_api.public import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
class UserSchema(BaseModel, extra=Extra.forbid):
    id : Optional[int]
    username : str
    password : str

def init():
    db.session.add(User(username="admin", password="admin"))
    db.session.add(User(username="user", password="user"))
    db.session.commit()
