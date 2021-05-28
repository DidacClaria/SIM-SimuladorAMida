
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

        self.scheduler=scheduler
        self.pesTotal = 0
        log(self.scheduler, self, "se ha creado", color.OKBLUE)


    def afegirOutput(self, server):
        self.outputs.append(server)
        log(self.scheduler, self, "ha añadido {} como ouput".format(server.id), color.OKBLUE)


    def recullEntitat(self, time, entitat):
        self.entitats.append(entitat)
        self.entitatsAfegides = self.entitatsAfegides + 1
        self.pesTotal = self.pesTotal + entitat.pes
        log(self.scheduler, self, "ha recibido una nueva entidad", color.OKCYAN)
        
        idleServer = None
        for server in self.outputs:
            # print(color.OKCYAN, "[{}]: El server tiene estado".format(self.id), server.state, color.ENDC)
            if (server.state == 'idle'):
                idleServer = server
        if (idleServer != None):
            # si alguno de los outputs tiene estado "idle", enviar la entidad
            self.enviaProperaEntitat(time, idleServer)
        else:
            log(self.scheduler, self, "[WARN]: ha recibido una entidad pero ninguno de sus servers está libre", color.WARNING)
    

    def enviaProperaEntitat(self, time, server):
        if (server.state == 'idle' and self.entitats):
            log(self.scheduler, self, "Envía entidad a [{}]".format(server.id), color.OKCYAN)

            # sacar entidad de la cola
            ultimaEntitat = self.entitats[0]
            self.entitats.remove(ultimaEntitat)
            self.pesTotal = self.pesTotal - ultimaEntitat.pes

            # enviar entidad al server
            server.recullEntitat(time, ultimaEntitat)

        elif (len(self.entitats) == 0):
            log(self.scheduler, self, "ha intentado enviar una entidad a {} pero ya no quedan más entidades disponibles".format(server.id), color.FAIL)

        elif (server.state != 'idle'):
            log(self.scheduler, self, "{} se encuentra ocupada. El estado del server es = ".format(server.id), color.FAIL)

