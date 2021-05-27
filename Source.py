#millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import *
# from Server import *
from Event import *
from Queue import *
from Client import *
from Scheduler import *
from Distributions import distribucioNormal

class Source:

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        self.entitatsCreades=0
        self.state='idle'
        self.scheduler=scheduler
        self.queues = []
        print("Se ha creado un Source")

    def crearConnexio(self,queue):
        self.queues.append(queue)
        print("Se ha conectado una queue con una source.")

    def tractarEsdeveniment(self, event):
        if (event.type=='SIMULATION_START'):
            print("Source trata un evento de tipo SIMULATION_START")
            self.simulationStart(event)

        elif (event.type=='NEXT_ARRIVAL'):
            print("Source trata un evento de tipo NEXT_ARRIVAL")
            self.processNextArrival(event)
        
        else:
            print("[ERROR]: Scheduler ha recibido un evento de tipo", event.type, "y no sabe cómo controlarlo")

    def simulationStart(self,event):
        nouEvent=self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self,event):

        # Nomes crea la entitat si té queues disponibles
        if (self.queues):
            # Cal crear l'entitat
            entitat = self.crearEntitat()

            # Mirar quina cua té menys pes
            bestQueue = self.queues[0]
            for queue in self.queues:
                if ((bestQueue == None or queue.pesTotal < bestQueue.pesTotal) and queue.state != 'full'):
                    bestQueue = queue

            # Transferir la entitat a la queue
            bestQueue.recullEntitat(event.time, entitat)

        # Cal programar la següent arribada
        nouEvent=self.properaArribada(event.time)
        self.scheduler.afegirEsdeveniment(nouEvent)


    def properaArribada(self, time):

        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = distribucioNormal(10, 1)

        # incrementem estadistics si s'escau
        self.entitatsCreades = self.entitatsCreades + 1
        self.state = 'busy'

        # programació primera arribada
        return Event(self,'NEXT_ARRIVAL', time + tempsEntreArribades, None)

    def crearEntitat(self):
        entitat = Client(self.scheduler)
        return entitat