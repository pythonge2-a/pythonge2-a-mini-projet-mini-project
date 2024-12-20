import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonction pour générer une courbe sinus
def generate_sinus(amplitude, frequency, x_values):
    return amplitude * np.sin(2 * np.pi * frequency * x_values)

# Classe principale du jeu
class SinusMatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Correspondance de Sinus")
        
        # Configuration principale de la fenêtre
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Génération de la courbe cible
        self.x_values = np.linspace(0, 1, 500)
        self.target_amplitude = np.random.uniform(0.5, 2.0)
        self.target_frequency = np.random.uniform(1.0, 3.0)
        self.target_y_values = generate_sinus(self.target_amplitude, self.target_frequency, self.x_values)

        # Initialisation des paramètres utilisateur
        self.user_amplitude = 1.0
        self.user_frequency = 1.0
        self.user_y_values = generate_sinus(self.user_amplitude, self.user_frequency, self.x_values)

        # Création de la figure Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Ajustez l'Amplitude et la Fréquence")
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(-2.5, 2.5)
        self.target_line, = self.ax.plot(self.x_values, self.target_y_values, label="Cible", color="blue")
        self.user_line, = self.ax.plot(self.x_values, self.user_y_values, label="Votre Sinus", color="red", linestyle="--")
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Sliders pour ajuster amplitude et fréquence
        self.amplitude_slider = ctk.CTkSlider(self.frame, from_=0.5, to=2.0, command=self.update_amplitude)
        self.amplitude_slider.set(self.user_amplitude)
        self.amplitude_slider.pack(pady=10)

        self.frequency_slider = ctk.CTkSlider(self.frame, from_=1.0, to=3.0, command=self.update_frequency)
        self.frequency_slider.set(self.user_frequency)
        self.frequency_slider.pack(pady=10)

        # Bouton pour vérifier la correspondance
        self.check_button = ctk.CTkButton(self.frame, text="Vérifier", command=self.check_match)
        self.check_button.pack(pady=10)

        # Label pour afficher le résultat
        self.result_label = ctk.CTkLabel(self.frame, text="Ajustez les valeurs pour correspondre à la courbe cible.")
        self.result_label.pack(pady=10)

    def update_amplitude(self, value):
        self.user_amplitude = float(value)
        self.update_user_sinus()

    def update_frequency(self, value):
        self.user_frequency = float(value)
        self.update_user_sinus()

    def update_user_sinus(self):
        self.user_y_values = generate_sinus(self.user_amplitude, self.user_frequency, self.x_values)
        self.user_line.set_ydata(self.user_y_values)
        self.canvas.draw()

    def check_match(self):
        diff = np.sum(np.abs(self.target_y_values - self.user_y_values))
        if diff < 0.1:
            self.result_label.configure(text="Bravo ! Vous avez correspondu au sinus cible !", text_color="green")
        else:
            self.result_label.configure(text=f"Encore un peu... Différence: {diff:.2f}", text_color="red")

# Lancement de l'application
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Apparence claire ou sombre selon le système
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = SinusMatchingGame(root)
    root.mainloop()
