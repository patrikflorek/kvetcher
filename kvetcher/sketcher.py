from kivy.uix.scatter import Scatter
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.lang.builder import Builder

from kvetcher.draw import Overlay


Builder.load_file('kvetcher/sketcher.kv')


class Sketcher(Scatter):
    translation_touches = BoundedNumericProperty(2, min=2)  # do not translate with only one finger
 
    overlays_container = ObjectProperty()

    def __init__(self, **kwargs):
        super(Sketcher, self).__init__(**kwargs)
