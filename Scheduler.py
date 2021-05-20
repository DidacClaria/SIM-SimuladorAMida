from Server import *
from Source import *
from event import *
from Queue import *
from Sink import *

class Scheduler:

    currentTime = 0
    eventList = []
    ...

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.source = Source()
        self.Queue1 = Queue()
        self.Queue2 = Queue()
        self.Queue3 = Queue()
        self.Queue4 = Queue()
        self.Caja1 = Server()
        self.Caja2 = Server()
        self.Caja3 = Server()
        self.Caja4 = Server()
        self.Caja5 = Server()
        self.Caja6 = Server()
        self.sink = Sink()

        self.source.crearConnexio(Queue1)
        self.source.crearConnexio(Queue2)
        self.source.crearConnexio(Queue3)
        self.source.crearConnexio(Queue4)

        self.Caja1.crearConnexio(Queue1,sink)
        self.Caja2.crearConnexio(Queue2,sink)
        self.Caja3.crearConnexio(Queue3,sink)
        self.Caja4.crearConnexio(Queue4,sink)
        self.Caja5.crearConnexio(Queue4,sink)
        self.Caja6.crearConnexio(Queue4,sink)


        self.simulationStart=Event(self,'SIMULATION_START', 0,null))
        self.eventList.append(simulationStart)

    def run(self):
        #configurar el model per consola, arxiu de text...
        self.configurarModel()

        #rellotge de simulacio a 0
        self.currentTime=0
        #bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            #recuperem event simulacio
            event=self.eventList.donamEsdeveniment
            #actualitzem el rellotge de simulacio
            self.currentTime=event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.objecte.tractarEsdeveniment(event)

        #recollida d'estadístics
        self.recollirEstadistics()

    def configurarModel():
        print "WIP"

    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        self.eventList.inserirEvent(event)

    def tractarEsdeveniment(self,event):
        if (event.tipus=="SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
