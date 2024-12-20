import customtkinter as ctk
import math

class Dynamo:
    def __init__(self, power_output):
        self.power_output = power_output

    def generate_power(self):
        return self.power_output

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dynamo Test")
        self.geometry("400x400")

        self.dynamo = Dynamo(0)

        self.label = ctk.CTkLabel(self, text=f"Dynamo Power Output: {self.dynamo.generate_power()}")
        self.label.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self, width=400, height=400)
        self.canvas.pack()

        self.outer_circle_radius = 150
        self.inner_circle_radius = 20
        self.angle = 0
        self.speed = 0  # Variable pour contrôler la vitesse

        self.outer_circle = self.canvas.create_oval(100, 100, 300, 300, outline="black")
        self.line = self.canvas.create_line(200, 200, 200, 200, fill="blue", width=5)
        self.inner_circle = self.canvas.create_oval(250, 180, 290, 220, fill="red")

        self.canvas.bind("<Button-1>", self.on_outer_circle_click)

        self.update_animation()

    def on_outer_circle_click(self, event):
        if self.is_inside_circle(event.x, event.y, 200, 200, self.outer_circle_radius):
            self.angle += 10

    def is_inside_circle(self, x, y, circle_x, circle_y, radius):
        return (x - circle_x) ** 2 + (y - circle_y) ** 2 <= radius ** 2

    def update_animation(self):
        self.angle += self.speed  # Utilisation de la variable de vitesse
        if self.angle >= 360:
            self.angle = 0
            self.dynamo.power_output += 1
            self.label.configure(text=f"Dynamo Power Output: {self.dynamo.generate_power()}")

        x = 200 + self.outer_circle_radius * math.cos(math.radians(self.angle))
        y = 200 + self.outer_circle_radius * math.sin(math.radians(self.angle))

        self.canvas.coords(self.inner_circle, x - self.inner_circle_radius, y - self.inner_circle_radius, x + self.inner_circle_radius, y + self.inner_circle_radius)
        self.canvas.coords(self.line, 200, 200, x, y)

        self.after(50, self.update_animation)

if __name__ == "__main__":
    app = App()
    app.mainloop()