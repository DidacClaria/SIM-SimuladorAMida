# from Server import *
from Source import *
from Event import *
from Queue import *
from Sink import *
from TerminalColors import TerminalColors as color

class Scheduler:

    currentTime = 0
    eventList = []

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.source1 = Source(self)
        self.Queue1 = Queue(self)
        self.Queue2 = Queue(self)
        self.Queue3 = Queue(self)
        self.Queue4 = Queue(self)

        self.source2 = Source(self)
        self.Queue5 = Queue(self)
        # self.Caja1 = Server()
        # self.Caja2 = Server()
        # self.Caja3 = Server()
        # self.Caja4 = Server()
        # self.Caja5 = Server()
        # self.Caja6 = Server()
        # self.sink = Sink()

        self.source1.crearConnexio(self.Queue1)
        self.source1.crearConnexio(self.Queue2)
        self.source1.crearConnexio(self.Queue3)
        self.source1.crearConnexio(self.Queue4)

        self.source2.crearConnexio(self.Queue5)

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
        if (event.time < self.currentTime):
            print(color.FAIL, "[ERROR]: Viaje en el tiempo inesperado.", color.ENDC)
            return;
        print("Se ha añadido un evento de tipo ", event.type)
        self.eventList.append(event)

    def tractarEsdeveniment(self,event):
        if (event.type == "SIMULATION_START"):
            print("Scheduler trata un evento de tipo SIMULATION_START")

            # comunicar a tots els objectes que cal preparar-se
            self.afegirEsdeveniment(Event(self.source1, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.source2, 'SIMULATION_START', 0, None))

    def sortEvents(self, e):
        return e.time

    def properEvent(self):
        self.eventList.sort(key = self.sortEvents)
        return self.eventList[0]

    def recollirEstadistics(self):
        print(self.currentTime)