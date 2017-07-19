import unittest
import sys
#use linux style
sys.path.append("../uclass/")
from RPNCalculator import RPNCalculator
import time
from MyStack import MyStack

class RPNCalculatorTest(unittest.TestCase):
	calc = None

	def setUp(self):
		self.calc = RPNCalculator()

	def test_add2(self):
		self.calc.input_work("1 2 +")
		self.assertEqual(self.calc.get_result(), 3)

	def test_multiple2(self):
		self.calc.input_work("3 2 *")
		self.assertEqual(self.calc.get_result(), 6)

	def test_minus2(self):
		self.calc.input_work("1.5 2.3 -")
		#self.assertEqual(round(self.calc.get_result(), 2), -0.8)
		self.assertAlmostEqual(self.calc.get_result(), -0.8)

	def test_div2(self):
		self.calc.input_work("10 3 /")
		#self.assertEqual(round(self.calc.get_result(), 2), 3.33)
		#use assertalmostequal method to avoid using round() func when doing calculation with float
		self.assertAlmostEqual(self.calc.get_result(), 3.33, places=2)

	def test_valuerror(self):
		self.calc.input_work("1 a +")
		self.assertEqual(self.calc.get_result(), "Cannot convert input to number.")

	def test_indexerror(self):
		self.calc.input_work("1 2 + *")
		self.assertEqual(self.calc.get_result(), "Math Error!")

	def test_add_minus_mul_div(self):
		self.calc.input_work(" 1 2  +   6 * 2 / 1 -    ")
		#self.assertEqual(round(self.calc.get_result(), 2), 8)
		self.assertEqual(self.calc.get_result(), 8)

	def test_sin_number(self):
		self.calc.input_work("30 sin")
		#self.assertEqual(round(self.calc.get_result(), 2), -0.99)
		#using assertalmostequal we can use either places (how mang digits) or delta (diff between two elements)
		self.assertAlmostEqual(self.calc.get_result(), -0.99, msg="check sin() function in RNPCalculator", delta=0.01)

	def test_sin_degree(self):
		self.calc.input_work("30 d sin")
		self.assertEqual(round(self.calc.get_result(), 2), 0.5)		

	#demo for how to use skip decorator to skip function not working for windows platform 
	#(skip can be used for any methods in the test and even for the test class)
	@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
	def test_windows_support(self):
		self.assertFalse(False)

	@unittest.skipIf(sys.platform.startswith("win"), "cannot run on Windows")
	def test_not_windows_support(self):
		self.assertTrue(True)

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

#use suite
#make testcases selective
def suite():
	suite = unittest.TestSuite()
	# suite.addTest(RPNCalculatorTest('test_add2'))
	# suite.addTest(RPNCalculatorTest('test_multiple2'))
	# suite.addTest(RPNCalculatorTest('test_div2'))
	# suite.addTest(RPNCalculatorTest('test_minus2'))

	#add tests as list
	l = [RPNCalculatorTest('test_add2'), RPNCalculatorTest('test_multiple2'), RPNCalculatorTest('test_div2'), 
			RPNCalculatorTest('test_minus2'), RPNCalculatorTest('test_sin_number'), MyStackTest('test_push_pop_emptycheck'), MyStackTest('test_large_num_push_pop')]
	suite.addTests(l)

	return suite

if __name__ == '__main__':
	#use unittest main
	#can test 1 or more testcase class
	#unittest.main() #(output: Ran 13 tests in 1.933s)
	
	#use test suite
	runner = unittest.TextTestRunner(verbosity=2)
	test_suite = suite()
	runner.run(test_suite)	