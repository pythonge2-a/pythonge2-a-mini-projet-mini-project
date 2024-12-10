# Importantion de toutes les classes et méthodes
from powerplant import *


def main():
    prix = KwhPrice('assets/kwh_price.csv')
    print(prix.get_price(30))
    

if __name__ == "__main__":
    main()

