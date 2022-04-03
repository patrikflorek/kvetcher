from kivy.graphics import Color, Ellipse, Fbo
from kivy.clock import Clock


class Pen():
    def __init__(self, color, size, **kwargs):
        super(Pen, self).__init__(**kwargs)
        self.texture = None
        self.color = color
        self.size = size  # size should be even to avoid artefacts during drawing
        Clock.schedule_once(lambda dt:self.update_texture(color=color, size=size), 0)
        
    def update_texture(self, color, size):
        self.color = color
        self.size =  size  # size should be even to avoid artefacts during drawing
        
        fbo = Fbo(size=(size, size))

        with fbo:
            Color(rgba=color)
            Ellipse(size=(size, size), pos=(0, 0))
        fbo.draw()

        self.texture = fbo.texture
