from Scheduler import *
from TerminalColors import *
import argparse

def main():

    parser = argparse.ArgumentParser(description='Ejecutar el simulador a medida.')
    parser.add_argument('-d', '--debug', action="store_true", default=False, help='Si se activa, el programa imprime cada acción que realiza la simulación.')
    parser.add_argument('-t', '--time', type=int, required=True, help='El tiempo máximo de simulación en SEGUNDOS.')

    args = parser.parse_args()


    for i in range(5):
        scheduler = Scheduler()
        scheduler.debug = args.debug
        scheduler.maxTime = args.time
        scheduler.numSimulations = 5
        scheduler.simulationNum = i
        scheduler.run()
    
    print ("COMPLETION: {:.2f}%".format(100), end="\r")
    print("\n")

    for casId, casStatistics in Scheduler.statistics.items():
        print("======={}=======".format(casId))
        for stat, values in casStatistics.items():
            print("{}: {} -> {:.2f}".format(stat, str(values), sum(values) / len(values)))
        print()


    # Si falta instalar numpy, ejecutar: python3 -m pip install numpy

if __name__ == "__main__":
    main()