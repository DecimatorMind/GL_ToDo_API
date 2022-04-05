from enum import unique
import datetime
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
secret_key = "GlueLabs"
# secret_key = "your-256-bit-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/ToDoAPI_GL'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    email = db.Column(db.String,unique = True)
    password = db.Column(db.String)
    token = db.Column(db.String,unique = True,nullable = False)

class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    task = db.Column(db.String,nullable = False)
    user_id = db.Column(db.Integer,nullable = False)
    completed = db.Column(db.Boolean)

db.create_all()

# task = Tasks(id = 1,task = "Test Task",user_id = 1,completed = False)
# db.session.add(task)
# try:
#     db.session.commit()
# except:
#     db.session.rollback()
# finally:
#     db.session.close()

# sample_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjEsImV4cCI6MTY0ODkwOTM2N30.PW8KrXIdFrUblLN4X_OhleyRuVK7uc-81rZrjc1yUd0'
# user = Users(id = 1,name = 'Test Name',email = 'Test Email',password = 'Password',token = sample_token)
# db.session.add(user)
# try:
#     db.session.commit()
# except:
#     db.session.rollback()
# finally:
#     db.session.close()

@app.route("/")
def home():
    return jsonify({"status":"OK"})

@app.route("/register",methods = ["POST"])
def register():
    data = request.get_json()
    token = jwt.encode({"email" : data["email"],"password" : data["password"]},secret_key, "HS256")
    new_user = Users(id = data["id"],name = data["name"],email = data["email"],password = data["password"],token = token)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"status":"Successfully Added to Database"})
    except:
        db.session.rollback()
        return jsonify({"error":"Error in adding task to Database"})
    finally:
        db.session.close()
        return jsonify({"status":"Request Recieved"})

@app.route('/check',methods = ["POST"])
def check():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    if(token == None):
        return jsonify({'status' : 'Invalid Token'})
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        print(payload)
        return jsonify({"check":"Successful"})
    except jwt.exceptions.ExpiredSignatureError:
        return jsonify({"error" : "Token Expired"})
    except:
        return jsonify({'status' : 'Unkown Error'})

@app.route('/login',methods = ["POST"])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if data == None or email == None or password == None:
        return jsonify({'status' : 'Data not complete'})
    user = Users.query.filter_by(email = email).first()
    if(user != None):
        if(user.password == password):
            token = jwt.encode({'public_id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=2)}, secret_key, "HS256")
            return jsonify({'token' : token})
        else:
            return jsonify({'status': 'Wrong password entered'})
    else:
        return jsonify({'status' : 'No such user exists'})

# def getUser():


@app.route('/tasks',methods = ["GET","POST","PATCH","DELETE"])
def tasks():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    if(token == None):
        return jsonify({'status' : 'Invalid Token'})
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        userId = payload['public_id']
        if(request.method == "GET"):
            tasks = Tasks.query.filter_by(user_id = userId)
            if(tasks == None):
                return jsonify({'status': 'No Task Found'})
            else:
                result = {}
                for i in tasks:
                    result[i.id] = i.task
                return jsonify(result)
        elif (request.method == "POST"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return jsonify({'error' : 'Access Not Allowed'})
                task = Tasks(id = json['id'],task = json['task'],user_id = json['user_id'],completed = json['completed'])
                db.session.add(task)
                try:
                    db.session.commit()
                    return "Successfully Added to Database"
                except:
                    db.session.rollback()
                    return "Error in adding task to Database"
                finally:
                    db.session.close()
                    return "Request Recieved"
            else:
                return "Content Type not Supported"
        elif (request.method == "PATCH"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return jsonify({'error' : 'Access Not Allowed'})
                user = json['user_id']
                taskid = json['id']
                temp = Tasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
                temp.task = json['task']
                temp.completed = json['completed']
                try:
                    db.session.commit()
                    return "Successfully Modified in Database"
                except:
                    db.session.rollback()
                    return "Error in patching task to Database"
                finally:
                    db.session.close()
                    return "Patch Request Recieved"
            else:
                return "Content Type not Supported"
        elif (request.method == "DELETE"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return jsonify({'error' : 'Access Not Allowed'})
                user = json['user_id']
                taskid = json['id']
                temp = Tasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
                db.session.delete(temp)
                try:
                    db.session.commit()
                    return "Successfully Deleted from Database"
                except:
                    db.session.rollback()
                    return "Error in Deleting task to Database"
                finally:
                    db.session.close()
                    return "Delete Request Recieved"
            else:
                return "Content Type not Supported"
    except:
        return jsonify({'status' : 'Token Expired'})

if __name__ == "__main__":
    app.run()