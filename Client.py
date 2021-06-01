from Distributions import distribucioNormal
from SimulationParameters import Parameters
from TerminalColors import TerminalColors as color
from TerminalColors import log
from Queue import *
from Event import *

class Client:
    pes = 0
    created_clients = 0
    changed_lines = 0

    def __init__(self, scheduler, container):
        # inicialitzar element de simulació
        Client.created_clients = Client.created_clients + 1
        global created_clients
        self.id = 'Client#{}'.format(self.created_clients)

        self.scheduler=scheduler
        self.pes = distribucioNormal(Parameters.tiempoEnCajaMedia, Parameters.tiempoEnCajaVarianza)

        self.container = container
        self.changeQueueEvent = None
        # print("Se ha creado un Cliente con peso = ", pes)
    

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


    def tractarEsdeveniment(self, event):
        log(self.scheduler, self, "Procesando evento ".format(self.id) + event.type, color.HEADER)

        if (event.type=='CHANGE_QUEUE'):
            self.changeQueueEvent = None
            self.changeToAnotherQueue()

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
            Client.changed_lines = Client.changed_lines + 1
            self.container.numEntitats = self.container.numEntitats - 1
            bestQueue.recullEntitat(self.scheduler.currentTime, self)
        
        else:
            log(self.scheduler, self, "quiere cambiar de {} a otra cola, pero no hay ninguna cola a la que cambiar o todas están llenas".format(self.container.id), color.WARNING)