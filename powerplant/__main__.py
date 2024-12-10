from powerplant import * # classe test

""" #inclure les classes ici "from powerplant.nom_du_fichier import nom_de_la_classe"
from .classes import price """

def main():
    prix = KwhPrice('assets/kwh_price.csv')
    print(prix.get_price(30))
    

if __name__ == "__main__":
    main()

