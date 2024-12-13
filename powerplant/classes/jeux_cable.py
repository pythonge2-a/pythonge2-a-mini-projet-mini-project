import customtkinter as ctk
import pygame
import time
import random
import math

# Initialiser le module mixer de pygame
pygame.mixer.init()

# Charger les fichiers audio
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

        # Conteneur principal
        self.frame = ctk.CTkFrame(self.root, width=600, height=(nb_points + 1) * 100)
        self.frame.pack()

        # Timer
        self.time_limit = nb_points * 3  # secondes
        self.start_time = time.time()

        # Points de départ et d'arrivée
        self.start_points = [(50, y * 100) for y in range(1, nb_points + 1)]
        random.shuffle(self.start_points)
        self.end_points, self.view_Point = self.generate_associated_points(self.start_points)

        self.start_circles = {}
        self.end_circles = {}
        self.view_circles = {}
        self.connection_valid = {}
        self.end_to_view_mapping = dict(zip(self.end_points, self.view_Point))

        # Couleurs des câbles et des points
        self.cable_colors = ["blue", "purple", "orange", "red", "pink", "brown"]
        self.color_mapping = dict(zip(self.cable_colors, range(len(self.cable_colors))))

        # Dessiner les points
        self.draw_points(self.start_points, self.cable_colors, "start", self.start_circles)
        self.draw_points(self.end_points, self.cable_colors, "end", self.end_circles)
        self.draw_points(self.view_Point, ["red" for _ in range(len(self.view_Point))], "view", self.view_circles)

        # Variables pour le tracé
        self.current_path = []
        self.current_start_point = None
        self.lines_connected = 0
        self.all_paths = []

        # Variables de gestion du tracé
        self.is_dragging = False
        self.dragged_line = None

        # Événements
        self.frame.bind("<Button-1>", self.start_drag)
        self.frame.bind("<B1-Motion>", self.drag_line)
        self.frame.bind("<ButtonRelease-1>", self.stop_drag)

        # Timer
        self.update_timer()

    def generate_associated_points(self, start_points):
        """Associe les points B et led aux positions y des points A."""
        start_y_positions = [point[1] for point in start_points]
        random.shuffle(start_y_positions)
        end_points = [(450, y) for y in start_y_positions]
        view_points = [(500, y) for y in start_y_positions]
        return end_points, view_points

    def draw_points(self, points, colors, tag, circles_dict):
        """Dessine les points donnés en utilisant des widgets CTk sous forme de cercles."""
        for i, (x, y) in enumerate(points):
            color = colors[i]

            # Création d'un label pour simuler un cercle sans texte
            circle = ctk.CTkLabel(self.frame, width=20, height=20, corner_radius=10, fg_color=color)
            circle.place(x=x - 10, y=y - 10)  # Positionner comme un cercle centré
            circles_dict[(x, y)] = circle

    def start_drag(self, event):
        """Début du tracé depuis un point de départ."""
        for i, point in enumerate(self.start_points):
            if self.is_inside_circle(event.x, event.y, point, 10):
                self.current_start_point = point
                self.current_color = self.cable_colors[i]
                self.is_dragging = True
                self.current_path = [point]
                break

    def drag_line(self, event):
        """Dessine la ligne en mouvement lors du drag."""
        if self.is_dragging and self.current_start_point:
            x1, y1 = self.current_path[-1]
            x2, y2 = event.x, event.y
            self.update_preview_line(x1, y1, x2, y2)

    def stop_drag(self, event):
        """Fin du tracé, valider et fixer le câble."""
        if not self.current_start_point:
            return

        end_point = self.get_closest_end_point(event.x, event.y)
        if end_point:
            start_index = self.start_points.index(self.current_start_point)
            end_index = self.end_points.index(end_point)

            if self.cable_colors[start_index] != self.cable_colors[end_index]:
                sound_faux.play()
                self.cancel_drag()
                return

            self.finalize_cable(event.x, event.y, end_point)
            sound_juste.play()

            self.start_points.remove(self.current_start_point)
            self.end_points.remove(end_point)
            self.cable_colors.remove(self.current_color)
            self.lines_connected += 1

            view_point = self.end_to_view_mapping.get(end_point)
            if view_point:
                self.view_circles[view_point].configure(fg_color="green")

        self.cancel_drag()

        if self.lines_connected == len(self.start_circles):
            self.end_game()

    def update_preview_line(self, x1, y1, x2, y2):
        """Met à jour la ligne de prévisualisation pendant le drag."""
        if self.dragged_line:
            self.dragged_line.place_forget()

        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        self.dragged_line = ctk.CTkFrame(self.frame, width=length, height=2, fg_color=self.current_color)
        self.dragged_line.place(x=x1, y=y1, anchor="w")
        self.dragged_line.configure(transform=(angle,))

    def finalize_cable(self, x, y, end_point):
        """Finalise le tracé du câble."""
        x1, y1 = self.current_path[0]
        x2, y2 = end_point

        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        cable = ctk.CTkFrame(self.frame, width=length, height=2, fg_color=self.current_color)
        cable.place(x=x1, y=y1, anchor="w")
        cable.configure(transform=(angle,))

        self.current_path.append(end_point)

    def cancel_drag(self):
        """Annule le tracé en cours."""
        if self.dragged_line:
            self.dragged_line.place_forget()
        self.is_dragging = False
        self.current_path = []
        self.current_start_point = None

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
        ctk.CTkLabel(self.frame, text="Vous avez réussi !", font=("Arial", 20), fg_color="green").place(x=250, y=250)
        sound_victoire.play()
        self.root.after(2000, self.root.quit)

    def update_timer(self):
        """Met à jour le chronomètre du jeu."""
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time

        if remaining_time <= 0:
            self.root.title("Temps écoulé !")
            sound_defaite.play()
            self.root.after(2000, self.root.quit)
        else:
            self.root.title(f"Mini-jeu : Câblage - Temps restant : {int(remaining_time)}s")
            self.root.after(1000, self.update_timer)


# Lancer le jeu
if __name__ == "__main__":
    root = ctk.CTk()
    game = JeuDeCablage(root)
    root.mainloop()
