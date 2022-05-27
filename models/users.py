from flask_sqlalchemy import SQLAlchemy
from collections.abc import Mapping
db = SQLAlchemy()
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    email = db.Column(db.String,unique = True)
    password = db.Column(db.String)

    def __init__(self,name,email,password) -> None:
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_email(cls,user_email):
        return(cls.query.filter_by(email = user_email).first())

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()