# Importantion de toutes les classes et méthodes
from powerplant import *
import os

def main():

    kwhCSV_path = os.path.join("assets", "kwh_price.csv")
    prix = KwhPrice(kwhCSV_path) #prix du jour
    '''
    market = marketing() # Gestion du marketing
    storage = Storage() # Gestion du stockage

    market.bank = 1000 # Banque de l'utilisateur
    storage.stock_max = 500 # Stock max
    storage.stock = 200 # Stock de l'utilisateur

    app = App() # Création de l'application
    
    app.my_frame.price_frame.set_kwh_stock(storage.stock)
    app.my_frame.marketing_frame.set_stock_max(storage.stock_max)
    app.my_frame.price_frame.set_money(market.bank)'''
    app = App()
    app.mainloop()    

if __name__ == "__main__":
    main()

