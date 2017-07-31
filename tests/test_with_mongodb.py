import sys
sys.path.append("../uclass/")
from MongoPractise import MongoPractise
import unittest
from nose.tools import nottest
from nose.tools import timed

class TestMongoDB(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		cls.mp = MongoPractise()
	
	@classmethod
	def tearDownClass(cls):
		cls.mp.shut_down()

	def setUp(self):
		self.mp.db = self.mp.client['tempDB']
		self.mp.coll = self.mp.db['tempColl']
		self.mp.coll.insert_one({"test" : 1, "_id" : 0})

	def tearDown(self):
		self.mp.client.drop_database('tempDB')

	@nottest
	@timed(1)
	def test_connect_to_db(self):
		#exist case
		db_name_pos = "course"
		return_value = self.mp.connect_to_db(db_name_pos)
		self.assertTrue(return_value)

		#not exist case
		db_name_neg = "notexist"
		return_value = self.mp.connect_to_db(db_name_neg)
		self.assertFalse(return_value)

	@timed(1)
	def test_connect_to_coll(self):
		#set up a correct db
		db_name_pos = "tempDB"
		self.mp.connect_to_db(db_name_pos)

		#exist case
		coll_name_pos = "tempColl"
		return_value = self.mp.connect_to_collection(coll_name_pos)
		self.assertTrue(return_value)

		#not exist case
		coll_name_neg = "notexist"
		return_value = self.mp.connect_to_collection(coll_name_neg)
		self.assertFalse(return_value)

	def test_create_db(self):
		#positive test
		db_name = "test_create"
		r = self.mp.create_db(db_name)
		self.assertTrue(r)

		#negative_test
		db_name1 = "tempDB"
		r = self.mp.create_db(db_name1)
		self.assertFalse(r)

		self.mp.client.drop_database(db_name)
	
	def test_create_collection_and_insert(self):
		db_name = "test_create"
		self.mp.create_db(db_name)
		collection_name = "test_create_coll"
		self.mp.create_collection(collection_name)
		self.mp.single_insert(1)

		try:
			i = 0
			for each in self.mp.client.database_names():
				#print(each)
				if each == db_name:
					i += 1
			self.assertEqual(1, i)
		finally:
			self.mp.client.drop_database(db_name)

	def test_insert_delete_count(self):
		#positive test
		r1 = self.mp.single_insert(1, "alex", "1234")
		self.assertTrue(r1)

		r2 = self.mp.single_insert(2, "beto", "2345", ["xx", "yy"])
		self.assertTrue(r2)

		n1 = self.mp.count_total_records()
		self.assertEqual(3, n1)

		r3 = self.mp.delete_by_id(0)
		self.assertEqual(1, r3)

		n2 = self.mp.count_total_records()
		self.assertEqual(2, n2)

		#negtive test
		r4 = self.mp.single_insert(2, "alex", "2345")
		self.assertFalse(r4)

		n3 = self.mp.count_total_records()
		self.assertEqual(2, n3)

		r5 = self.mp.delete_by_id(4)
		self.assertEqual(0, r5)

		n4 = self.mp.count_total_records()
		self.assertEqual(2, n4)

	def test_insert_update_get(self):
		data = [{"_id": 1, "uname": "alex", "upwd": "1234"}, {"_id": 2, "uname": "alex1", "upwd": "12345"}]
		replace_data = {"_id": 1, "uname": "alex", "upwd": "4321"}
		#positive test
		r1 = self.mp.multiple_insert(data)
		self.assertTrue(r1)

		# for each in self.mp.coll.find():
		# 	print(each)

		r2 = self.mp.get_by_id(1)
		self.assertFalse(r2 == None)
		self.assertEqual("alex", r2['uname'])
		self.assertEqual("1234", r2['upwd'])

		r3 = self.mp.update_by_id(replace_data)
		#print(r3)
		self.assertEqual(1, r3)

		r4 = self.mp.get_by_id(1)
		self.assertNotEqual("1234", r4['upwd'])
		self.assertEqual("4321", r4['upwd'])

	def test_show(self):
		from io import StringIO
		sys.stdout = StringIO()
		self.mp.show_content_by_id(0) #{'_id': 0, 'test': 1}
		output = sys.stdout.getvalue().strip()
		self.assertEqual(output, "{'_id': 0, 'test': 1}")

if __name__ == '__main__':
	unittest.main()
