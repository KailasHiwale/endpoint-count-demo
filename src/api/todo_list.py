from flask import jsonify
import random


class TodoList(object):
	"""doc string"""
	def __init__(self, db):
		self.db = db
	
	def get_tasks(self):
		"""doc string"""
		data = None
		try:
			data = [{k: v for k, v in doc.items() if k != '_id'} for doc in self.db.task_manager.find()]
		except Exception as e:
			print(e)
		return jsonify({'success': True, 'data': data}), 200

	def add_task(self, request_data):
		"""doc string"""
		id = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
		status = request_data['status']
		date = request_data['date']
		task = request_data['task']
		response = {'success': True, 'msg': 'Success'}
		try:
			self.db.task_manager.insert_one(data)
		except Exception as e:
			response = {'success': True, 'msg': 'Failed'}
		
		return jsonify(response), 200