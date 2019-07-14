# Installed Libraries
from apscheduler.schedulers.background import BackgroundScheduler

def someRandomFunction():
    """some random code"""




if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(someRandomFunction, trigger='cron', day_of_week='mon', hour=2, minute=0, second=0)

    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
