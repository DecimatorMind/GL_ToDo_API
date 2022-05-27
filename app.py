from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from resources.users import User_Login, Users
from resources.tasks import Tasks, Daywise

app = Flask(__name__)
api = Api(app)

secret_key = "GlueLabs"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/ToDoAPI_GL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api.add_resource(Users,'/register')
# api.add_resource(User_Login,'/login')
api.add_resource(Tasks,'/tasks')
api.add_resource(Daywise,'/daywise')

@app.route("/")
def home():
    return jsonify({"status":"OK"})

@app.route("/login")
def login():
    return "Login"

if __name__ == "__main__":
    app.run()