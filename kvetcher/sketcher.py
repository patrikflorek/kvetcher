from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.lang.builder import Builder

Builder.load_file('kvetcher/sketcher.kv')

from kvetcher.draw import Overlay
from kvetcher.draw import copy_texture


class Sketcher(Scatter):
    translation_touches = BoundedNumericProperty(2, min=2)  # do not translate with only one finger
 
    overlays_container = ObjectProperty()

    # data = []

    _overlays_dict = {}

    def __init__(self, **kwargs):
        super(Sketcher, self).__init__(**kwargs)

    @property
    def data(self):
        exported_overlays_data = []
        for overlay in self.overlays_container.children[::-1]:
            overlay_data = {
                'id': overlay.id,
                'name': overlay.name,
                'active': overlay.active,
                'texture': copy_texture(overlay.texture),
                'opacity': overlay.opacity,
                'pen_texture': copy_texture(overlay.pen_texture),
                'pen_mode': overlay.pen_mode
            } 

            exported_overlays_data.append(overlay_data)

        return exported_overlays_data

    @data.setter
    def data(self, data_list):
        self.overlays_container.clear_widgets()

        for overlay_data in data_list:
            overlay_id = overlay_data['id']  # required

            if overlay_id in self._overlays_dict:
                overlay = self._overlays_dict[overlay_id]
            else:
                overlay = Overlay(size=self.size)
                self._overlays_dict[overlay_id] = overlay
            overlay.id = overlay_id

            if 'name' in overlay_data:
                overlay.name = overlay_data['name']
            else:
                overlay.name = ''

            if 'active'in overlay_data:
                overlay.active = overlay_data['active']
            else:
                overlay.active = True

            if 'texture' in overlay_data and overlay_data['texture'] is not None:
                overlay.texture = copy_texture(overlay_data['texture'], self.size)
            else:
                overlay.texture = Texture.create(size=self.size, colorfmt='rgba')

            if 'opacity' in overlay_data:
                overlay.opacity = overlay_data['opacity']
            else:
                overlay.opacity = 1.0

            if 'pen_texture' in overlay_data:
                overlay.pen_texture = copy_texture(overlay_data['pen_texture'])
            else:
                overlay.pen_texture = None

            if 'pen_mode' in overlay_data:
                overlay.pen_mode = overlay_data['pen_mode']
            else:
                overlay.pen_mode = 'pen'

            self.overlays_container.add_widget(overlay)

        # Delete overlays not listed in data_list argument
        given_ids = set([d['id'] for d in data_list])
        omitted_overlays_ids = set(self._overlays_dict.keys()) - given_ids
        for id in omitted_overlays_ids:
            del self._overlays_dict[id]
