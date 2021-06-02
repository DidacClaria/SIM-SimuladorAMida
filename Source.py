#millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import *
# from Server import *
from Event import *
from Queue import *
from Client import *
from Scheduler import *
from Distributions import distribucioNormal
from SimulationParameters import Parameters
from TerminalColors import TerminalColors as color
from TerminalColors import log

class Source:

    def __init__(self, scheduler, id):
        # inicialitzar element de simulació
        self.id = id
        self.entitatsCreades = 0
        self.state = 'idle'
        self.scheduler=scheduler
        self.queues = []
        log(scheduler, self, "se ha creado".format(self.id), color.OKBLUE)


    def crearConnexio(self, queue):
        self.queues.append(queue)
        log(self.scheduler, self, "ha añadido {} como ouput".format(queue.id), color.OKBLUE)
        # print(color.OKBLUE, "[{}] ha añadido {} como ouput".format(self.id, queue.id), color.ENDC)


    def tractarEsdeveniment(self, event):
        log(self.scheduler, self, "Procesando evento ".format(self.id) + event.type, color.HEADER)

        if (event.type=='SIMULATION_START'):
            self.simulationStart(event)

        elif (event.type=='NEXT_ARRIVAL'):
            self.processNextArrival(event)
        
        else:
            log(self.scheduler, self, "[WARN]: ha recibido un evento de tipo {} y no sabe cómo gestionarlo".format(event.type), color.WARNING)


    def simulationStart(self,event):
        nouEvent=self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)


    def processNextArrival(self,event):

        # Nomes crea la entitat si té queues disponibles
        if (self.queues):
            # Cal crear l'entitat
            entitat = self.crearEntitat()

            # Mirar quina cua té menys pes
            bestQueue = None
            for queue in self.queues:
                if ((bestQueue == None or queue.pesTotal < bestQueue.pesTotal) and queue.state != 'full'):
                    bestQueue = queue

            # Transferir la entitat a la queue
            if (bestQueue):
                log(self.scheduler, self, "Envía entidad creada a [{}]".format(bestQueue.id), color.OKCYAN)
                bestQueue.recullEntitat(event.time, entitat)
            
            else:
                log(self.scheduler, self, "[WARN]: ha creado una entidad pero no tiene ningún output libre", color.WARNING)

        # Cal programar la següent arribada
        nouEvent=self.properaArribada(event.time)
        self.scheduler.afegirEsdeveniment(nouEvent)


    def properaArribada(self, time):

        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = distribucioNormal(Parameters.llegadaClienteMedia, Parameters.llegadaClienteVarianza)

        # incrementem estadistics
        self.state = 'busy'

        # programació primera arribada
        return Event(self,'NEXT_ARRIVAL', time + tempsEntreArribades, None)


    def crearEntitat(self):
        entitat = Client(self.scheduler, self, self.id)
        log(self.scheduler, self, "ha creado un Client con peso = {:.2f}".format(entitat.pes), color.OKGREEN)
        self.entitatsCreades = self.entitatsCreades + 1
        return entitat