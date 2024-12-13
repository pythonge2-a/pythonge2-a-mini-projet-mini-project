# Fichier de gestion de la production d'énergie
# Gère la production active et passive d'énergie

class production:
    def __init__(self):
        self.production_active = 0
        self.production_passive = 0

        # Assets production passive
        self.singe          = 1         # Singe sur un vélo
        self.hamster        = 5         # Hamster dans une roue
        self.moulin         = 10        # Moulin à eau
        self.eolienne       = 25        # Éolienne
        self.champignon     = 50        # Ferme de champignons bioluminescents
        self.solaire        = 100       # Panneau solaire
        self.biomasse       = 250       # Ferme de biomasse
        self.nucleaire      = 500       # Centrale nucléaire
        self.fusion         = 1000      # Réacteur de fusion
        self.anti_matiere   = 5000      # Réacteur à antimatière
        self.dyson          = 10000     # Sphère de Dyson
        self.dimension      = 100000    # Centrale dimensionnelle
        self.grandmere      = 1000000   # L'amour de grand-mère

    def set_production_active(self, n):
        self.production_active = n
        return self.production_active

    def update_production_passive(self, nSinge, nHamster, nMoulin, nEolienne, nChampignon, nSolaire, nBiomasse, nNucleaire, nFusion, nAntiMatiere, nDyson, nDimension, nGrandmere):
        self.production_passive = nSinge*self.singe + nHamster*self.hamster + nMoulin*self.moulin + nEolienne*self.eolienne + nChampignon*self.champignon + nSolaire*self.solaire + nBiomasse*self.biomasse + nNucleaire*self.nucleaire + nFusion*self.fusion + nAntiMatiere*self.anti_matiere + nDyson*self.dyson + nDimension*self.dimension + nGrandmere*self.grandmere
        return self.production_passive
    
    def production_totale(self):
        return self.production_active + self.production_passive

        

