import unittest
from unittest.mock import patch
import sys
sys.path.append("../uclass/")
from MockTest import Real
from MockTest import Upload
from MockTest import SimpleFacebook
import os.path
import tempfile
import unittest.mock as mock


class TestWithMockReal(unittest.TestCase):
	def setUp(self):
		self.real = Real()
		#all code below is required for traditional test
		self.tmp_file_path = os.path.join(tempfile.gettempdir(), "temp_file_for_test")
		#print(self.tmp_file_path)
		with open(self.tmp_file_path, "w") as f:
			print("delete me!", file=f, end='\n') 

	def tearDown(self):
		#need in case the rm method failed
		if os.path.isfile(self.tmp_file_path):
			os.remove(self.tmp_file_path)

	#using mock to simulate the fuction call (this test proved that using rm will call os.remove method) 
	@patch('MockTest.os')
	def test_rm_with_mock(self, mock_os):
		self.real.rm('any file')
		mock_os.remove.assert_called_with('any file')
		#self.assertTrue(mock_os.remove.called, "should call the remove method")

	#same test in tradtional way, only proved that the file has been create and deleted
	def test_rm_without_mock(self):
		self.assertTrue(os.path.isfile(self.tmp_file_path), "the temp file is not created.")
		self.real.rm(self.tmp_file_path)
		self.assertFalse(os.path.isfile(self.tmp_file_path), "the method is failed to remove file.")

	#handle if condition
	@patch('MockTest.os.path')
	@patch('MockTest.os')
	def test_rm1_with_mock(self, mock_os, mock_path):
		#the if condtion is false in rm1
		#set up os.path.isfile method return value
		mock_path.isfile.return_value = False
		self.real.rm1('any false')
		self.assertFalse(mock_os.remove.called, 'the file is not exist, so this method should not be called')

		#the if condtion is true in rm1
		#make the isfile return True to test the case when the remove method has been called
		mock_path.isfile.return_value = True
		self.real.rm1('any true')
		mock_os.remove.assert_called_with('any true')
		#self.assertTrue(mock_os.remove.called, 'the file is exist, the method should be called')

class TestWithMockUpload(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.real = Real()
		cls.upload = Upload(cls.real)
		cls.upload.pre_upload('test')

	@patch.object(Real, "rm1")
	def test_postupload(self, mock_rm):
		self.upload.post_upload()
		mock_rm.assert_called_with('test')
		self.assertTrue(mock_rm.called, "the method should be invoked")
		#the mock_rm acctually replace the self.real.rm1 in above assert
		self.real.rm1.assert_called_with('test')
		self.assertTrue(self.real.rm1.called, "the method should be invoked")

	def test_postupload_without_patch(self):
		#create an autospec Real instance which on functionality meets the requirements that upload instance needs from Real
		mock_real = mock.create_autospec(Real)
		ref = Upload(mock_real)
		ref.pre_upload('aaa')
		ref.post_upload()
		mock_real.rm1.assert_called_with('aaa')
		self.assertTrue(mock_real.rm1.called, "the method should be invoked")

#more realistic example
import facebook
class TestSimpleFacebook(unittest.TestCase):
	#use patch object
	#mock the facebook.GraphAPI, so that we do not need to worry the oauth token we use
	#cannot use autospec param in patch.object -> raise error that the actual called put_object is not belong to the class SompleFacebook
	@patch.object(facebook.GraphAPI, "put_object", autospec=False)
	def test_post_msg(self, mock_put_object):
		sf = SimpleFacebook("fake oauth token")
		sf.post_msg("Hello Unittest")

		#verify
		self.assertTrue(mock_put_object.called, "the method should be invoked")
		mock_put_object.assert_called_with("me", "feed", message="Hello Unittest")
		
if __name__ == '__main__':
	unittest.main(verbosity=2)