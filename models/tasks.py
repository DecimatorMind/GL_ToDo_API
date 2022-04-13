from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String,nullable = False)
    description = db.Column(db.String,nullable = False)
    user_id = db.Column(db.Integer,nullable = False)
    completed = db.Column(db.Boolean)
    initial_date = db.Column(db.Date,nullable = False)
    last_date = db.Column(db.Date)
    user_order = db.Column(db.Integer,nullable = False)
    last_update = db.Column(db.Date,nullable = False)
    deleted = db.Column(db.Date,nullable = True)

    def __init__(self,title,description,user_id,completed,initial_date,last_date,user_order,last_update,deleted) -> None:
        self.title = title
        self.description = description
        self.user_id = user_id
        self.completed = completed
        self.initial_date = initial_date
        self.last_date = last_date
        self.user_order = user_order
        self.last_update = last_update
        self.deleted = deleted