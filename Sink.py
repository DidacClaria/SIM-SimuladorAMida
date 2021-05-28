class Sink:

    def __init__(self,scheduler, id):
        # inicialitzar element de simulació
        self.id = id;
        entitatsEliminades=0
        self.state='idle'
        self.scheduler=scheduler
