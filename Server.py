#millor treballar amb define o algun sistema simular a l'enum de C++
from Server import *
from Event import *
from TerminalColors import TerminalColors as color
from TerminalColors import log

class Server:

    def __init__(self,scheduler, id):
        # inicialitzar element de simulació
        self.id = id
        self.entitatsTractades = 0
        self.state = 'idle'
        self.scheduler = scheduler
        self.entitatActiva = None

        self.queue = None
        self.sink = None
        log(self.scheduler, self, "se ha creado", color.OKBLUE)


    def afegirInput(self, queue):
        self.queue = queue
        log(self.scheduler, self, "ha establecido {} como input".format(queue.id), color.OKBLUE)
        queue.afegirOutput(self)


    def afegirOutput(self, sink):
        self.sink = sink
        log(self.scheduler, self, "ha establecido {} como output".format(sink.id), color.OKBLUE)


    def recullEntitat(self, time, entitat):
        log(self.scheduler, self, "ha recibido una entidad", color.OKCYAN)
        self.entitatActiva = entitat
        entitat.moveTo(self)
        self.programarFinalServei(time,entitat)


    def tractarEsdeveniment(self, event):
        log(self.scheduler, self, "Procesando evento ".format(self.id) + event.type, color.HEADER)

        if (event.type=='SIMULATION_START'):
            self.simulationStart(event)

        elif (event.type=='END_SERVICE'):
            self.processarFiServei(event)

        else:
            log(self.scheduler, self, "[WARN]: ha recibido un evento de tipo {} y no sabe cómo gestionarlo".format(event.type), color.WARNING)


    def simulationStart(self,event):
        self.state = 'idle'
        self.entitatsTractades = 0


    def programarFinalServei(self, time, entitat):

        # que triguem a fer un servei (aleatorietat)
        tempsServei = entitat.pes

        # incrementem estadistics si s'escau
        self.state = 'busy'

        # programació final servei
        eventoProceso = Event(self, 'END_SERVICE', time + tempsServei, entitat)
        log(self.scheduler, self, "ha empezado a procesar una entidad y acabará en {:.2f}".format(eventoProceso.time), color.OKGREEN)
        self.scheduler.afegirEsdeveniment(eventoProceso)
        

    def processarFiServei(self,event):

        log(self.scheduler, self, "ha terminado de procesar una entidad", color.OKGREEN)

        # Registrar estadístics
        self.entitatsTractades = self.entitatsTractades + 1

        #sink.recullEntitat(entitat)
        if (self.queue.numEntitats < 1): print("{}[ERROR]: {} decrementar el numero de clientes de {} a un valor negativo{}".format(color.FAIL, self.id, self.queue.id, color.ENDC))
        self.queue.numEntitats = self.queue.numEntitats - 1
        self.queue.pesTotal = self.queue.pesTotal - self.entitatActiva.pes

        self.entitatActiva = None
        self.state = 'idle'
        log(self.scheduler, self, "solicita a {} que le envíe la siguiente entidad".format(self.queue.id), color.OKCYAN)
        self.queue.enviaProperaEntitat(event.time, self)
        