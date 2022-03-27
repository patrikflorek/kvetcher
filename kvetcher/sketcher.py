from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang.builder import Builder

Builder.load_file('kvetcher/sketcher.kv')

from kvetcher.draw import Overlay


class Sketcher(Scatter):
    translation_touches = BoundedNumericProperty(2, min=2)  # do not translate with only one finger
 
    overlays_container = ObjectProperty()

    _overlays_dict = {}

    def __init__(self, **kwargs):
        super(Sketcher, self).__init__(**kwargs)
        Clock.schedule_once(self._init_sketcher)  # wait until overlays_container is mounted

    def _init_sketcher(self, dt):
        self.data = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data_list):
        self._data = []
        self.overlays_container.clear_widgets()

        for overlay_data in data_list:
            overlay_name = overlay_data['name']
            if overlay_name in self._overlays_dict:
                overlay = self._overlays_dict[overlay_name]
            else:
                overlay = Overlay(name=overlay_name, 
                                  size=self.size)
                self._overlays_dict[overlay_name] = overlay

            overlay.opacity = overlay_data['opacity']
            if overlay_data['texture'] is None:
                overlay.texture = Texture.create(size=self.size)
            else:
                overlay.texture = overlay_data['texture']

            self._data.append({
                'name': overlay.name,
                'opacity': overlay.opacity,
                'texture': overlay.texture
            })
            self.overlays_container.add_widget(overlay)

            # Delete overlays not listed in data_list argument
            overlay_names = set([d['name'] for d in data_list])
            omitted_overlay_names = set(self._overlays_dict.keys()) - overlay_names
            for name in omitted_overlay_names:
                del self._overlays_dict[name]
