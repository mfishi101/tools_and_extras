#Python default
import os
import sys
from time import sleep, localtime, strftime
import calendar
import webbrowser
#Installed Libraries
import win32com.client as win32
import psycopg2
import psycopg2.extras




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
