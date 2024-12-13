# Fichier de gestion du marketing
# Définition du prix de vente utilisateur
# Calcul des gain/s en fonction de la demande

class marketing:
    def __init__(self):
        self.user_price = 0
        self.bank = 0

    def set_user_price(self, price):    #définit le prix de vente utilisateur
        self.user_price = price
        return self.user_price

    def get_user_price(self):   #retourne le prix de vente utilisateur
        return self.user_price
    
    def get_user_bank(self):    #retourne la valeur de la banque utilisateur
        return self.bank
    
    def get_user_gain(self, demand, storage):    #retourne les gains utilisateur par seconde
        if storage == 0:
            return 0
        return self.user_price * demand
    
    def update_user_bank(self, gain):
        self.bank += gain
        return self.bank