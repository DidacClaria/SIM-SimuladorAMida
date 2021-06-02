from Distributions import distribucioNormal
from SimulationParameters import Parameters
from TerminalColors import TerminalColors as color
from TerminalColors import log
from Queue import *
from Server import *
from Event import *

class Client:
    created_clients = 0

    total_changed_lines = {}
    total_left_clients = {}
    total_wait_time = {}
    total_processed_entities = {}


    def __init__(self, scheduler, container, sourceId):
        # inicialitzar element de simulació
        Client.created_clients = Client.created_clients + 1
        global created_clients
        self.id = 'Client#{}'.format(self.created_clients)
        self.sourceId = sourceId

        self.scheduler=scheduler
        self.pes = distribucioNormal(Parameters.tiempoEnCajaMedia, Parameters.tiempoEnCajaVarianza)

        self.container = container
        self.changeQueueEvent = None

        self.birthTime = self.scheduler.currentTime

        self.leaveEvent = Event(self, 'LEAVE', self.scheduler.currentTime + Parameters.tiempoAhuecarElAla, self)
        log(self.scheduler, self, "se irá del supermercado si no ha llegado a la caja antes de {:.2f}".format(self.leaveEvent.time), color.OKCYAN)
        self.scheduler.afegirEsdeveniment(self.leaveEvent)

        if (not self.sourceId in Client.total_wait_time): Client.total_wait_time[self.sourceId] = 0
        if (not self.sourceId in Client.total_processed_entities): Client.total_processed_entities[self.sourceId] = 0
        if (not self.sourceId in Client.total_left_clients): Client.total_left_clients[self.sourceId] = 0
        if (not self.sourceId in Client.total_changed_lines): Client.total_changed_lines[self.sourceId] = 0
    

    def moveTo(self, container):
        self.container = container

        # Eliminar el evento de cambiar cola si se había añadido uno previamente, para que no se active depués de haber cambiado de contenedor
        if (self.changeQueueEvent != None):
            log(self.scheduler, self, "se ha movido a un nuevo contenedor, por lo que elimina su evento de cambiar de cola en {:.2f}".format(self.changeQueueEvent.time), color.OKCYAN)
            self.scheduler.eliminarEsdeveniment(self.changeQueueEvent)
            self.changeQueueEvent = None

        # Si el cliente se ha movido a una cola nueva, añadir un nuevo evento de cambiar cola
        if(isinstance(self.container, Queue)):

            eventoCambiarCola = Event(self, 'CHANGE_QUEUE', self.scheduler.currentTime + Parameters.tiempoEsperaEnCola, self)
            self.changeQueueEvent = eventoCambiarCola
            log(self.scheduler, self, "se ha movido a una nueva cola, y cambiará a otra cola si no ha llegado a la caja antes de {:.2f}".format(eventoCambiarCola.time), color.OKCYAN)
            self.scheduler.afegirEsdeveniment(eventoCambiarCola)
        
        elif(isinstance(self.container, Server)):

            log(self.scheduler, self, "ha llegado a la caja, por lo que elimina su evento de ahuecar el ala en {:.2f}".format(self.leaveEvent.time), color.OKCYAN)
            self.scheduler.eliminarEsdeveniment(self.leaveEvent)
            self.leaveEvent = None


    def tractarEsdeveniment(self, event):
        log(self.scheduler, self, "Procesando evento ".format(self.id) + event.type, color.HEADER)

        if (event.type=='CHANGE_QUEUE'):
            self.changeQueueEvent = None
            self.changeToAnotherQueue()

        elif (event.type=='LEAVE'):
            if (not isinstance(self.container, Queue)):
                print("{}[ERROR]: {} ha intentado ahuecar el ala pero en lugar de estar en una cola estaba en {}{}".format(color.FAIL, self.id, self.container.id, color.ENDC))
                return
            
            self.container.entitats.remove(self)
            self.container.numEntitats -= 1
            self.container.pesTotal -= self.pes
            log(self.scheduler, self, "se ha cansado de esperar y ha ahuecado el ala", color.FAIL)

            Client.total_left_clients[self.sourceId] += 1

        elif (event.type=='END_SERVICE'):
            self.processarFiServei(event)

        else:
            log(self.scheduler, self, "[WARN]: ha recibido un evento de tipo {} y no sabe cómo gestionarlo".format(event.type), color.WARNING)
    

    def changeToAnotherQueue(self):
        if(not isinstance(self.container, Queue)):
            print("{}[ERROR]: {} ha intentado cambiar de cola pero estaba en {} en lugar de en una cola{}".format(color.FAIL, self.id, self.container.id, color.ENDC))
            return

        log(self.scheduler, self, "se ha cansado de esperar :(", color.OKCYAN)

        # Mirar quina cua té menys pes
        bestQueue = None
        for queue in self.container.connectedQueues:
            if ((bestQueue == None or queue.pesTotal < bestQueue.pesTotal) and queue.state != 'full'):
                bestQueue = queue

        # Transferir la entitat a la queue
        if (bestQueue):
            log(self.scheduler, self, "Cambia de cola de [{}] a [{}]".format(self.container.id, bestQueue.id), color.OKCYAN)
            Client.total_changed_lines[self.sourceId] += 1
            if (self.container.numEntitats < 1): print("{}[ERROR]: {} ha intentado decrementar el numero de clientes de {} a un valor negativo{}".format(color.FAIL, self.id, self.container.id, color.ENDC))

            self.container.numEntitats = self.container.numEntitats - 1
            self.container.pesTotal = self.container.pesTotal - self.pes
            self.container.entitats.remove(self)

            bestQueue.recullEntitat(self.scheduler.currentTime, self)
        
        else:
            log(self.scheduler, self, "quiere cambiar de {} a otra cola, pero no hay ninguna cola a la que cambiar o todas están llenas".format(self.container.id), color.WARNING)

        
    def destroy(self):
        self.deathTime = self.scheduler.currentTime

        wait_time = self.deathTime - self.birthTime

        Client.total_wait_time[self.sourceId] = Client.total_wait_time[self.sourceId] + wait_time
        Client.total_processed_entities[self.sourceId] = Client.total_processed_entities[self.sourceId] + 1


    def resetStatistics():
        Client.total_changed_lines = {}
        Client.total_left_clients = {}
        Client.total_wait_time = {}
        Client.total_processed_entities = {}