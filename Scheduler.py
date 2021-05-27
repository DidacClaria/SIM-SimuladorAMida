# from Server import *
from Source import *
from Event import *
from Queue import *
from Sink import *

class Scheduler:

    currentTime = 0
    eventList = []

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.source = Source(self)
        self.Queue1 = Queue(self)
        self.Queue2 = Queue(self)
        self.Queue3 = Queue(self)
        self.Queue4 = Queue(self)
        # self.Caja1 = Server()
        # self.Caja2 = Server()
        # self.Caja3 = Server()
        # self.Caja4 = Server()
        # self.Caja5 = Server()
        # self.Caja6 = Server()
        # self.sink = Sink()

        
        self.source.crearConnexions(self.Queue1, self.Queue2, self.Queue3, self.Queue4)

        # self.Caja1.crearConnexio(Queue1,sink)
        # self.Caja2.crearConnexio(Queue2,sink)
        # self.Caja3.crearConnexio(Queue3,sink)
        # self.Caja4.crearConnexio(Queue4,sink)
        # self.Caja5.crearConnexio(Queue4,sink)
        # self.Caja6.crearConnexio(Queue4,sink)


        self.simulationStart=Event(self,'SIMULATION_START', 0, None)
        self.eventList.append(self.simulationStart)

    def run(self):
        #configurar el model per consola, arxiu de text...
        self.configurarModel()

        #rellotge de simulacio a 0
        self.currentTime=0
        #bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            #recuperem event simulacio
            event=self.properEvent()

            self.eventList.remove(event)
            #actualitzem el rellotge de simulacio
            self.currentTime=event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.object.tractarEsdeveniment(event)

        #recollida d'estadístics
        self.recollirEstadistics()

    def configurarModel(self):
        print("Configurant model")

    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        self.eventList.append(event)

    def tractarEsdeveniment(self,event):
        print("tractarEsdeveniment")
        # if (event.tipus=="SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se

    def sortEvents(self, e):
        return e.time

    def properEvent(self):
        self.eventList.sort(key = self.sortEvents)
        return self.eventList[0]

    def recollirEstadistics(self):
        print(self.currentTime)