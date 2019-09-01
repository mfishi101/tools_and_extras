# do common imports
import psycopg2
import psycopg2.extras
from emailserver import Emailer
import pandas as pd
from time import sleep, localtime, strftime
import os
from datetime import timedelta, date, datetime
from assets.holiday import SouthAfricanHolidays
from pandas.tseries.offsets import CustomBusinessDay
import calendar
from dateutil.relativedelta import relativedelta
import warnings
import mysql.connector
from auth.auth import *
# getpath = os.path.dirname(os.path.abspath(__file__))

currentpath = os.getcwd()


express = dict(host='host address', 
					dbname='database name', 
					user='username', 
					password='password')


# create connection string
conn_string = "host=%s dbname=%s user=%s password=%s" % (express['host'],
                                                             express['dbname'],
                                                             express['user'],
                                                             express['password'])

# list of possible error codes
reportingserviceerror = 'Query failed'
schedulingerror = 'a scheduling job failed'
emailerror = 'email failed to send'
scripterror = 'error in script'
