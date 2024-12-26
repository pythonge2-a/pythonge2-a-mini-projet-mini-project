import math

class LowPass:
    def __init__(self,order,cutoff_frequency):
        self.order = order
        self.cutoff_frequency = cutoff_frequency

    def transfer_function(self, frequency):
        w0 = 2 * math.pi * self.cutoff_frequency
        return 1 / math.sqrt(1 + (frequency / w0) ** (2*self.order))
    
class HighPass:
    def __init__(self,order,cutoff_frequency):
        self.order = order
        self.cutoff_frequency = cutoff_frequency

    def transfer_function(self, frequency):
        w0 = 2 * math.pi * self.cutoff_frequency
        return 1 / math.sqrt(1 + (frequency / w0) ** (2*self.order))

class BandPass:
    def __init__(self,order,cutoff_frequency):
        self.order = order
        self.cutoff_frequency = cutoff_frequency

    def transfer_function(self, frequency):
        w0 = 2 * math.pi * self.cutoff_frequency
        return 1 / math.sqrt(1 + (frequency / w0) ** (2*self.order))