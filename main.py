from filters import Filters

def main():
    # Initialisation de Filters
    filters = Filters()

    # Appeler le calcul des composants pour Tchebychev passe-bas d'ordre 2
    result = filters.snk.tchebychev.2.components(1000, 2000, 1e-6, 2e-6)
    print("Résultat des composants :", result)


## TEST A VOIR AVEC VOUS SI OK
L = 10e-3
C  = 1e-6
R = 1000

try:
    resonant_frequency = filters.passives.band_pass.BandPassFilter.resonant_frequency(L, C)
    quality_factor = filters.passives.band_pass.BandPassFilter.quality_factor(R, L, C)
    bandwidth = filters.passives.band_pass.BandPassFilter.bandwidth(resonant_frequency, quality_factor)

    #Affichage des résultats
    print("Résultats pour le filtre passe-bande:\n"
          f"- Fréquence de résonance: {resonant_frequency:.2f} Hz\n"
          f"- Facteur de qualité: {quality_factor:.2f}\n"
          f"- Bande passante: {bandwidth:.2f} Hz")
except ValueError as e:
    print(f"Erreur: {e}")

if __name__ == "__main__":
    main()