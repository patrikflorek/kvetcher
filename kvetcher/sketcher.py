from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.properties import BoundedNumericProperty, ObjectProperty
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
            overlay_id = overlay_data['id']
            if overlay_id in self._overlays_dict:
                overlay = self._overlays_dict[overlay_id]
            else:
                overlay = Overlay(id=overlay_id, 
                                  size=self.size)
                self._overlays_dict[overlay_id] = overlay

            overlay.name = overlay_data['name']
            
            if 'active' in overlay_data:
                overlay.active = overlay_data['active']

            if ('texture' in overlay_data 
                and overlay_data['texture'] is not None):
                overlay.texture = overlay_data['texture']
            else:
                overlay.texture = Texture.create(size=self.size)
            
            if 'opacity' in overlay_data:    
                overlay.opacity = overlay_data['opacity']
            
            if 'pen_texture' in overlay_data:
                overlay.pen_texture = overlay_data['pen_texture']

            self._data.append({
                'id': overlay.id,
                'name': overlay.name,
                'active': overlay.active,
                'texture': overlay.texture,
                'opacity': overlay.opacity,
                'pen_texture': overlay.pen_texture
            })

            self.overlays_container.add_widget(overlay)

            # Delete overlays not listed in data_list argument
            given_ids = set([d['id'] for d in data_list])
            omitted_overlays_ids = set(self._overlays_dict.keys()) - given_ids
            for id in omitted_overlays_ids:
                del self._overlays_dict[id]
