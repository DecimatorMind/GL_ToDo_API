# yorec77612@bamibi.com


# @app.route("/reorder",methods = ["GET"])
# def reorder():
#     token = request.headers.get("Authorization").split(" ")
#     token = token[1]
#     if(token == None):
#         return make_response(jsonify({'status' : 'Invalid Token'}),400)
#     try:
#         payload = jwt.decode(token, secret_key, algorithms=["HS256"])
#         userId = payload['public_id']
#         tasks = Tasks.query.filter_by(user_id = userId).order_by(Tasks.last_date.asc())
#         if(tasks == None):
#             return make_response(jsonify({'status': 'No Task Found'}),200)
#         else:
#             new_index = 0
#             result = {}
#             for i in tasks:
#                 if(i.deleted == False):
#                     i.user_order = new_index
#                     new_index += 1
#                     result[i.id] = {"title":i.title,"description": i.description,"user_id":i.user_id,"completed":i.completed,"last_date":i.last_date,"last_update":i.last_update,"user_order": i.user_order}
#             try:
#                 db.session.commit()
#                 return make_response(jsonify({"status":"Successfully Reordered Items"}),200)
#             except:
#                 db.session.rollback()
#                 return make_response(jsonify({"status":"Error in Writing to Database"}),400)
#             finally:
#                 db.session.close()
#                 return make_response(jsonify(result),200)
#     except:
#         return make_response(jsonify({'status' : 'Token Expired'}),400)