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


