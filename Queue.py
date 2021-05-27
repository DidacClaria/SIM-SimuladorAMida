class Queue:
    pesTotal = 0
    entitats = []

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        entitatsTractades=0
        self.state='idle'
        self.scheduler=scheduler
        self.pesTotal = 0
        print("Se ha creado una Queue")

    def recullEntitat(self,time,entitat):
        self.entitats.append(entitat)
        self.entitatsTractades=self.entitatsTractades+1
        print("Una queue ha recibido una entidad")
