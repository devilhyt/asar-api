from project.public import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

def init():
    db.create_all()
    db.session.add(User(username="admin", password="admin"))
    db.session.add(User(username="user", password="user"))
    db.session.commit()
