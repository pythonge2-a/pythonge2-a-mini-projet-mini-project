import customtkinter
import colors

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the grid layout for the MainFrame
        self.grid_rowconfigure(0, weight=1)  # One row
        self.grid_columnconfigure((0, 1, 2), weight=1)  # Three columns

        # add widgets onto the frame
        self.price_frame = PriceFrame(master=self)
        self.price_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.stock_frame = StockFrame(master=self)
        self.stock_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.invest_frame = InvestFrame(master=self)
        self.invest_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.marketing_frame = MarketingFrame(master=self)
        self.marketing_frame.grid(row=1, column=1)

class PriceFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.price_label = customtkinter.CTkLabel(self, text="fr -----")
        self.price_label.pack(pady=10)
        self.price_label.grid(row=0,column=0, sticky="w")

        self.kwh_label = customtkinter.CTkLabel(self, text="///// kWh")
        self.kwh_label.grid(row=1,column=0,padx=10,pady=15,sticky="w")

        self.radio_var = customtkinter.StringVar(value="coal")  # variable pour 

        self.coal_button = customtkinter.CTkRadioButton(self, text="coal", variable=self.radio_var, value="coal")
        self.coal_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.solar_button = customtkinter.CTkRadioButton(self, text="solar panel", variable=self.radio_var, value="solar")
        self.solar_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.turbine_button = customtkinter.CTkRadioButton(self, text="wind turbine", variable=self.radio_var, value="wind")
        self.turbine_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.uranium_button = customtkinter.CTkRadioButton(self, text="uranium", variable=self.radio_var, value="uranium")
        self.uranium_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")
   
class StockFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.stock_label = customtkinter.CTkLabel(self, text="Stockage :")
        self.stock_label.grid(row=0,column=0, padx=10, pady=15, sticky="w")
    
        self.capa_button = customtkinter.CTkButton(self,text="capacitor")
        self.capa_button.grid(row=1,column=0, padx=10, pady=5, sticky="w")

        self.pile_button = customtkinter.CTkButton(self,text="aa cell")
        self.pile_button.grid(row=2,column=0, padx=10, pady=5, sticky="w")

        self.batterie_button = customtkinter.CTkButton(self,text="batterie")
        self.batterie_button.grid(row=3,column=0, padx=10, pady=5, sticky="w")

        self.graphene_button = customtkinter.CTkButton(self,text="graphene")
        self.graphene_button.grid(row=4,column=0, padx=10, pady=5, sticky="w")

        self.antimat_button = customtkinter.CTkButton(self,text="antimatiere")
        self.antimat_button.grid(row=5,column=0, padx=10,pady=5, sticky="w")

class InvestFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.invest_label = customtkinter.CTkLabel(self, text="Investissements :")
        self.invest_label.grid(row=0,column=0, padx=10, pady=15, sticky="w")
    
        self.monkey_button = customtkinter.CTkButton(self,text="singe sur velo")
        self.monkey_button.grid(row=1,column=0, padx=10, pady=5, sticky="w")

        self.dyson_button = customtkinter.CTkButton(self,text="dyson sphere")
        self.dyson_button.grid(row=2,column=0, padx=10, pady=5, sticky="w")

class MarketingFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.invest_label = customtkinter.CTkLabel(self, text="Marketing :")
        self.invest_label.grid(row=0,column=0, padx=10, pady=15, sticky="w")

        self.price_label = customtkinter.CTkLabel(self, text="--- fr")
        self.price_label.grid(row=1,column=0,padx=5,pady=5)

        self.increasePrice_button = customtkinter.CTkButton(
            master=self,
            text="+",
            corner_radius=10,  # Set the corner radius to half the height for a circular shape
            width=20,  # Make the button square for a true circle
            height=20,
            fg_color="white",  # Set the button color
            text_color=colors.green  # Set the text color
        )
        self.increasePrice_button.grid(row=1,column=1)
        self.decreasePrice_button = customtkinter.CTkButton(
            master=self,
            text="-",
            corner_radius=10,  # Set the corner radius to half the height for a circular shape
            width=20,  # Make the button square for a true circle
            height=20,
            fg_color="white",  # Set the button color
            text_color=colors.red  # Set the text color
        )
        self.decreasePrice_button.grid(row=1,column=2)

        self.demand_label = customtkinter.CTkLabel(self, text="Demande -- %")
        self.demand_label.grid(row=2,column=0, sticky="w")

        self.gainpers_label = customtkinter.CTkLabel(self, text="Gain/s ---")
        self.gainpers_label.grid(row=2,column=0, sticky="w")

        self.stockMax_label = customtkinter.CTkLabel(self, text="Stock --- /max")
        self.stockMax_label.grid(row=2,column=0, sticky="w")


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=10)
        self.button1 = customtkinter.CTkButton(self, text="bouton 1", command=self.button1_action)
        self.button1.grid(row=1,column=0,padx=10)
    def button1_action(self) :
        self.button1.configure(state="disabled", text="womp womp")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MainFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    