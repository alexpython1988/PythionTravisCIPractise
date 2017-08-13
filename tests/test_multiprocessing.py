# import multiprocessing as mp
import multiprocessing
from multiprocessing import Process, Queue
import threading
import time
import os
from multiprocessing import cpu_count
import concurrent.futures
import functools
from multiprocessing import Pool as ProcessPool
from multiprocessing.pool import ThreadPool
from multiprocessing import freeze_support
from threading import RLock

lock = RLock()

def my_sum(j):
	sum1 = 0 
	for k in range(j):
		sum1 += k
		#time.sleep(0.02)
		# with open("file1", "a") as f:
		# 	print(sum1, file=f, end='\n')

def my_sqrt(x):
	sum1 = 0
	r = []
	for k in range(1000, x, -1):
		sum1 += k
		r.append("{}\t{}\t{}\t{}".format(x, sum1, os.getpid(), threading.currentThread().ident))
	# return "{}\t{}\t{}\t{}".format(x, sum1, os.getpid(), threading.currentThread().ident)
	return r

def create_test():
	s = set()
	for i in range(100):
		s.add(i)
	return s

def result2txt(future, ofile):
	result = future.result()
	mode = None
	if not os.path.isfile(ofile):
		mode = "w"
	else:
		mode = "a"
	with open(ofile, mode) as f:
		for each in result:
			print(each, file=f, end='\n')


# def run_test(nums):
# 	with open("final.txt", "w") as f:
# 		for each in nums:
# 			print(each*each, file=f, end='\n')

# def feed(queue, jobs):
# 	for job in jobs:
# 		queue.put(job)

# def process(queue_in, queue_out):
# 	while 1:
# 		try: 
# 			job = queue_in.get(block=True)
# 			#print("process: " + str(job))
# 			res = my_sqrt(job)
# 			queue_out.put((job, res))
# 		except:
# 			#print("!!!!!!!!!!!!!")
# 			break

# def write(queue, fname):
# 	with open(fname, "w") as f:
# 		while 1:
# 			try:
# 				job, res = queue.get(block=True)
# 				print("init: {}; result: {}".format(job, res), file=f, end='\n')
# 			except:
# 				#print("!!!!!!!!!!!!!")
# 				break

def sub2(month):
	for i in range(100):
		month += 1

	return month

def out2(future, file):
	res = future.result()
	if not os.path.isfile(file):
		mode = "w"
	else:
		mode = "a"
	lock.acquire()
	try:
		with open(file, mode) as f:
			print(res, file=f, end='\n')
	finally:
		lock.release()
	# with open(file, mode) as f:
	# 		print(res, file=f, end='\n')

def out1(future, file):
	res, months = future.result()
	if not os.path.isfile(file):
		mode = "w"
	else:
		mode = "a"
	lock.acquire()
	try:
		with open(file, mode) as f:
			print(res, file=f, end='\n')
	finally:
		lock.release()
	# with open(file, mode) as f:
	# 		print(res, file=f, end='\n')

	futures_= []

	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
		# lock.acquire()
		for month in months:
			future_ = executor.submit(sub2, month=month)
			future_.add_done_callback(functools.partial(out2, file="1/out2.txt"))
			futures_.append(future_)
		# lock.release()
		concurrent.futures.wait(futures_)

