from pymongo import MongoClient
#from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError, BulkWriteError, OperationFailure, ConnectionFailure, ServerSelectionTimeoutError

class MongoPractise():
	
	def __init__(self, host="localhost", port=27017):
		self.client = MongoClient(host, port)

		try:
			self.client.admin.command('ismaster')
		except (ConnectionFailure, ServerSelectionTimeoutError) as ex:
			print("The server is not available. The error code is {}".format(ex))

	def single_insert(self, uid, uname=None, upwd=None, uinfo=[]):
		user = {}
		user['_id'] = uid
		user['uname'] = uname
		user['upwd'] = upwd
		user['uinfo'] = uinfo

		try:
			self.coll.insert_one(user)
		except DuplicateKeyError:
			print("record with id={} is already exist, considering using update_by_id to change this record.".format(uid))
			return False
		except OperationFailure:
			print("internal error!")
			return False 
		return True


	def multiple_insert(self, users):
		#users is a list of dict
		try:
			self.coll.insert_many(users)
		except BulkWriteError:
			print("Keys are already exist, considering using update_by_id to change this record.")
			return False
		except OperationFailure:
			print("internal error!")
			return False 
		return True
		

	def delete_by_id(self, uid):
		r = self.coll.delete_one({"_id": uid})
		return r.deleted_count 

	def update_by_id(self, new_data):
		uid = new_data['_id']
		r = self.coll.replace_one({"_id": uid}, new_data, True)
		return r.modified_count 

	def get_by_id(self, uid):
		res = self.coll.find({"_id": uid})
		if res.count() == 1:
			return res[0]
		return None

	def count_total_records(self):
		return self.coll.find().count()
	# def delete_by_field(self, field):
	# 	pass

	# def update_by_field(self, field):
	# 	pass

	# def get_by_field(self, field):
	# 	pass

	def connect_to_db(self, db_name):
		flag = 1
		dbs = self.client.database_names()
		for each in dbs:
			if db_name == each:
				self.db = self.client[db_name]
				#flag = 0
				#break
				return True
		if flag:
			print("The {} is not exist!".format(db_name))
			return False

	def connect_to_collection(self, coll_name):
		flag = 1
		colls = self.db.collection_names()
		for each in colls:
			if coll_name == each:
				self.coll = self.db[coll_name]
				#flag = 0
				return True		
		if flag:
			print("The {} is not exist!".format(coll_name))
			return False

	def create_db(self, db_name):
		dbs = self.client.database_names()
		flag = 1
		for each in dbs:
			if db_name == each:
				print("The {} is already exist!".format(db_name))
				flag = 0
				return False		
		if flag:
			self.db = self.client[db_name]
			return True

	def create_collection(self, coll_name):
		flag = 1
		colls = self.db.collection_names()
		for each in colls:
			if coll_name == each:
				print("The {} is already exist!".format(coll_name))
				flag = 0
				return False		
		if flag:
			self.coll = self.db[coll_name]
			return True

	def show_content_by_id(self, uid):
		import pprint
		for each in self.coll.find({"_id": uid}):
			pprint.pprint(each)

	def shut_down(self):
		self.client.close()

