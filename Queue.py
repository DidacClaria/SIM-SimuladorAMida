
from TerminalColors import TerminalColors as color
from TerminalColors import log

class Queue:
    pesTotal = 0
    entitats = []

    def __init__(self, scheduler, id):
        # inicialitzar element de simulació
        self.id = id
        self.entitatsAfegides = 0
        self.state = 'idle'
        
        self.entitats = []
        self.outputs = []
        self.connectedQueues = []

        self.scheduler=scheduler
        self.pesTotal = 0
        self.numEntitats = 0
        log(self.scheduler, self, "se ha creado", color.OKBLUE)


    def afegirOutput(self, server):
        self.outputs.append(server)
        log(self.scheduler, self, "ha añadido {} como ouput".format(server.id), color.OKBLUE)


    def conectarAmbCua(self, queue):
        self.connectedQueues.append(queue)
        log(self.scheduler, self, "se ha conectado con la cola {}".format(queue.id), color.OKBLUE)


    def recullEntitat(self, time, entitat):
        log(self.scheduler, self, "ha recibido una nueva entidad", color.OKCYAN)
        entitat.moveTo(self)
        
        self.entraEntitat(entitat)
        
        # self.numEntitats = self.numEntitats + 1
        # self.pesTotal = self.pesTotal + entitat.pes
        
        idleServer = None
        for server in self.outputs:
            # print(color.OKCYAN, "[{}]: El server tiene estado".format(self.id), server.state, color.ENDC)
            if (server.state == 'idle'):
                idleServer = server
        if (idleServer != None):
            # si alguno de los outputs tiene estado "idle", enviar la entidad
            self.enviaProperaEntitat(time, idleServer)
        else:
            log(self.scheduler, self, "ha recibido una entidad pero ninguno de sus servers está libre", color.WARNING)
    
    def entraEntitat(self, entitat):

        self.entitats.append(entitat)
        entitat.pesoEnCola = self.pesTotal

        self.numEntitats = self.numEntitats + 1
        self.pesTotal = self.pesTotal + entitat.pes

    def surtEntitat(self, entitat): 
        index = 0

        if entitat in self.entitats:
            index = self.entitats.index(entitat)
            self.entitats.remove(entitat)

        # actualizar los valores del peso en cola de todos los clientes:
        for i in range(index, len(self.entitats)):
            self.entitats[i].pesoEnCola -= entitat.pes

        self.numEntitats = self.numEntitats - 1
        self.pesTotal = self.pesTotal - entitat.pes

    def enviaProperaEntitat(self, time, server):
        if (server.state == 'idle' and self.entitats):
            log(self.scheduler, self, "Envía entidad a [{}]".format(server.id), color.OKCYAN)

            # sacar entidad de la cola
            ultimaEntitat = self.entitats[0]
            self.entitats.remove(ultimaEntitat)
            # self.pesTotal = self.pesTotal - ultimaEntitat.pes (ahora hago esto en Server, para que una entidad todavía en proceso siga contando como "peso" en la cola)

            # enviar entidad al server
            server.recullEntitat(time, ultimaEntitat)

        elif (len(self.entitats) == 0):
            log(self.scheduler, self, "ha intentado enviar una entidad a {} pero ya no quedan más entidades disponibles".format(server.id), color.WARNING)

        elif (server.state != 'idle'):
            log(self.scheduler, self, "{} se encuentra ocupada. El estado del server es = ".format(server.id), color.WARNING)

