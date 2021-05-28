from Server import *
from Source import *
from Event import *
from Queue import *
from Sink import *
from TerminalColors import TerminalColors as color
from TerminalColors import log

class Scheduler:

    debug = False

    maxTime = 100
    currentTime = 0
    eventList = []


    def __init__(self):
        self.id = 'Scheduler'

        # creació dels objectes que composen el meu model
        self.source1 = Source(self, 'Source1')
        self.Queue1 = Queue(self, 'Cua1')
        self.Queue2 = Queue(self, 'Cua2')
        self.Queue3 = Queue(self, 'Cua3')

        self.source2 = Source(self, 'Source2')
        self.Queue4 = Queue(self, 'Cua4')
        self.Caja1 = Server(self, 'Caja1')
        self.Caja2 = Server(self, 'Caja2')
        self.Caja3 = Server(self, 'Caja3')
        self.Caja4 = Server(self, 'Caja4')
        self.Caja5 = Server(self, 'Caja5')
        self.Caja6 = Server(self, 'Caja6')
        # self.sink = Sink()

        self.source1.crearConnexio(self.Queue1)
        self.source1.crearConnexio(self.Queue2)
        self.source1.crearConnexio(self.Queue3)

        self.source2.crearConnexio(self.Queue4)

        self.Caja1.afegirInput(self.Queue1)
        self.Caja2.afegirInput(self.Queue2)
        self.Caja3.afegirInput(self.Queue3)
        self.Caja4.afegirInput(self.Queue4)
        self.Caja5.afegirInput(self.Queue4)
        self.Caja6.afegirInput(self.Queue4)
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
        while self.eventList and self.currentTime <= self.maxTime:
            if (not self.debug):
                percentage = (self.currentTime/self.maxTime)*100
                print ("COMPLETION: {:.2f}%".format(percentage), end="\r")
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
        log(self, self, "[{}]: Configurando modelo...".format(self.id), color.OKBLUE)


    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        if (event.time < self.currentTime):
            log(self, self, "[ERROR]: Viaje en el tiempo inesperado.", color.FAIL)
            return;
        self.eventList.append(event)


    def tractarEsdeveniment(self,event):
        log(self, self, "[{}]: Procesando evento ".format(self.id) + event.type, color.HEADER)

        if (event.type == "SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se
            self.afegirEsdeveniment(Event(self.source1, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.source2, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja1, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja2, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja3, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja4, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja5, 'SIMULATION_START', 0, None))
            self.afegirEsdeveniment(Event(self.Caja6, 'SIMULATION_START', 0, None))

        else:
            log(scheduler, self, "[WARN]: ha recibido un evento de tipo {} y no sabe cómo gestionarlo".format(event.type), color.WARNING)

    def sortEvents(self, e):
        return e.time


    def properEvent(self):
        self.eventList.sort(key = self.sortEvents)
        return self.eventList[0]


    def recollirEstadistics(self):
        print(self.currentTime)
        
        print(color.OKGREEN)
        print("Source1 ha creado ", self.source1.entitatsCreades, " entidades")
        print("Source2 ha creado ", self.source2.entitatsCreades, " entidades")
        print("Cua1 contiene ", len(self.Queue1.entitats), " clientes con un peso total de ", self.Queue1.pesTotal)
        print("Cua2 contiene ", len(self.Queue1.entitats), " clientes con un peso total de ", self.Queue2.pesTotal)
        print("Cua3 contiene ", len(self.Queue1.entitats), " clientes con un peso total de ", self.Queue3.pesTotal)
        print("Cua4 contiene ", len(self.Queue1.entitats), " clientes con un peso total de ", self.Queue4.pesTotal)
        print("Caja1 ha procesado ", self.Caja1.entitatsTractades, " entidades")
        print("Caja2 ha procesado ", self.Caja2.entitatsTractades, " entidades")
        print("Caja3 ha procesado ", self.Caja3.entitatsTractades, " entidades")
        print("Caja4 ha procesado ", self.Caja4.entitatsTractades, " entidades")
        print("Caja5 ha procesado ", self.Caja5.entitatsTractades, " entidades")
        print("Caja6 ha procesado ", self.Caja6.entitatsTractades, " entidades")

        print(color.ENDC)