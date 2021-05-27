#millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import *
# from Server import *
from Event import *
from Queue import *
from Client import *
from Scheduler import *
import numpy as np

class Source:

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        self.entitatsCreades=0
        self.state='idle'
        self.scheduler=scheduler
        print("Se ha creado un Source")

    def crearConnexio(self,queue):
        self.queue=queue
        print("Se ha conectado una queue con una source.")

    def crearConnexions(self,queue1,queue2,queue3,queue4):
        self.queue1=queue1
        self.queue2=queue2
        self.queue3=queue3
        self.queue4=queue4
        print("Se ha conectado una queue con 4 sources.")

    def tractarEsdeveniment(self, event):
        if (event.type=='SIMULATION_START'):
            print("Source trata un evento de tipo SIMULATION_START")
            self.simulationStart(event)

        if (event.type=='NEXT_ARRIVAL'):
            self.processNextArrival()

    def simulationStart(self,event):
        nouEvent=self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self,event):
        # Cal crear l'entitat
        entitat = self.crearEntitat(self)

        # Mirar quina cua té menys pes
        bestQueue = queue1
        if (queue2.pesTotal < bestQueue.pesTotal):
            bestQueue = queue2
        if (queue3.pesTotal < bestQueue.pesTotal):
            bestQueue = queue3
        if (queue4.pesTotal < bestQueue.pesTotal):
            bestQueue = queue4

        # Transferir la entitat a la queue
        bestQueue.recullEntitat(event.time, entitat)

        # Cal programar la següent arribada
        nouEvent=self.properaArribada(event.temps)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = self.distribucioNormal(5, 10)
        # incrementem estadistics si s'escau
        self.entitatsCreades=self.entitatsCreades+1
        self.state = 'busy'
        # programació primera arribada
        return Event(self,'NEXT ARRIVAL', time+ tempsEntreArribades, None)

    def crearEntitat(self):
        entitat = Client()
        return entitat

    def distribucioNormal(self, center, scale):
        return np.random.normal(center, scale, None)