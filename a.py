#!/usr/bin/python3
# Python default
import os
import sys
from time import sleep, localtime, strftime
from tabulate import tabulate
import calendar
import webbrowser
from importlib import reload
from datetime import datetime
# Installed Libraries
import pandas
import win32com.client as win32
import numpy as np
import psycopg2
import psycopg2.extras
import xlsxwriter
import fire
# My Libraries
from sqlscripts import *
from networkLists import *
from startuplist import *
from mdxLists import *
from funcList import functions, heading

class Program(object):

	def columns(self, csv=False, ename='test'):
		if csv:
			df = pandas.read_csv('C:\\Users\\matthew.fisher\\Desktop\\%s.csv' %ename)
			headerNames = list(df.columns.values)
			
		else:
			df = pandas.read_excel('C:\\Users\\matthew.fisher\\Desktop\\%s.xlsx'%ename)
			headerNames = list(df.columns.values)
			
		print(tabulate(None, headers = headerNames, tablefmt='psql'))

	def network(self, dbnetwork=replicamain):
		conn_string = dbnetwork
		# print the connection string we will use to connect
		print("Connecting to database\n	->%s" % (conn_string))

		# get a connection, if a connect cannot be made an exception will be raised here

		# execute our Query
		print('|Datetime         |', '|Delay_as_interval|')
		while True:
			conn = psycopg2.connect(conn_string)

			# conn.cursor will return a cursor object, you can use this cursor to perform queries
			cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			cursor.execute("%s" % networkHealth)

			# retrieve the records from the database
			records = cursor.fetchall()
			print(strftime("%Y-%m-%d %H:%M:%S", localtime()), ''.join(str(e) for e in records))
			sleep(1)
			# cntrl c to escape
		cursor.close()
		conn.close()

	def ipNumber(self, dbnetwork):
		conn_string = dbnetwork
		# print the connection string we will use to connect
		print("Connecting to database\n	->%s" % (conn_string))

		# get a connection, if a connect cannot be made an exception will be raised here

		# execute our Query

		conn = psycopg2.connect(conn_string)

		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		cursor.execute("%s" % getServerIP)

		# retrieve the records from the database
		records = cursor.fetchall()
		print(records)
		sleep(1)
		# cntrl c to escape


a = Program()

if __name__ == '__main__':
	fire.Fire(a)
