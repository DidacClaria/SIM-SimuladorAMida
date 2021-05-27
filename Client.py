from Distributions import distribucioNormal

class Client:
    pes = 0

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        self.scheduler=scheduler
        pes = distribucioNormal(10, 1)
        print("Se ha creado un Cliente con peso = ", pes)
        
