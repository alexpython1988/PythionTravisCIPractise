from MyStack import MyStack
import math
import re


class RPNCalculator:
	__input_data = ""
	__stack = None

	def __init__(self):
		self.__stack = MyStack()

	def __process_inpuit_data(self):
		args = re.split(r"\s{1,}", self.__input_data.strip())
		#print(args)
		try:
			for each in args:
				if each == "+":
					num1 = self.__stack.pop()
					num2 = self.__stack.pop()
					self.__stack.push(num1 + num2)
				elif each == "-":
					num1 = self.__stack.pop()
					num2 = self.__stack.pop()
					self.__stack.push(num2 - num1)
				elif each == "*":
					num1 = self.__stack.pop()
					num2 = self.__stack.pop()
					self.__stack.push(num1 * num2)
				elif each == "/":
					num1 = self.__stack.pop()
					num2 = self.__stack.pop()
					self.__stack.push(num2 / num1)
				elif each == "sin":
					num1 = self.__stack.pop()
					self.__stack.push(math.sin(num1))
				elif each == "cos":
					num1 = self.__stack.pop()
					self.__stack.push(math.cos(num1))
				elif each == "sqrt":
					num1 = self.__stack.pop()
					self.__stack.push(math.sqrt(num1))
				elif each == "d":
					print("degree mode")
					num1 = self.__stack.pop()
					self.__stack.push(num1/180*math.pi)
				else:
					num = float(each)
					self.__stack.push(num)
		except ValueError:
				while not self.__stack.is_empty():
					self.__stack.pop()
				self.__stack.push("Cannot convert input to number.")
		except IndexError:
				while not self.__stack.is_empty():
					self.__stack.pop()
				self.__stack.push("Math Error!")

	def input_work(self, input_data):
		self.__input_data += input_data

	def get_result(self):
		self.__process_inpuit_data()
		return self.__stack.pop()