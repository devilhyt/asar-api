from wingman_api.main import db
from pydantic import BaseModel
from typing import Optional

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
class UserSchema(BaseModel):
    id : Optional[int]
    username : str
    password : str

def init():
    db.create_all()
    db.session.add(User(username="admin", password="admin"))
    db.session.add(User(username="user", password="user"))
    db.session.commit()
