from kivy.graphics import Color, Ellipse, Fbo

class Pen():
    def __init__(self, color, size, **kwargs):
        super(Pen, self).__init__(**kwargs)
        self.size = (size, size)
        self.color = color

        fbo = Fbo(size=self.size)
        with fbo:
            Color(rgba=color)
            Ellipse(size=self.size, pos=(0, 0))
        fbo.draw()

        self.texture = fbo.texture
