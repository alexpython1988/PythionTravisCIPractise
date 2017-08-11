import os
#not sure how to use
#from nose.tools import with_setup
from nose.tools import raises
from nose.tools import timed
import nose.tools as nt
from nose.plugins.attrib import attr
import time
from nose.plugins.plugintest import run_buffered as run
import nose
# import unittest
# from nose.plugins import Plugin
# from MyStack import MyStack
#multithread test: nosetests script --processes=num (num = # of cpu cores)

# class ConfigMyTest(Plugin):
# 	enabled = True
# 	def configure(self, options, conf):
# 		pass
# 	def begin(self):
# 		#TestT.c = MyStack()
# 		TestT.c = []

class TestT:
	c = None
	# @classmethod
	# def setup_func(cls):
	# 	cls.c = RPNCalculator()
	# 	cls.c.input_work("1 2 +")

	# def teardown_func(self):
	# 	pass
	
	# def test_stack(self):
	# 	#self.c.push(1)
	# 	self.c.append(1)
	# 	assert self.c.pop == 1

	def add(self, a, b):
		return a + b

	#@with_setup(setup_func, teardown_func)
	def test_add(self):
		nt.eq_(self.add(1,3), 4)
		# nt.ok_(self.c.get_result() == 3)

	@raises(TypeError)
	def test_error(self):
		raise TypeError("Test")

	@timed(2)
	def test_time(self):
		time.sleep(1)

	@timed(3)
	@attr(speed='slow')
	#run commend:
	#only slow: nosetests test_xxxx.py -A "speed == 'slow'" -v
	#not include slow: nosetests test_xxxx.py -A "speed != 'slow'" -v (fix the doc of nose)
	def test_time1(self):
		time.sleep(2)

	#no decorator
	#function name must be test_A, check_A
	#total 100 test
	def test_event(self):
		for i in range(100):
			yield self.check_event, i, (100-i)

	def check_event(self, a, b):
		assert a + b == 100



#use the run_buffered from nose.plugins.plugintest to run in script instead from shell
#in this method, some results have been removed
if __name__ == '__main__':
	file = os.path.join(os.path.dirname(__file__), 'mynosetest.py')
	run(argv=['nosetests', '-v', file])
	#run(argv=['nosetests', '-v', file], plugins=[ConfigMyTest()])
	result = nose.run(TestT)
	#print(result)