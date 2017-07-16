import sys
#use linux style
sys.path.append("class/")

import unittest
from MyStack import MyStack
import time
import timeout_decorator

class MyStackTest(unittest.TestCase):
	def setUp(self):
		self.start_time = time.perf_counter()
		self.stack = MyStack()

	def tearDown(self):
		t = time.perf_counter() - self.start_time
		if t < 0.1:
			t = t * 1000
			print("{}: {:.3f}ms".format(self.id(), t))
		else:
			print("{}: {:.3f}s".format(self.id, t))
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
	@timeout_decorator.timeout(0.3)
	def test_large_num_push_pop(self):
		for i in range(100001):
			self.stack.push(i)

		for i in range(100000, 0, -1):
			self.assertEqual(i, self.stack.pop())
			self.assertFalse(self.stack.is_empty())

		self.stack.pop()
		self.assertTrue(self.stack.is_empty())

		with self.assertRaises(IndexError):
			self.stack.pop()

if __name__ == '__main__':
	unittest.main()