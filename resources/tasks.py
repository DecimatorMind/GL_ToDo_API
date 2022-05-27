from encodings import utf_8
from flask_restful import Resource, reqparse
from flask import request, make_response, jsonify
from models.tasks import Tasks as DbTasks
from models.users import Users
import jwt
import datetime

secret_key = "GlueLabs"

def check_token():
    token = request.headers.get("Authorization").split(" ")
    token = token[1]
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        userId = payload['public_id']
        curr_user = Users.query.filter_by(id = userId).first()
        return curr_user
    except:
        return None

def getUserOrder(userId):
    tasks = DbTasks.query.filter_by(user_id = userId)
    order = 0
    for i in tasks:
        order += 1
    return order

class Daywise(Resource):
    def get(self):
        curr_user = check_token()
        curr_user_id = curr_user.id
        date_today = datetime.date.today()
        tasks = DbTasks.query.filter_by(user_id = curr_user_id)
        if(tasks == None):
            return make_response(jsonify({'status': 'No Task Found'}),200)
        else:
            result = {}
            for i in tasks:
                if(date_today == i.last_date and i.deleted == None):
                    result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
            return make_response(jsonify(result),200)

class Tasks(Resource):
    def get(self):
        curr_user = check_token()
        tasks = DbTasks.query.filter_by(user_id = curr_user.id)
        if(tasks == None):
            return make_response(jsonify({'status': 'No Task Found'}),200)
        else:
            result = {}
            for i in tasks:
                if(i.deleted == None):
                    result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
            return make_response(jsonify(result),200)

    def post(self):
        # curr_user = check_token()
        json = request.get_json()
        # curr_user_id = curr_user.id
        curr_user_id = 1
        if(json['user_id'] != curr_user_id):
            return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
        user_order = getUserOrder(curr_user_id)
        date_today = datetime.date.today()
        task = DbTasks(title = json['title'],description = json['description'],user_id = json['user_id'],completed = json['completed'],initial_date = date_today,last_date = date_today+datetime.timedelta(days=json["number_of_days"]),user_order = user_order,last_update = date_today,deleted = None)
        try:
            DbTasks.save_to_db(task)
            return make_response(jsonify({"status":"Successfully Added to Database"}),200)
        except:
            return make_response(jsonify({"status":"Error in adding task to Database"}),400)

    def patch(self):
        curr_user = check_token()
        json = request.get_json()
        curr_user_id = curr_user.id
        if(json['user_id'] != curr_user_id):
            return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
        user = json['user_id']
        taskid = json['id']
        temp = DbTasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
        temp.title = json['title']
        temp.description = json['description']
        temp.completed = json['completed']
        temp.last_date = temp.initial_date + datetime.timedelta(days=json["number_of_days"])
        temp.last_update = datetime.date.today()
        try:
            DbTasks.save_to_db(temp)
            return make_response(jsonify({"status":"Successfully Modified in Database"}),200)
        except:
            return make_response(jsonify({"status":"Error in patching task to Database"}),400)

    def delete(self):
        curr_user = check_token()
        json = request.get_json()
        curr_user_id = curr_user.id
        if(json['user_id'] != curr_user_id):
            return make_response(jsonify({'error' : 'Access Not Allowed'}),401)
        user = json['user_id']
        taskid = json['id']
        temp = DbTasks.query.filter_by(user_id = user).filter_by(id = taskid).first()
        temp.deleted = datetime.date.today()
        temp.user_order = 0
        try:
            DbTasks.save_to_db(temp)
            return make_response(jsonify({"status":"Successfully Deleted from Database"}),200)
        except:
            return make_response(jsonify({"status":"Error in Deleting task to Database"}),400)
