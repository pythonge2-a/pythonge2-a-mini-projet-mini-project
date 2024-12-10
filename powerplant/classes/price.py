# Fichier de classe pour la génération des prix.
# get_price(day) retourne le prix de l'électricité pour le jour donné.
# si day < 0, une exception est levée.
# le fichier comporte le prix pour 2895 jours (8 ans) si day est supérieur à 2894
# alors le prix du jour est calculé en faisant un modulo 2895 et ne génère pas d'exception.

import pandas as pd

class KwhPrice: # génération des prix de l'électricité
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    #charge les données du fichier csv et convertit les prix de MWh en kWh
    def _load_data(self):
        df = pd.read_csv(self.file_path)
        df['Baseload_CHF_kWh'] = df['Baseload_CHF_MWh'] / 1000
        df.reset_index(drop=True, inplace=True) #réinitialise l'index
        return df['Baseload_CHF_kWh'].tolist()

    #retourne le prix du jour
    def get_price(self, day): 
        if day < 0 : 
            raise IndexError("Erreur indice jour inférieur à 0")

        return self.data[day%len(self.data)]
    

'''Exemple d'utilisation''''''
from powerplant.price import KwhPrice 

def main():
    file_path = "assets/kwh_price.csv"
    kwh_price = KwhPrice(file_path)
    print(kwh_price.get_price(0)) # prix du premier jour
    print(kwh_price.get_price(2894)) # prix du dernier jour 
    print(kwh_price.get_price(2895)) # prix du premier jour (rebouclement) 
if __name__ == "__main__":
    main()

'''