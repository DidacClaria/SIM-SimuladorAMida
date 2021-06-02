from Scheduler import *
from TerminalColors import TerminalColors as color
import argparse

def main():

    parser = argparse.ArgumentParser(description='Ejecutar el simulador a medida.')
    parser.add_argument('-t', '--time', type=int, required=True, help='El tiempo máximo de simulación en SEGUNDOS.')
    parser.add_argument('-n', '--simulations', type=int, default=1, help='El número de simulaciones que se ejecutan.')
    parser.add_argument('-s', '--seed', type=int, default=0, help='La seed para los números generados aleatoriamente.')
    parser.add_argument('-d', '--debug', action="store_true", default=False, help='Si se activa, el programa imprime cada acción que realiza la simulación.')
    parser.add_argument('--hide', action="store_true", default=False, help='Si se activa, el programa no mostrará los resultados individuales de cada iteración.')

    args = parser.parse_args()


    for i in range(args.simulations):
        scheduler = Scheduler()
        scheduler.debug = args.debug
        scheduler.maxTime = args.time
        scheduler.numSimulations = args.simulations
        scheduler.simulationNum = i
        scheduler.run()
    
    print ("COMPLETION: {:.2f}%".format(100), end="\r")

    print()
    print("{}Tiempo de ejecución: {}{}{} segundos ({}{:.2f}{} horas){}".format(color.WARNING, color.OKGREEN, args.time, color.WARNING, color.OKGREEN, args.time / 3600, color.WARNING, color.ENDC))
    print("{}Número de ejecuciones: {}{}{}".format(color.WARNING, color.OKGREEN, args.simulations, color.ENDC))
    print()


    for casId, casStatistics in Scheduler.statistics.items():
        print("{}{}╔════ {} ══════════╗{}".format(color.HEADER, color.BOLD, casId, color.ENDC))
        for stat, valuesArray in casStatistics.items():

            # Calcular mean y values (con sólo 2 decimales)
            values = "("
            for i in range(len(valuesArray)):
                if i > 0: values += ", "
                value = valuesArray[i]
                if (value % 1 == 0): values += "{:.0f}".format(value)
                else: values += "{:.2f}".format(value)
            values += ")"
            mean = "{:.2f}".format(sum(valuesArray) / len(valuesArray))

            # Imprimir resultados:
            print("{}║{} ".format(color.HEADER, color.ENDC))
            print("{}║{} ".format(color.HEADER, color.ENDC), end="")

            if (stat == "entitats_creades"):
                print("{}Se han creado {}{}{} clientes.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))
            
            elif (stat == "entitats_en_cua"):
                print("{}Han quedado {}{}{} clientes en las colas.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))
            
            elif (stat == "entitats_processades"):
                print("{}Se han procesado {}{}{} compras.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))
            
            elif (stat == "canvis_de_cua"):
                print("{}Los clientes han cambiado de cola {}{}{} veces.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))
            
            elif (stat == "temps_en_cua"):
                print("{}El tiempo de espera en cola es {}{}{} de media.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))
            
            elif (stat == "entitats_fugides"):
                print("{}De media {}{}{} clientes han ahuecado el ala.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))

            elif (stat == "temps_esperant"):
                print("{}Los clientes han esperado {}{}{} segundos de media a ser atendidos.".format(color.OKCYAN, color.OKGREEN, mean, color.OKCYAN, color.WARNING, values))

            else:
                print("{}{}: {}{}{}".format(color.OKCYAN, stat, color.OKGREEN, mean, color.OKCYAN))
            
            if not args.hide and len(valuesArray) > 1:
                print("{}║{} ".format(color.HEADER, color.ENDC), end="")
                print("{}{}".format(color.WARNING, values))

        print("{}{}╚══════════════════════════════╝{}".format(color.HEADER, color.BOLD, color.ENDC))
        print()

    # Si falta instalar numpy, ejecutar: python3 -m pip install numpy

if __name__ == "__main__":
    main()