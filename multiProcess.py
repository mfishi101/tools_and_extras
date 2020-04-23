import os
from multiprocessing import Pool, Process
import sys
import subprocess
from time import localtime, strftime, sleep
from datetime import datetime, time

processes = (""" put list of processes here""")
no_of_processes = len(processes)

def run_process(process):
    os.system('python {}'.format(process))

if __name__ == '__main__':

    pool = Pool(processes=no_of_processes)
    pool.map(run_process, processes)


# another take on multiprocessing with the option to stop and restart services

def gotosleep(buffertime,multiplier,timeinteval):

	if multiplier == 'permin':
		addtime = 60
		timemultiplier = 1
		timeformat = int(strftime('%S',localtime()))
	elif multiplier == 'hourly':
		addtime = 60*60
		timemultiplier = 60
		timeformat = int(strftime('%M',localtime()))
	elif multiplier == 'daily':
		addtime = 60*60*24
		timemultiplier = 60*60
		timeformat = int(strftime('%H',localtime()))
	else:
		addtime=0

	if timeformat < timeinteval:
		a = (timeinteval - timeformat)*timemultiplier
	elif timeformat > timeinteval:
		a = addtime - (timeformat*timemultiplier) + (timeinteval*timemultiplier)
	else:
		a = addtime
	sleep(a-buffertime)

def process1():
	a = subprocess.Popen(["python3", "randomfile1.py"])
	gotosleep(5,'daily',22)
	a.kill()
	print('exited')

def process2():
	a = subprocess.Popen(["python3", "randomfile2.py"])
	gotosleep(5,'daily',22)
	a.kill()
	print('exited')

def process3():
	a = subprocess.Popen(["python3", "randomfile3.py"])
	gotosleep(5,'daily',22)
	a.kill()
	print('exited')

processdict = dict(p1=process1,
					p2=process2,
					p3=process3)

def runprocesses():
	print('-------------------STARTING PROCESSES--------------------------')
	processd = {}
	for x in processdict.values():
		processd['go%s' % x] = Process(target=x)
		processd['go%s' % x].start()

	gotosleep(0,'daily',22)

	for x in processdict.values():
		processd['go%s' % x].terminate()
		processd['go%s' % x].join()

	print('-------------------STOPPING PROCESSES--------------------------')

if __name__ == '__main__':
	while True:
		runprocesses()