import calendar
from datetime import datetime
import click

@click.command()
@click.option('--year', '-y', 'year', default=datetime.today().year)
@click.option('--month', '-m', 'month', is_flag=True)
@click.option('--monthNum', '-mm', 'monthNum', default=datetime.today().month)

def cal(year, month, monthNum):
	if month:
		print(calendar.month(year,monthNum))
	else:
		print(calendar.calendar(year))

if __name__ == '__main__':
	cal()