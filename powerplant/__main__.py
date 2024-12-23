# Importantion de toutes les classes et méthodes
from powerplant import *
import os
import time

def main():
    '''
    kwhCSV_path = os.path.join("assets", "kwh_price.csv")
    prix = KwhPrice(kwhCSV_path) #prix du jour'''
    app = App()
    app.my_frame.marketing_frame.set_stock_max(1000)
    app.my_frame.price_frame.set_kwh_stock(1000)
    app.run()


if __name__ == "__main__":
    main()

