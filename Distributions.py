import numpy as np

def setSeed(seed):
        np.random.seed(seed)

def distribucioNormal(center, scale):
        return np.random.normal(center, scale, None)

def distibucioUniforme():
        return np.random.uniform()