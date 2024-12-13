import tkinter as tk
from tkinter import messagebox
import time
import random
import math
import pygame

# Initialiser le module mixer de pygame
pygame.mixer.init()

# Charger le fichier audio avec un chemin absolu et une chaîne brute
sound_victoire = pygame.mixer.Sound(r"assets\fichier_mp3\success-fanfare-trumpets-6185.mp3")
sound_defaite = pygame.mixer.Sound(r"assets\fichier_mp3\failure-1-89170.mp3")
sound_faux = pygame.mixer.Sound(r"assets\fichier_mp3\wrong-47985.mp3")
sound_juste = pygame.mixer.Sound(r"assets\fichier_mp3\electric-155027.mp3")

class JeuDeCablage:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-jeu : Câblage")
        nb_points = 6
        self.root.geometry(f"600x{(nb_points+1)*100}")

        # Timer
        self.time_limit = nb_points * 3  # secondes
        self.start_time = time.time()

       # Label pour afficher le timer avec un effet de boîte
        self.timer_label = tk.Label(self.root, text="Temps restant : 0", font=("Arial", 14), bg="grey",
                            borderwidth=2, relief="solid", padx=10, pady=5)
        self.timer_label.pack(pady=10)

        # Canvas de jeu
        self.canvas = tk.Canvas(self.root, width=600, height=(nb_points+1)*100, bg="white")
        self.canvas.pack()

        # Points de départ et d'arrivée
        self.start_points = [(50, y*100) for y in range(1, nb_points+1)]
        random.shuffle(self.start_points)

        # Points d'arrivée et Points led (y associés aux y des points A)
        self.end_points, self.view_Point = self.generate_associated_points(self.start_points)

        self.start_circles = {}
        self.end_circles = {}
        self.view_circles = {}
        self.connection_valid = {}

        # Mappage des points d'arrivée aux points de visualisation
        self.end_to_view_mapping = dict(zip(self.end_points, self.view_Point))

        # Couleurs des câbles et des points
        self.cable_colors = ["blue", "purple", "orange", "red", "pink", "brown"]
        self.color_mapping = dict(zip(self.cable_colors, range(len(self.cable_colors))))

        # Dessiner les points
        self.draw_points(self.start_points, self.cable_colors, "start", self.start_circles)
        self.draw_points(self.end_points, self.cable_colors, "end", self.end_circles)
        self.draw_points(self.view_Point, ["red" for i in range(len(self.view_Point))], "view", self.view_circles)

        # Variables pour le tracé
        self.current_path = []
        self.current_start_point = None
        self.lines_connected = 0
        self.all_paths = []

        # Événements
        self.canvas.tag_bind("start", "<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        # Timer
        self.update_timer()

    def generate_associated_points(self, start_points):
        """Associe les points B et led aux positions y des points A."""
        start_y_positions = [point[1] for point in start_points]
        random.shuffle(start_y_positions)

        # Associer les y mélangés aux points d'arrivée et led
        end_points = [(450, y) for y in start_y_positions]
        view_points = [(500, y) for y in start_y_positions]

        return end_points, view_points

    def draw_points(self, points, colors, tag, circles_dict):
        """Dessine les points donnés sur le canvas."""
        for i in range(len(points)):
            x, y = points[i]
            color = colors[i]
            circle_id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10,
                                                fill=color, outline="black", tags=tag)
            circles_dict[(x, y)] = circle_id

    def start_drag(self, event):
        """Début du tracé depuis un point de départ."""
        for i, point in enumerate(self.start_points):
            if self.is_inside_circle(event.x, event.y, point, 10):
                self.current_start_point = point
                self.current_color = self.cable_colors[i]  # Attribuer une couleur unique
                break

    def drag_line(self, event):
        """Permet un aperçu dynamique de la courbe du câble."""
        if self.current_start_point:
            preview_path = self.calculate_cable_path(self.current_start_point, (event.x, event.y))
            self.canvas.delete("current_line")
            self.draw_cable(preview_path, self.current_color, "current_line")

    def stop_drag(self, event):
        """Fin du tracé, valider et fixer le câble."""
        if not self.current_start_point:
            return

        end_point = self.get_closest_end_point(event.x, event.y)
        if end_point:
            start_index = self.start_points.index(self.current_start_point)
            end_index = self.end_points.index(end_point)

            # Vérification de la couleur du câble
            if self.cable_colors[start_index] != self.cable_colors[end_index]:
                sound_faux.play()
                self.canvas.delete("current_line")
                self.current_start_point = None
                return

            final_path = self.calculate_cable_path(self.current_start_point, end_point)
            self.draw_cable(final_path, self.current_color)

            sound_juste.play()

            self.canvas.itemconfig(self.start_circles[self.current_start_point], fill=self.current_color)
            self.canvas.itemconfig(self.end_circles[end_point], fill=self.current_color)

            self.start_points.remove(self.current_start_point)
            self.end_points.remove(end_point)
            self.cable_colors.remove(self.current_color)
            self.lines_connected += 1

            view_point = self.end_to_view_mapping.get(end_point)
            if view_point:
                self.canvas.itemconfig(self.view_circles[view_point], fill="green")

        self.current_start_point = None
        self.canvas.delete("current_line")

        if self.lines_connected == len(self.start_circles):
            self.end_game()

    def calculate_cable_path(self, start, end, gravity=50, segments=20):
        """Calcule une courbe réaliste pour le câble."""
        x1, y1 = start
        x2, y2 = end
        path = []

        for i in range(segments + 1):
            t = i / segments
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t + math.sin(t * math.pi) * gravity
            path.append((x, y))

        return path

    def draw_cable(self, path, color, tag=None):
        """Dessine une courbe lisse représentant le câble."""
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3, tags=tag)

    def get_closest_end_point(self, x, y):
        """Retourne le point d'arrivée le plus proche."""
        for point in self.end_points:
            if self.is_inside_circle(x, y, point, 10):
                return point
        return None

    def is_inside_circle(self, x, y, center, radius):
        """Vérifie si le point (x, y) est à l'intérieur du cercle défini par (center, radius)."""
        return (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

    def end_game(self):
        """Fin du jeu."""
        self.canvas.create_text(300, 250, text="Vous avez réussi !", font=("Arial", 20), fill="green")
        sound_victoire.play()
        self.root.after(2000, self.root.quit)

    def update_timer(self):
        """Met à jour le chronomètre du jeu."""
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time

        if remaining_time <= 0:
            self.canvas.create_text(300, 250, text="Temps écoulé !", font=("Arial", 20), fill="red")  # Afficher le message
            sound_defaite.play()
            self.root.after(2000, self.root.quit)  # Fermer après 2 secondes
        else:
            self.timer_label.config(text=f"Temps restant : {int(remaining_time)}s")
            self.root.after(1000, self.update_timer)

# Lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    game = JeuDeCablage(root)
    root.mainloop()
