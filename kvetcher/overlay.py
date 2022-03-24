from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture


class Overlay(Image):
    def __init__(self, name, active, opacity, texture, pen, **kwargs):
        super(Overlay, self).__init__(**kwargs)
        self.name = name
        self.active = active
        self.opacity = opacity
        self.texture = texture if texture is not None else Texture.create(size=self.size)


class OverlaysContainer(RelativeLayout):
    pass