# Fichier de gestion de la production d'énergie
# Gère la production active et passive d'énergie

class production:
    def __init__(self):
        self.production_active = 0
        self.production_passive = 0

        # Assets production passive
        self.singe = 1          # Singe sur un vélo
        self.hamster = 5        # Hamster dans une roue
        self.fontaine = 10      # Fontaine à roue

