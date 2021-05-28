from Scheduler import *

def main():
    scheduler = Scheduler()

    scheduler.debug = True
    scheduler.maxTime = 5000

    scheduler.run()

    # Si falta instalar numpy, ejecutar: python3 -m pip install numpy

if __name__ == "__main__":
    main()