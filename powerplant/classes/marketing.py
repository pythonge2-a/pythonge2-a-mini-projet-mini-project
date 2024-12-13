# Fichier de gestion du marketing
# Définition du prix de vente utilisateur
# Calcul des gain/s en fonction de la demande

class marketing:
    def __init__(self, user_price):
        self.user_price = user_price
        self.bank = 0

    def get_user_price(self):   #retourne le prix de vente utilisateur
        return self.user_price
    
    def get_user_gain(self, demand):    #retourne les gains utilisateur par seconde
        return self.user_price * demand