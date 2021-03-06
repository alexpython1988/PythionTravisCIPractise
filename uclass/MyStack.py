class MyStack:
	#LIFO
	__data = None

	def __init__(self):
		self.__data = []

	def push(self, ele):
		#self.__data.append(ele)
		self.__data.insert(0, ele)

	def pop(self):
		# return self.__data.pop()
		return self.__data.pop(0)
		
	def is_empty(self):
		return len(self.__data) == 0

	def peek(self, index = -1):
		return self.__data[index]

	def size(self):
		return len(self.__data)

	def clear(self):
		self.__data = []