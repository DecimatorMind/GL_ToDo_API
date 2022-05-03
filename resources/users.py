from flask_restful import Resource, reqparse
from flask import request, make_response, jsonify
from models.users import Users as DbUser
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary.uploader

cloudinary.config(
  cloud_name = "dxr7lcjmd",
  api_key = "643921477167134",
  api_secret = "z9WyxtR6Io6ACEQsA_yylzxfk68")

class Users(Resource):
    def post(self):
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        password = generate_password_hash(request.form.get('password'))
        new_user = DbUser(name = user_name,email = user_email,password = password)
        if DbUser.find_by_username(user_name):
            return {"message": 'A user with username {} already exists.'.format(user_name)}, 400
        try:
            new_user.save_to_db()
            data = request.files["display_picture"]
            cloudinary.uploader.upload(data,public_id = user_email)
        except:
            return make_response(jsonify({"error":"Error in adding User to Database"}),400)
        return {"message": "User created successfully."}, 200