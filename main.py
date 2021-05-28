from Scheduler import *

def main():
    scheduler = Scheduler()

    scheduler.debug = True
    scheduler.maxTime = 5000

    scheduler.run()

if __name__ == "__main__":
    main()