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

    numSimulations = 1
    simulationNum = 0
    maxTime = 100

    statistics = {}


    def __init__(self):
        self.currentTime = 0
        self.eventList = []

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
                percentage = ((100 * self.simulationNum) / self.numSimulations) + (self.currentTime/self.maxTime)* (100 / self.numSimulations)
                if (percentage > self.latestPercentage + self.percentageStep):
                    self.latestPercentage = percentage
                    print ("COMPLETION: {:.2f}%".format(self.latestPercentage), end="\r")

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
            print("{}[ERROR]: Viaje en el tiempo inesperado en evento {} de {}{}".format(color.FAIL, event.type, event.object.id, color.ENDC))
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
        # if (not self.debug):
        #     print ("COMPLETION: 100.00%", end="\r")
        

        sources = [self.source1, self.source2]
        for source in sources:
            if (not source.id in Scheduler.statistics): Scheduler.statistics[source.id] = {}
            if (not "entitats_creades" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["entitats_creades"] = []
            if (not "entitats_en_cua" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["entitats_en_cua"] = []
            if (not "entitats_processades" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["entitats_processades"] = []
            if (not "canvis_de_cola" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["canvis_de_cola"] = []
            if (not "temps_en_cola" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["temps_en_cola"] = []
            if (not "entitats_fugides" in Scheduler.statistics[source.id]): Scheduler.statistics[source.id]["entitats_fugides"] = []

            Scheduler.statistics[source.id]["entitats_creades"].append(source.entitatsCreades)

            entitats_en_cua = 0
            for queue in source.queues: entitats_en_cua += queue.numEntitats
            Scheduler.statistics[source.id]["entitats_en_cua"].append(entitats_en_cua)

            entitats_processades = 0
            cajas = []
            for queue in source.queues: cajas.extend(queue.outputs)
            for caja in cajas: entitats_processades += caja.entitatsTractades
            Scheduler.statistics[source.id]["entitats_processades"].append(entitats_processades)

            Scheduler.statistics[source.id]["canvis_de_cola"].append(Client.total_changed_lines[source.id])

            Scheduler.statistics[source.id]["temps_en_cola"].append(Client.total_wait_time[source.id])

            Scheduler.statistics[source.id]["entitats_fugides"].append(Client.total_left_clients[source.id])


        Client.resetStatistics()



        # print(color.OKGREEN)
        # print("Tiempo de ejecución = {:.2f} segundos".format(self.maxTime))

        # print("\n=========== CASO 1 ===========")
        # print("Source1 ha creado ", self.source1.entitatsCreades, " entidades")
        # print("Cua1 contiene ", self.Queue1.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue1.pesTotal))
        # print("Cua2 contiene ", self.Queue2.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue2.pesTotal))
        # print("Cua3 contiene ", self.Queue3.numEntitats, " clientes con un peso total de {:.2f} (incluyendo el cliente que está en caja)".format(self.Queue3.pesTotal))
        # print("Caja1 ha procesado ", self.Caja1.entitatsTractades, " entidades")
        # print("Caja2 ha procesado ", self.Caja2.entitatsTractades, " entidades")
        # print("Caja3 ha procesado ", self.Caja3.entitatsTractades, " entidades")
        # print("Han habido ", Client.total_changed_lines, " cambios de cola")
        # print("Tiempo medio en la cola = {:.2f} segundos".format(Client.total_wait_time[self.source1.id] / Client.total_processed_entities[self.source1.id]))
        # print("{} clientes se han cansado de esperar y se han ido sin comprar nada".format(Client.total_left_clients[self.source1.id]))

        # print("\n=========== CASO 2 ===========")
        # print("Source2 ha creado ", self.source2.entitatsCreades, " entidades")
        # print("CuaUnica contiene ", self.Queue4.numEntitats, " clientes con un peso total de {:.2f} (incluyendo los clientes que están en caja)".format(self.Queue4.pesTotal))
        # print("Caja4 ha procesado ", self.Caja4.entitatsTractades, " entidades")
        # print("Caja5 ha procesado ", self.Caja5.entitatsTractades, " entidades")
        # print("Caja6 ha procesado ", self.Caja6.entitatsTractades, " entidades")
        # print("Tiempo medio en la cola = {:.2f} segundos".format(Client.total_wait_time[self.source2.id] / Client.total_processed_entities[self.source2.id]))
        # print("{} clientes se han cansado de esperar y se han ido sin comprar nada".format(Client.total_left_clients[self.source2.id]))

        # print(color.ENDC)