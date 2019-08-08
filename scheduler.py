# Installed Libraries
from apscheduler.schedulers.background import BackgroundScheduler

# For Windows Stand-Alone Applications (Typically compile with Pyinstaller), environment may not recognise 'cron' ~Seb
from apscheduler.triggers.cron import CronTrigger
#---------------------------------------------------------------------------------------------------------------------

def someRandomFunction():
    """some random code"""




if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(someRandomFunction, trigger='cron', day_of_week='mon', hour=2, minute=0, second=0)

    #For Stand alone app --------------------------------------------------------------------------------------------
    args = ['Arg1', 2 , [1.2,3.45,67.89]]   # example, if function takes in argument varibles, lists, objects etc.
    trigger = CronTrigger(day_of_week='mon', hour=2, minute=0, second=0)
    sched.add_job(someRandomFunction, trigger, args=(args[0],args[2],args[2]))   #can leave out args overload if there are no arguments in function
    #----------------------------------------------------------------------------------------------------------------
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
