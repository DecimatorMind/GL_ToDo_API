from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from resources.users import User_Login, Users, Login_Check
from resources.tasks import Tasks, Daywise

app = Flask(__name__)
api = Api(app)

secret_key = "GlueLabs"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/ToDoAPI_GL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zwkyozttqbjolj:025b9d9677e8ce2a41782fca237d09ac2723ca9c2787faa9257641a30a3465e5@ec2-34-230-153-41.compute-1.amazonaws.com:5432/d3fls186trme57'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api.add_resource(Users,'/register')
api.add_resource(User_Login,'/login')
api.add_resource(Tasks,'/tasks')
api.add_resource(Daywise,'/daywise')

@app.route("/")
def home():
    return jsonify({"status":"OK"})

if __name__ == "__main__":
    app.run()