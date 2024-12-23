# gère le stockage de l'énergie produite par les différentes sources d'énergie

class Storage :
    def __init__(self):
        self.stock = 0
        self.stock_max = 1000
    
    def add_stock(self, stk):
        self.stock += stk
        if self.stock > self.stock_max:
            self.stock = self.stock_max
        return self.stock
    
    def set_stock_max(self, max):
        self.stock_max = max
        return self.stock_max
    
