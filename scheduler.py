# Installed Libraries
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from time import sleep

def some_function():
    "do some things"


def startThread(operation):
  # ------------- Create Dictionary of Functions
  availableFunctions = dict(some_function = some_function)
	# ------------- Initiate Thread Operations
  threadToStart = threading.Thread(target=availableFunctions[operation])	
  threadToStart.start()

print('----------------- Starting Scheduled Cron Jobs ------------------\n')
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Africa/Johannesburg',})
scheduler.add_job(startThread,trigger='cron', day=7, hour=3, minute=30, second=0, args=['some_function'],misfire_grace_time=300)

scheduler.start()

try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()