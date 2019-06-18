#Python default
import os
import sys
from time import sleep, localtime, strftime
from tabulate import tabulate
import calendar
import webbrowser
from importlib import reload
from shutil import copy2
#Installed Libraries
import pandas
import win32com.client as win32
import numpy as np
import psycopg2
import psycopg2.extras
import xlsxwriter
#My Libraries
from sqlscripts import *
from networkLists import *
from startuplist import *
from mdxLists import *


def startup(listname, sleeptime):
	"""
	start and application or file
	"""
	for go in listname:
		os.startfile(go)
		sleep(sleeptime)

def openpage(url):
	"""
	open webpage
	"""
	webbrowser.open_new_tab(url)

def openpages(url, sleeptime):
	"""
	open list of webpages
	"""
	for page in url:
		webbrowser.open_new_tab(page)
		sleep(sleeptime)


def sendmailout(to, subject, body, attachments=False):
	"""
	Use outlook to send email
	"""
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = to
	mail.Subject = subject
	mail.Body = 'ph'
	mail.HTMLBody = body  # html format

	if attachments:
		for attach in attachments:
			mail.Attachments.Add(attach)

	mail.Send()


def robynMonthlyBillingFunc(startDate, endDateMinusOneDay, nameOfFile):
	conn_string = replicamain
	"""
	 print the connection string we will use to connect
	"""
	print("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	daterange = pandas.date_range(startDate, endDateMinusOneDay)

	print("%s data executing..."%nameOfFile)

	count = 1

	pandas.read_sql(sql='%s'% robynMonthlyBilling%(daterange[0], daterange[1]), con=conn).to_csv('G:\\My Drive\\Company reports\\Robyn Walker\\%s.csv'%nameOfFile, index=False, mode='a', header = True)

	print('%s Day number 1 done'%(nameOfFile))

	for i in daterange:

		pandas.read_sql(sql='%s'% robynMonthlyBilling%(i+1, i+2), con=conn).to_csv('G:\\My Drive\\Company reports\\Robyn Walker\\%s.csv'%nameOfFile, index=False, mode='a', header = False)

		count += 1

		print('%s Day number %s done'%(nameOfFile,count))

	print('complete')
	sendmailout('robyn.walker@takealot.com',"Report status",'Your %s report is complete. Please allow 5 min for it to upload to the drive'%nameOfFile)


def bagNumbers(BagFileName, cmdxList):
	"""
	Bags by CMDX nuumber with parcels
	"""
	conn_string = replicamain
	# print the connection string we will use to connect
	print("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	print("Query executing...")

	pandas.read_sql(sql='%s'% billing_bag_numbers%cmdxList, con=conn).to_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%BagFileName, index=False, mode='w', header = True)

	count = 0

	print('bag numbers obtained')


def mdxDetails(BagFileName, billiingFileName, query=adhoc):

	conn_string = replicamain
	# print the connection string we will use to connect
	print("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	print("Query executing...")

	pandas.read_sql(sql='%s'% query%('null','null'), con=conn).to_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%billiingFileName, index=False, mode='w', header = True)

	count = 0

	df = pandas.read_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%BagFileName,usecols=[1], header=0)

	bagNum = df['bag_num'].values

	for b in bagNum:

		pandas.read_sql(sql='%s'% query%(b,b), con=conn).to_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%billiingFileName, index=False, mode='a', header = False)

		count += 1

		print(count)



	print('complete')


def AndraBillableDelivered(startDate, endDateMinusOneDay,  nameOfFile, supplier):
	conn_string = replicareport
	# print the connection string we will use to connect
	print("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	daterange = pandas.date_range(startDate, endDateMinusOneDay)

	print("%s data executing..."%nameOfFile)
	count = 1

	df = pandas.read_sql(sql='%s'% andraMonthlyBillableDelivered%(daterange[0], daterange[1], "%s"%supplier, daterange[0], daterange[1], "%s"%supplier), con=conn)
	df['multiplier'] = [np.ceil(df['parcels'][a]/3) if df['parcels'][a]>3 else 1 for a in range(len(df.index))]
	df.to_csv('G:\\My Drive\\Company reports\\Andra\\%s.csv'%nameOfFile, index=False, mode='a', header = True)

	print('%s Day number 1 of %s done'%(nameOfFile, supplier))

	for i in daterange:

		df = pandas.read_sql(sql='%s'% andraMonthlyBillableDelivered%(i+1, i+2, "%s"%supplier, i+1, i+2, "%s"%supplier), con=conn)
		df['multiplier'] = [np.ceil(df['parcels'][a]/3) if df['parcels'][a]>3 else 1 for a in range(len(df.index))]
		df.to_csv('G:\\My Drive\\Company reports\\Andra\\%s.csv'%nameOfFile, index=False, mode='a', header = False)

		count += 1

		print('%s Day number %s of %s done'%(nameOfFile,count, supplier))

	print('complete')
	sendmailout('andra.vantonder@takealot.com',"Report status",'Your %s report is complete. Please allow 5 minutes for it to upload to the drive'%supplier)


def darren(startDate, endDateMinusOneDay, nameOfFile):
	conn_string = replicamain
	"""
	 print the connection string we will use to connect
	"""
	print("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	daterange = pandas.date_range(startDate, endDateMinusOneDay)

	print("%s data executing..."%nameOfFile)

	count = 1

	pandas.read_sql(sql='%s'% adhoc%(daterange[0], daterange[1]), con=conn).to_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%nameOfFile, index=False, mode='a', header = True)

	print('%s Day number 1 done'%(nameOfFile))

	for i in daterange:

		pandas.read_sql(sql='%s'% adhoc%(i+1, i+2), con=conn).to_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv'%nameOfFile, index=False, mode='a', header = False)

		count += 1

		print('%s Day number %s done'%(nameOfFile,count))

	print('complete')
	sendmailout('darren.richards@takealot.com',"Report status",'Your %s report is complete. Please allow 5 min for it to upload to the drive'%nameOfFile)


