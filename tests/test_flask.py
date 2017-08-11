import sys
sys.path.append("../uclass/")
from simple_flask_login import app
import unittest
# import os
from pymongo import MongoClient

class SimpleFlaskAppTest(unittest.TestCase):
	'''
	This test is desgined only for travisCI test for now, because the db will be removed after test
	In production, run test might cause data lost
	'''
	#config
	@classmethod
	def setUpClass(self):
		# app.config['MONGO_URI'] = "mongodb://localhost:27017"
		self.app = app.test_client()
		self.app.testing = True
		self.client = MongoClient("localhost:27017")
		self.client.simple_flask_login.users.insert_one({"_id": "aaa", "password": "bbb"})

	@classmethod
	def tearDownClass(self):
		self.client.drop_database('simple_flask_login')
		self.client.close()

	# test
	def test_index_status_code(self):
		result = self.app.get('/')
		self.assertEqual(200, result.status_code)

	def test_login(self):
		result = self.app.post('/login', data=dict(username="aaa", password="bbb"), follow_redirects=True)
		self.assertEqual(200, result.status_code)
		self.assertIn("Hello Boss", str(result.data))

	def test_signup(self):
		result1 = self.app.get('/signup')
		self.assertEqual(200, result1.status_code)

		self.app.post('/signup', data=dict(username="ccc", password="ddd"))
		res = self.client.simple_flask_login.users.find_one({"_id": "ccc"})
		self.assertEqual(res["password"], "ddd")

if __name__ == '__main__':
	unittest.main()