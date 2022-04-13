import datetime
from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary.uploader
from flask_migrate import Migrate
from models.users import Users
from models.tasks import Tasks

app = Flask(__name__)

# yorec77612@bamibi.com

secret_key = "GlueLabs"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/ToDoAPI_GL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.create_all()

def getUserOrder(userId):
    tasks = Tasks.query.filter_by(user_id = userId)
    order = 0
    for i in tasks:
        order += 1
    return order

cloudinary.config(
  cloud_name = "dxr7lcjmd",
  api_key = "643921477167134",
  api_secret = "z9WyxtR6Io6ACEQsA_yylzxfk68")

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
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    password = generate_password_hash(request.form.get('password'))
    new_user = Users(name = user_name,email = user_email,password = password)
    db.session.add(new_user)
    try:
        db.session.commit()
        data = request.files["display_picture"]
        cloudinary.uploader.upload(data,public_id = user_email)
        return make_response(jsonify({"status" : "Successfully Added to Database"}),201)
    except:
        db.session.rollback()
        return make_response(jsonify({"error":"Error in adding task to Database"}),400)
    finally:
        db.session.close()
        return make_response(jsonify({"status":"Request Recieved"}),200)

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
        return make_response(jsonify({'status' : 'Data not complete'}),400)
    user = Users.query.filter_by(email = email).first()
    if(user != None):
        if check_password_hash(user.password, password):
            token = jwt.encode({'public_id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, secret_key, "HS256")
            return make_response(jsonify({'token' : token}),200)
        else:
            return make_response(jsonify({'status': 'Wrong password entered'}),400)
    else:
        return make_response(jsonify({'status' : 'No such user exists'}),400)

@app.route('/tasks',methods = ["GET","POST","PATCH","DELETE"])
def tasks():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    if(token == None):
        return make_response(jsonify({'status' : 'Invalid Token'}),400)
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        userId = payload['public_id']
        if(request.method == "GET"):
            tasks = Tasks.query.filter_by(user_id = userId)
            if(tasks == None):
                return make_response(jsonify({'status': 'No Task Found'}),200)
            else:
                result = {}
                for i in tasks:
                    if(i.deleted == False):
                        result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
                return make_response(jsonify(result),200)
        elif (request.method == "POST"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
                user_order = getUserOrder(userId)
                date_today = datetime.date.today()
                task = Tasks(title = json['title'],description = json['description'],user_id = json['user_id'],completed = json['completed'],initial_date = date_today,last_date = date_today+datetime.timedelta(days=json["number_of_days"]),user_order = user_order,last_update = date_today,deleted = None)
                db.session.add(task)
                try:
                    db.session.commit()
                    return make_response(jsonify({"status":"Successfully Added to Database"}),200)
                except:
                    db.session.rollback()
                    return make_response(jsonify({"status":"Error in adding task to Database"}),400)
                finally:
                    db.session.close()
                    return make_response(jsonify({"status":"Request Recieved"}),200)
            else:
                return make_response(jsonify({"status":"Content Type not Supported"}),200)
        elif (request.method == "PATCH"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
                user = json['user_id']
                taskid = json['id']
                temp = Tasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
                temp.title = json['title']
                temp.description = json['description']
                temp.completed = json['completed']
                temp.last_date = temp.initial_date + datetime.timedelta(days=json["number_of_days"])
                temp.last_update = datetime.date.today()
                try:
                    db.session.commit()
                    return make_response(jsonify({"status":"Successfully Modified in Database"}),200)
                except:
                    db.session.rollback()
                    return make_response(jsonify({"status":"Error in patching task to Database"}),400)
                finally:
                    db.session.close()
                    return make_response(jsonify({"status":"Patch Request Recieved"}),200)
            else:
                return make_response(jsonify({"status":"Content Type not Supported"}),200)
        elif (request.method == "DELETE"):
            content = request.headers.get('Content-Type')
            if(content == 'application/json'):
                json = request.get_json()
                if(json['user_id'] != userId):
                    return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
                user = json['user_id']
                taskid = json['id']
                temp = Tasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
                temp.deleted = datetime.date.today()
                temp.user_order = 0
                try:
                    db.session.commit()
                    reorder()
                    return make_response(jsonify({"status":"Successfully Deleted from Database"}),200)
                except:
                    db.session.rollback()
                    return make_response(jsonify({"status":"Error in Deleting task to Database"}),400)
                finally:
                    db.session.close()
                    return make_response(jsonify({"status": "Delete Request Recieved"}),200)
            else:
                return make_response(jsonify({"status": "Content Type not Supported"}),200)
    except:
        return make_response(jsonify({'status' : 'Token Expired'}),400)

@app.route("/daywise",methods = ["GET"])
def daywiseTasks():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    if(token == None):
        return make_response(jsonify({'status' : 'Invalid Token'}),400)
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        userId = payload['public_id']
        if(request.method == "GET"):
            date_today = datetime.date.today()
            tasks = Tasks.query.filter_by(user_id = userId)
            if(tasks == None):
                return make_response(jsonify({'status': 'No Task Found'}),200)
            else:
                result = {}
                for i in tasks:
                    if(date_today == i.last_date and i.deleted == False):
                        result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
                return make_response(jsonify(result),200)
    except:
        return make_response(jsonify({'status' : 'Token Expired'}),400)

@app.route("/reorder",methods = ["GET"])
def reorder():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    if(token == None):
        return make_response(jsonify({'status' : 'Invalid Token'}),400)
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        userId = payload['public_id']
        tasks = Tasks.query.filter_by(user_id = userId).order_by(Tasks.last_date.asc())
        if(tasks == None):
            return make_response(jsonify({'status': 'No Task Found'}),200)
        else:
            new_index = 0
            result = {}
            for i in tasks:
                if(i.deleted == False):
                    i.user_order = new_index
                    new_index += 1
                    result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
            try:
                db.session.commit()
                return make_response(jsonify({"status":"Successfully Reordered Items"}),200)
            except:
                db.session.rollback()
                return make_response(jsonify({"status":"Error in Writing to Database"}),400)
            finally:
                db.session.close()
                return make_response(jsonify(result),200)
    except:
        return make_response(jsonify({'status' : 'Token Expired'}),400)

if __name__ == "__main__":
    app.run()