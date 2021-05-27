class Sink:

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        entitatsEliminades=0
        self.state='idle'
        self.scheduler=scheduler
