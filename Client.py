from Distributions import distribucioNormal
from SimulationParameters import Parameters

class Client:
    pes = 0

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        self.scheduler=scheduler
        self.pes = distribucioNormal(Parameters.tiempoEnCajaMedia, Parameters.tiempoEnCajaVarianza)
        # print("Se ha creado un Cliente con peso = ", pes)
        
