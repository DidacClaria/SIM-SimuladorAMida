from Server import *
from Source import *
from Event import *
from Queue import *
from Sink import *
from Client import *
from TerminalColors import TerminalColors as color
from TerminalColors import log
from SimulationParameters import Parameters

class Scheduler:

    debug = False

    maxTime = 100
    currentTime = 0
    eventList = []


    def __init__(self):
        self.id = 'Scheduler'

        # Crear objectos del CASO 1: Tres colas intercambiables, cada una asignada a un Server
        self.source1 = Source(self, 'Source1')
        self.Queue1 = Queue(self, 'Cola1')
        self.Queue2 = Queue(self, 'Cola2')
        self.Queue3 = Queue(self, 'Cola3')

        self.source1.crearConnexio(self.Queue1)
        self.source1.crearConnexio(self.Queue2)
        self.source1.crearConnexio(self.Queue3)

        self.Queue1.conectarAmbCua(self.Queue2)
        self.Queue1.conectarAmbCua(self.Queue3)
        self.Queue2.conectarAmbCua(self.Queue1)
        self.Queue2.conectarAmbCua(self.Queue3)
        self.Queue3.conectarAmbCua(self.Queue1)
        self.Queue3.conectarAmbCua(self.Queue2)

        self.Caja1 = Server(self, 'Caja1')
        self.Caja2 = Server(self, 'Caja2')
        self.Caja3 = Server(self, 'Caja3')

        self.Caja1.afegirInput(self.Queue1)
        self.Caja2.afegirInput(self.Queue2)
        self.Caja3.afegirInput(self.Queue3)


        # Crear objectos del CASO 2: Una única cola, asignada a 3 Servers distintos

        self.source2 = Source(self, 'Source2')
        self.Queue4 = Queue(self, 'ColaUnica')
        
        self.Caja4 = Server(self, 'Caja4')
        self.Caja5 = Server(self, 'Caja5')
        self.Caja6 = Server(self, 'Caja6')

        self.source2.crearConnexio(self.Queue4)

        self.Caja4.afegirInput(self.Queue4)
        self.Caja5.afegirInput(self.Queue4)
        self.Caja6.afegirInput(self.Queue4)

        self.simulationStart=Event(self,'SIMULATION_START', 0, None)
        self.eventList.append(self.simulationStart)
        
        self.latestPercentage = 0
        self.percentageStep = 0.5


    def run(self):
        #configurar el model per consola, arxiu de text...
        self.configurarModel()

        #rellotge de simulacio a 0
        self.currentTime=0
        #bucle de simulació (condició fi simulació llista buida)
        while self.eventList and self.currentTime <= self.maxTime:
            if (not self.debug):
                percentage = (self.currentTime/self.maxTime)*100
                if (percentage > self.latestPercentage + self.percentageStep):
                    self.latestPercentage = percentage
                    print ("COMPLETION: {:.2f}%".format(self.latestPercentage), end="\r")

            # print("CURRENT EVENTS:")
            # for events in self.eventList:
            #     print('{:.2f} - {}'.format(events.time, events.type))
            #recuperem event simulacio
            event=self.properEvent()

            self.eventList.remove(event)
            #actualitzem el rellotge de simulacio
            self.currentTime=event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            log(self, self, "Iniciando evento " + event.type, color.HEADER)
            event.object.tractarEsdeveniment(event)

        #recollida d'estadístics
        self.recollirEstadistics()


    def configurarModel(self):
        log(self, self, "Configurando modelo...", color.OKBLUE)
        # self.maxTime = Parameters.totalSimulationTime


    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        if (event.time < self.currentTime):
            # log(self, self, "[ERROR]: Viaje en el tiempo inesperado.", color.FAIL)
            print("{}[ERROR]: Viaje en el tiempo inesperado{}".format(color.FAIL, color.ENDC))
            event.time = self.currentTime

        log(self, self, "Añadiendo el evento {} en {:.2f}".format(event.type, event.time), color.OKBLUE)
        self.eventList.append(event)
        self.eventList.sort(key = self.sortEvents)
    

    def eliminarEsdeveniment(self,event):
        #eliminar esdeveniment determinat
        self.eventList.remove(event)


    def tractarEsdeveniment(self,event):
        log(self, self, "Procesando evento" + event.type, color.HEADER)

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
        return self.eventList[0]


    def recollirEstadistics(self):
        if (not self.debug):
            print ("COMPLETION: 100.00%", end="\r")
        
        print(color.OKGREEN)

        print("=========== CASO 1 ===========")
        print("Source1 ha creado ", self.source1.entitatsCreades, " entidades")
        print("Cua1 contiene ", self.Queue1.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue1.pesTotal))
        print("Cua2 contiene ", self.Queue2.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue2.pesTotal))
        print("Cua3 contiene ", self.Queue3.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue3.pesTotal))
        print("Caja1 ha procesado ", self.Caja1.entitatsTractades, " entidades")
        print("Caja2 ha procesado ", self.Caja2.entitatsTractades, " entidades")
        print("Caja3 ha procesado ", self.Caja3.entitatsTractades, " entidades")
        print("Han habido ", Client.changed_lines, " cambios de cola")

        print("\n=========== CASO 2 ===========")
        print("Source2 ha creado ", self.source2.entitatsCreades, " entidades")
        print("CuaUnica contiene ", self.Queue4.numEntitats, " clientes con un peso total de {:.2f} (incluyendo los clientes que están en caja)".format(self.Queue4.pesTotal))
        print("Caja4 ha procesado ", self.Caja4.entitatsTractades, " entidades")
        print("Caja5 ha procesado ", self.Caja5.entitatsTractades, " entidades")
        print("Caja6 ha procesado ", self.Caja6.entitatsTractades, " entidades")

        print(color.ENDC)