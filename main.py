from filters import Filters

def main():
    # Initialisation de Filters
    filters = Filters()

    # Appeler le calcul des composants pour Tchebychev passe-bas d'ordre 2
    result = filters.snk.tchebychev.lowpass._2.components(2, 4, 5, 10)
    print("Résultat des composants :", result)

if __name__ == "__main__":
    main()
