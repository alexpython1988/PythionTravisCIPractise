import unittest
import sys
sys.path.append("class\\")
from RPNCalculator import RPNCalculator

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
		self.assertEqual(round(self.calc.get_result(), 2), -0.8)

	def test_div2(self):
		self.calc.input_work("10 3 /")
		self.assertEqual(round(self.calc.get_result(), 2), 3.33)

	def test_valuerror(self):
		self.calc.input_work("1 a +")
		self.assertEqual(self.calc.get_result(), "Cannot convert input to number.")

	def test_indexerror(self):
		self.calc.input_work("1 2 + *")
		self.assertEqual(self.calc.get_result(), "Math Error!")

	def test_add_minus_mul_div(self):
		self.calc.input_work(" 1 2  +   6 * 2 / 1 -    ")
		self.assertEqual(round(self.calc.get_result(), 2), 8)

	def test_sin_number(self):
		self.calc.input_work("30 sin")
		self.assertEqual(round(self.calc.get_result(), 2), -0.99)

	def test_sin_degree(self):
		self.calc.input_work("30 d sin")
		self.assertEqual(round(self.calc.get_result(), 2), 0.5)		


if __name__ == '__main__':
	unittest.main()	