# Importantion de toutes les classes et méthodes
from powerplant import *
import os


def main():
    kwhCSV_path = os.path.join("assets", "kwh_price.csv")
    prix = KwhPrice(kwhCSV_path)
    print(prix.get_price(30))
    

if __name__ == "__main__":
    main()