def sub1(season):
	for i in range(100):
		season += 1

	months = range(0, (season//100000)+10)
	#print(season//10000)
	# futures_= []

	# with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
	# 	# lock.acquire()
	# 	for month in months:
	# 		future_ = executor.submit(sub2, month=month)
	# 		future_.add_done_callback(functools.partial(out1, file="1/out2.txt"))
	# 		futures_.append(future_)
	# 	# lock.release()
	# 	concurrent.futures.wait(futures_)
	
	return season, months

def main():
	seasons = range(10000)
	futures_= []

	if os.path.isfile("1/out1.txt"):
		os.remove("1/out1.txt")
	if os.path.isfile("1/out2.txt"):
		os.remove("1/out2.txt")

	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
		for season in seasons:
			future_ = executor.submit(sub1, season=season)
			future_.add_done_callback(functools.partial(out1, file="1/out1.txt"))
			futures_.append(future_)
		concurrent.futures.wait(futures_)


	check = []
	check1 = []
	with open("1/out1.txt", "r") as f:
		for each in f:
			check.append(int(each[:-1]))
	with open("1/out2.txt", "r") as f:
		for each in f:
			check1.append(int(each[:-1]))

	print(len(check))
	print(len(check1))
	# for each in seasons:
	# 	for i in range(100):
	# 		each += 1
	# 	# try:
	# 	j = check.index(each)
	# 	#print(j)
	# 	check.pop(j)
			#print(len(check))
		# except:
		# 	print("check failed!")

	# if len(check) == 0:
	# 	print("sucess!")
	# else:
	# 	print("fail!")
	

	# # jobs = create_test()
	# futures_ = []
	# #test using concurrent.future
	# with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as excutor:
	# 	for job in jobs:
	# 		future_ = excutor.submit(my_sqrt, x=job)
	# 		future_.add_done_callback(functools.partial(result2txt, ofile="test_mulitprocessing.txt"))
	# 		futures_.append(future_)
	# 	concurrent.futures.wait(futures_)

	#multiprocess
	#processes = [mp.process(target=my_sum, args= for )]
	# p1 = Process(target=my_sum, args=(1, 10000))
	# p2 = Process(target=my_sum, args=(10000, 20000))
	# p1.start()
	# p2.start()
	# p1.join()
	# p2.join()

	#single thread
	# my_sum(1,10000)
	# my_sum(10000,20000)
	# l = [] 
	
	
	# for job in jobs:
	# 	res = my_sqrt(job)
	# 	l.append(res)
	# with open("foo1.txt", "w") as f:
	# 	for each in l:
	# 		print(each, file=f, end='\n')


	#multithread
	# t1 = threading.Thread(target=my_sum, args=(1, 10000))
	# t2 = threading.Thread(target=my_sum, args=(10000, 20000))
	# t1.start()
	# t2.start()

	#concurrent.futures
	# work_queue = Queue()
	# write_queue = Queue()
	
	# nthreads = multiprocessing.cpu_count()
	# fname= "foo.txt"
	# feedProc = Process(target=feed, args=(work_queue, jobs))
	# workProc = [Process(target=process, args=(work_queue, write_queue)) for i in range(nthreads)]
	# outProc = Process(target=write, args=(write_queue, fname))

	# feedProc.start()
	# for each in workProc:
	# 	each.start()
	# outProc.start()

	# feedProc.join()
	# for each in workProc:
	# 	each.join()
	# outProc.join()
	# l = None
	# with Pool(processes=4) as pool:
	# 	l= pool.map(my_sqrt, jobs)

	# print(len(jobs))
	# print(len(l))
	# print(type(jobs))
	# print(type(l))
	
	# n = multiprocessing.cpu_count()
	# pool = ProcessPool(processes=n)
	# #pool = ThreadPool(processes=n)
	# ress = {}
	# for job in jobs:
	# 	res = pool.apply_async(my_sqrt, args=(job,))
	# 	ress[job] = res

	# final_ress = {}

	# while 1:
	# 	for k, v in ress.items():
	# 		if v.ready() == False:
	# 			print(k, "working...")
	# 		else:
	# 			print(k, "result: ", v.get())
	# 	time.sleep(1)
	# 	# os.system("clear")
	# 	print()
	# 	print()

	# 	for k, v in ress.items():
	# 		if v.ready() == False:
	# 			break
	# 	else:
	# 		for k, v in ress.items():
	# 			print(k, "result: ", v.get())
	# 			final_ress[k] = v
	# 		print("="*30)
	# 		print("done")
	# 		print("="*30)
	# 		break

	# pool.close()
	# pool.join()

	# for each in final_ress:
	# 	print(final_ress[each].get())





if __name__ == '__main__':
	freeze_support() #only need for windows
	main()