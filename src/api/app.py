#app
import os
import json
import jsonschema
from datetime import timedelta
from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
import schema_validator
from db_connect import Connect
from todo_list import TodoList
from gbl_variables import host, port

# configuration
DEBUG = True

# Paths
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# JWT Configs
app.config['JWT_SECRET_KEY'] = "asdkjahsd^*&^"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=455)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=455)
jwt = JWTManager(app)

# Enable CORS
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

conn = Connect()
mongo = conn.get_mongodb_connection()

def api_count_tracker(api_name = '/'):
	print('inside api count tracker')
	def decorator(func):
		print('inside decorator')
		result = mongo.api_count_tracker.find_one_and_update({'api_name': api_name}, {'$inc': {'count': 1}})
		if not result:
			mongo.api_count_tracker.insert_one({'api_name': api_name, 'count': 1})
		def update_counter():
			return func()
		return update_counter
	return decorator


@api_count_tracker(api_name='/')
@app.route('/')
def version_info():
    return jsonify([{'Version': '1.0.0', 'service detail': 'ToDo list service'}])
	

@api_count_tracker(api_name='/signin')
@app.route('/signin', methods=['POST'])
def signin():
	request_data = request.get_json()
	username = request_data['username']
	password = request_data['password']
	conn = Connect()
	mongodb = conn.get_mongodb_connection()
	validated_user = list(mongodb.user_manager.find({'username': username}, {"_id": 0}))
	conn.close_connection()
	if validated_user:
		if validated_user[0]['password'] != password:
			return jsonify({"msg": "Invalid password"}), 401
	else:
		return jsonify({"msg": "Invalid username"}), 401

	access_token = create_access_token(identity=username)

	return jsonify(access_token=access_token)


@api_count_tracker(api_name='/todo')
@app.route('/todo', methods=['GET', 'POST'])
@jwt_required()
def todo_list():
	if request.method == 'GET':
		current_user = get_jwt_identity()
		conn = Connect()
		mongodb = conn.get_mongodb_connection()
		tl = TodoList(mongodb)
		result = tl.get_tasks()
		conn.close_connection()
		return result
	elif request.method == 'POST':
		current_user = get_jwt_identity()
		try:
			request_data = request.get_json()
		except Exception as e:
			print(e)
			return jsonify({'message': 'invalid data'}), 422
		try:
			jsonschema.validate(request_data, schema_validator.TODO)
		except jsonschema.exceptions.ValidationError as val_err:
			return make_response(str(val_err), 400)
		conn = Connect()
		mongodb = conn.get_mongodb_connection()
		tl = TodoList(mongodb)
		result = tl.add_task(request_data)
		conn.close_connection()

		return result


if __name__ == '__main__':
    app.run(host = host, port = port)
