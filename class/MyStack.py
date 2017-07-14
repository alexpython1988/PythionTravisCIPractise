class MyStack:
	#LIFO
	__data = []

	def push(self, ele):
		self.__data.append(ele)

	def pop(self):
		return self.__data.pop()
		
	def is_empty(self):
		return len(self.__data) == 0

	def peek(self, index = -1):
		return self.__data[index]