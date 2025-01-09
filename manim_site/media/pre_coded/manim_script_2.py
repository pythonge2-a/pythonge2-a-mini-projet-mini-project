from manim import *


class output(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(BLUE, opacity=0.5)  # set the color and transparency
        circle.set_stroke(BLUE, width=10)
        self.play(Create(circle))  # show the circle on screen