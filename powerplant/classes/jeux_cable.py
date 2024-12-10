import tkinter as tk
import time
import math
from tkinter import messagebox
import random
from playsound import playsound

class JeuDeCablage:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-jeu : Câblage")
        self.root.geometry("600x500")
        # Jouer un fichier WAV
        playsound("success-fanfare-trumpets-6185.wav")
        # Timer
        self.time_limit = 60  # secondes
        self.start_time = time.time()

        # Canvas de jeu
        self.canvas = tk.Canvas(self.root, width=600, height=500, bg="white")
        self.canvas.pack()

        # Points de départ et d'arrivée
        self.start_points = [(50, 100), (50, 200), (50, 300), (50, 400)]  # Points A

        # Points d'arrivée et Points led (y associés aux y des points A)
        self.end_points, self.view_Point = self.generate_associated_points(self.start_points)

        self.start_circles = {}  # Garde la trace des objets graphiques des points de départ
        self.end_circles = {}  # Garde la trace des objets graphiques des points d'arrivée
        self.view_circles = {}  # Garde la trace des objets graphiques des points led
        self.connection_valid = {}  # Garde la validité de la connexion

        # Mappage des points d'arrivée aux points de visualisation
        self.end_to_view_mapping = dict(zip(self.end_points, self.view_Point))

        # Couleurs des câbles et des points
        self.cable_colors = ["blue", "purple", "orange", "red"]
        self.color_mapping = dict(zip(self.cable_colors, range(len(self.cable_colors))))

        # Dessiner les points
        self.draw_points(self.start_points, self.cable_colors, "start", self.start_circles)
        self.draw_points(self.end_points, self.cable_colors, "end", self.end_circles)
        self.draw_points(self.view_Point, ["red" for i in range(len(self.view_Point))], "view", self.view_circles)

        # Variables pour le tracé
        self.current_path = []  # Liste des segments de la ligne actuelle
        self.current_start_point = None  # Point de départ en cours
        self.lines_connected = 0  # Nombre de connexions réussies
        self.all_paths = []  # Liste des chemins terminés

        # Événements
        self.canvas.tag_bind("start", "<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        # Timer
        self.update_timer()

    def show_custom_popup():
        # Créer une fenêtre popup personnalisée
        popup = tk.Toplevel()
        popup.title("Popup Personnalisée")
        popup.geometry("300x150")  # Taille de la popup

        # Modifier le fond de la fenêtre
        popup.config(bg="lightblue")  # Changer la couleur de fond

        # Ajouter un texte dans la popup
        label = tk.Label(popup, text="Ceci est une popup avec un fond personnalisé.", bg="lightblue")
        label.pack(pady=20)

        # Ajouter un bouton pour fermer la popup
        close_button = tk.Button(popup, text="Fermer", command=popup.destroy)
        close_button.pack()

    def generate_associated_points(self, start_points):
        """Associe les points B et led aux positions y des points A."""
        # Extraire les positions y des points de départ
        start_y_positions = [point[1] for point in start_points]

        # Mélanger aléatoirement les positions y pour les points B et view
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
                # self.connection_valid[point] = self.canvas.create_oval(
                #     point[0] - 15, point[1] - 15, point[0] + 15, point[1] + 15,
                #     fill="red", outline="black", width=2, tags="connection_check"
                # )  # Cercle de vérification
                break

    def drag_line(self, event):
        """Permet un aperçu dynamique de la courbe du câble."""
        if self.current_start_point:
            # Calcule une courbe réaliste
            preview_path = self.calculate_cable_path(self.current_start_point, (event.x, event.y))
            self.canvas.delete("current_line")
            self.draw_cable(preview_path, self.current_color, "current_line")

    def stop_drag(self, event):
        """Fin du tracé, valider et fixer le câble."""
        if not self.current_start_point:
            return

        # Trouver le point d'arrivée le plus proche
        end_point = self.get_closest_end_point(event.x, event.y)
        if end_point:
            # Vérifier si la couleur du câble correspond à la couleur de l'arrivée
            start_index = self.start_points.index(self.current_start_point)
            end_index = self.end_points.index(end_point)

            # Si les couleurs ne correspondent pas, ne pas valider la connexion
            if self.cable_colors[start_index] != self.cable_colors[end_index]:
                messagebox.showwarning("Erreur", "La couleur du câble doit correspondre à celle du point d'arrivée!")
                self.canvas.delete("current_line")
                self.current_start_point = None
                self.canvas.itemconfig(self.connection_valid[self.current_start_point], fill="red")  # Cercle rouge
                return

            # Calcul de la courbe finale
            final_path = self.calculate_cable_path(self.current_start_point, end_point)

            # Dessiner le câble final
            self.draw_cable(final_path, self.current_color)

            # Changer les couleurs des points de départ et d'arrivée pour correspondre à la couleur du câble
            self.canvas.itemconfig(self.start_circles[self.current_start_point], fill=self.current_color)
            self.canvas.itemconfig(self.end_circles[end_point], fill=self.current_color)

            # Mettre à jour les points et les connexions
            self.start_points.remove(self.current_start_point)
            self.end_points.remove(end_point)
            self.cable_colors.remove(self.current_color)
            self.lines_connected += 1

            # Utilisation du dictionnaire pour accéder à view_Point
            view_point = self.end_to_view_mapping.get(end_point)
            if view_point:
                self.canvas.itemconfig(self.view_circles[view_point], fill="green")

        # Réinitialiser
        self.current_start_point = None
        self.canvas.delete("current_line")

        # Vérifier si toutes les connexions sont faites
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
            # Simuler une gravité : les points intermédiaires descendent légèrement
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
        print("Tous les fils connectés avec succès !")
        self.root.after(2000, self.root.quit)  # Fermer après 2 secondes

    def update_timer(self):
        """Met à jour le chronomètre du jeu."""
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time

        if remaining_time <= 0:
            self.root.title("Temps écoulé !")
            self.root.quit()  # Fermer la fenêtre
        else:
            self.root.title(f"Mini-jeu : Câblage - Temps restant : {int(remaining_time)}s")
            self.root.after(1000, self.update_timer)

