"""This module does blah blah."""
import unittest
#we can use nose tools in unittest
import time
from nose.tools import timed
from uclass.MyStack import MyStack
#import timeout_decorator
# import sys
#use linux style
# sys.path.append("../uclass/")
# from MyStack import MyStack

class MyStackTest(unittest.TestCase):
	def setUp(self):
		self.start_time = time.perf_counter()
		self.stack = MyStack()

	def tearDown(self):		
		t = time.perf_counter() - self.start_time
		test_id = self.id().split(".")[-1]
		
		if t < 0.1:
			t = t * 1000
			print("{}: {:.3f}ms".format(test_id, t))
		else:
			print("{}: {:.3f}s".format(test_id, t))
		#self.stack.clear()

	def test_push_peek(self):
		self.stack.push("right")
		self.assertEqual(self.stack.peek(), "right")

	def test_push_pop_emptycheck(self):
		self.stack.push(1)
		num = self.stack.pop()
		self.assertEqual(num, 1)
		self.assertTrue(self.stack.is_empty())

	# only work under linux because of SIGALRM not work in windows
	#@timeout_decorator.timeout(0.5)
	@timed(10)
	def test_large_num_push_pop(self):
		for i in range(100001):
			self.stack.push(i)

		for i in range(100000, 0, -1):
			#without using subTest, the test will stop when the first fail happened
			#with subTest, all test will be performed and failure ones will be presented separately
			# if i == 9983:
			# 	i += 1
			with self.subTest(i = i):
				self.assertEqual(i, self.stack.pop())
				self.assertFalse(self.stack.is_empty())

		self.stack.pop()
		self.assertTrue(self.stack.is_empty())

		with self.assertRaises(IndexError):
			self.stack.pop()

		# with self.assertRaises(IndexError) as sr:
		# 	self.stack.pop()
		# the_exception = sr.exception
		# self.assertEqual(the_exception.error_code, 3)

if __name__ == '__main__':
	unittest.main()