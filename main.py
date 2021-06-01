from Scheduler import *
import argparse

def main():
    scheduler = Scheduler()

    parser = argparse.ArgumentParser(description='Ejecutar el simulador a medida.')
    parser.add_argument('-d', '--debug', action="store_true", default=False, help='Si se activa, el programa imprime cada acción que realiza la simulación.')
    parser.add_argument('-t', '--time', type=int, required=True, help='El tiempo máximo de simulación en SEGUNDOS.')

    args = parser.parse_args()

    scheduler.debug = args.debug
    scheduler.maxTime = args.time

    scheduler.run()

    # Si falta instalar numpy, ejecutar: python3 -m pip install numpy

if __name__ == "__main__":
    main()