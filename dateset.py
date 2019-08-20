# internal modules
from time import sleep, localtime, strftime
from datetime import timedelta, date, datetime
from pandas.tseries.offsets import CustomBusinessDay
import calendar
from dateutil.relativedelta import relativedelta
import pandas as pd

# external module
from holiday import SouthAfricanHolidays

sa_bd = CustomBusinessDay(calendar=SouthAfricanHolidays()) 

class Dateset:
	def __init__(self,start=None,end=None,specific=None,workdaycheck=None):
		self.start = start
		self.end = end
		self.specific = specific
		self.workdaycheck = workdaycheck

	def nextworkday(self):
		current_day = datetime.utcnow()
		week_day = current_day.weekday()
		if week_day == 4:
			get_date = current_day + relativedelta(days=+3)
		elif week_day == 5:
			get_date = current_day + relativedelta(days=+2)
		else:
			get_date = current_day + relativedelta(days=+1)

		nextworkday_result = '%s-%s-%s' % (get_date.year, get_date.month, get_date.day)

		return nextworkday_result

	def firstofmonth(self):
		get_date = date.today() - relativedelta(months=+self.start)
		firstofmonth_result = '%s-%s-1' % (get_date.year, get_date.month)
		return firstofmonth_result

	def lastofmonth(self):
		get_date = date.today() - relativedelta(months=+self.end)
		lastofmonth_result = '%s-%s-%s' % (get_date.year, get_date.month, calendar.monthrange(get_date.year, get_date.month)[1])
		return lastofmonth_result

	def startofweek(self):
		get_date = date.today() - relativedelta(weeks=+self.start)
		get_start = get_date - relativedelta(days=+get_date.weekday())
		startofweek_result = '%s-%s-%s' % (get_start.year, get_start.month, get_start.day)
		return startofweek_result

	def endofweek(self):
		get_date = date.today() - relativedelta(weeks=+self.end)
		get_diff = 6 - get_date.weekday()
		get_end = get_date + relativedelta(days=+get_diff)
		endofweek_result = '%s-%s-%s' % (get_end.year, get_end.month, get_end.day)
		return endofweek_result

	def datecheck(self):
		get_date = pd.date_range(start='%s-%s-01' % (date.today().year, date.today().month), end=date.today().strftime('%Y-%m-%d'),  freq=sa_bd).shape[0]
		if get_date == self.workdaycheck:
			datecheck_result = True
		else:
			datecheck_result = False
		return datecheck_result

	def minusdays(self):
		get_date = date.today() - relativedelta(days=+self.start)
		endofweek_result = '%s-%s-%s' % (get_date.year, get_date.month, get_date.day)
		return endofweek_result

	def specificdayofmonth(self):
		get_date = date.today() - relativedelta(months=+self.start)
		specific_day = self.specific
		specificdayofmonth_result = '%s-%s-%s' % (get_date.year, get_date.month, specific_day)
		return specificdayofmonth_result
