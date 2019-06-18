import calendar
from datetime import datetime
import click

@click.command()
@click.option('--params', '-pr', 'params', is_flag=True)

def cal(y=datetime.today().year, m=False):
	if m:
		print(calendar.month(y,m))
	else:
		print(calendar.calendar(y))

if __name__ == '__main__':
	cal()