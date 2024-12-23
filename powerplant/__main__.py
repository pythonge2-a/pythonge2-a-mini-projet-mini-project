# Importantion de toutes les classes et méthodes
from powerplant import *
import os

app = App() # Création de l'application globale

def loop(): #boucle de jeu , actualise les paramètres du jeu toute les secondes
    demand = 20
    app.update_game()
    if app.my_frame.price_frame.kwh_stock > 0:
        prix_vente = app.my_frame.marketing_frame.selling_price
        unite_vendue = app.my_frame.price_frame.kwh_stock * demand / 100

        if app.my_frame.price_frame.kwh_stock < 1: #forcer la vente si le stock est inférieur à 1
            unite_vendue = app.my_frame.price_frame.kwh_stock

        gain = prix_vente * unite_vendue
        app.my_frame.price_frame.kwh_stock -= unite_vendue
        app.my_frame.price_frame.money += gain

    app.after(1000, loop)

def run():
    loop()
    app.mainloop()

def main(): #initialisation des paramètres de lancement du jeu
    '''
    kwhCSV_path = os.path.join("assets", "kwh_price.csv")
    prix = KwhPrice(kwhCSV_path) #prix du jour'''
    app.my_frame.marketing_frame.set_stock_max(1000)
    app.my_frame.price_frame.set_kwh_stock(1000)

    run()

if __name__ == "__main__":
    main()

