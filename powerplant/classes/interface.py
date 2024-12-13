import customtkinter

class MainFrame(customtkinter.ctkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.price_label = customtkinter.CTkLabel(self, text="$-----")
        self.price_label.pack(pady=10)
        
    pass
class StockFrame(customtkinter.ctkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
    pass
class InvestFrame(customtkinter.ctkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
    pass



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
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    