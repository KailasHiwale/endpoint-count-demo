from pymongo import MongoClient
from gbl_variables import db_connection_string, dbname


#mongodb://localhost:27017


class Connect():
	"""Doc string"""
	def __init__(self):
		self.db_connection_string = db_connection_string
		self.client = MongoClient(self.db_connection_string)

	def get_mongodb_connection(self):
		db_conn = self.client[dbname]
		return db_conn

	def close_connection(self):
		self.client.close()
		return True