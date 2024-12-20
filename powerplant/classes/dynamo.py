import customtkinter as ctk
import math

class Dynamo:
    # Initialisation de la puissance de sortie du dynamo
    def __init__(self, power_output):
        self.power_output = power_output

    # Retourne la puissance de sortie actuelle du dynamo
    def generate_power(self):
        return self.power_output

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("Dynamo")
        self.geometry("500x500")

        # Création d'une instance de Dynamo avec une puissance initiale de 0
        self.dynamo = Dynamo(0)

        # Création d'un label pour afficher la puissance de sortie du dynamo
        self.label = ctk.CTkLabel(self, text=f"Dynamo Power Output: {self.dynamo.generate_power()}")
        self.label.pack(pady=20)

        # Création d'un canvas pour dessiner les cercles et la ligne
        self.canvas = ctk.CTkCanvas(self, width=400, height=400)
        self.canvas.pack()

        # Initialisation des variables pour les cercles et l'animation
        self.outer_circle_radius = 150
        self.inner_circle_radius = 20
        self.angle = 0
        self.speed = 0  # Variable pour contrôler la vitesse

        # Création du cercle extérieur
        self.outer_circle = self.canvas.create_oval(100, 100, 300, 300, outline="black")
        # Création de la ligne reliant le centre du cercle extérieur au cercle intérieur
        self.line = self.canvas.create_line(200, 200, 200, 200, fill="blue", width=5)
        # Création du cercle intérieur
        self.inner_circle = self.canvas.create_oval(250, 180, 290, 220, fill="red")

        # Liaison de l'événement de clic sur le canvas avec la méthode on_outer_circle_click
        self.canvas.bind("<Button-1>", self.on_outer_circle_click)

        # Démarrage de l'animation
        self.update_animation()

    def on_outer_circle_click(self, event):
        # Vérifie si le clic est à l'intérieur du cercle extérieur
        if self.is_inside_circle(event.x, event.y, 200, 200, self.outer_circle_radius):
            # Incrémente l'angle de 10 degrés
            self.angle += 10

    def is_inside_circle(self, x, y, circle_x, circle_y, radius):
        # Vérifie si un point (x, y) est à l'intérieur d'un cercle de centre (circle_x, circle_y) et de rayon radius
        return (x - circle_x) ** 2 + (y - circle_y) ** 2 <= radius ** 2

    def update_animation(self):
        # Incrémente l'angle en utilisant la variable de vitesse
        self.angle += self.speed
        if self.angle >= 360:
            # Réinitialise l'angle et augmente la puissance de sortie du dynamo
            self.angle = 0
            self.dynamo.power_output += 1
            self.label.configure(text=f"Dynamo Power Output: {self.dynamo.generate_power()}")

        # Calcule les nouvelles coordonnées du cercle intérieur
        x = 200 + self.outer_circle_radius * math.cos(math.radians(self.angle))
        y = 200 + self.outer_circle_radius * math.sin(math.radians(self.angle))

        # Met à jour les coordonnées du cercle intérieur et de la ligne
        self.canvas.coords(self.inner_circle, x - self.inner_circle_radius, y - self.inner_circle_radius, x + self.inner_circle_radius, y + self.inner_circle_radius)
        self.canvas.coords(self.line, 200, 200, x, y)

        # Planifie la prochaine mise à jour de l'animation
        self.after(50, self.update_animation)

if __name__ == "__main__":
    # Crée et lance l'application
    app = App()
    app.mainloop()