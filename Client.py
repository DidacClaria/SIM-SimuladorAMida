import numpy as np

class Client:
    pes = 0

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        self.scheduler=scheduler
        pes = distribucioNormal(10, 5)
        print("Se ha creado un Cliente con peso = " + pes)
    
    def distribucioNormal(center, scale):
        return np.random.normal(center, scale, 1000)
        
