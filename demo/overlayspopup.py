from id_generator import get_new_id

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder

Builder.load_file('overlayspopup.kv')


class OverlayItem(BoxLayout):
    def __init__(self, data, **kwargs):
        super(OverlayItem, self).__init__(**kwargs)
        self.data = data

    def delete(self):
        self.data.clear()
        self.parent.remove_widget(self)


class OverlaysPopup(Popup):
    overlay_items_container = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverlaysPopup, self).__init__(**kwargs)
        self.overlays_data_list = []
        self.new_overlays_data_list = []
        self.pen_texture = None

    def on_open(self):
        self.new_overlays_data_list = []
        self.overlay_items_container.clear_widgets()

        for overlay_data in self.overlays_data_list:
            new_overlay_data = overlay_data.copy()
            self.new_overlays_data_list.append(new_overlay_data)
            overlay_item = OverlayItem(new_overlay_data)
            self.overlay_items_container.add_widget(overlay_item)

    def add_new(self):
        new_overlay_data = {
            'id': get_new_id(),
            'name': '',
            'active': True,
            'opacity': 1.0,
            'pen_texture': self.pen_texture
        }
        self.new_overlays_data_list.append(new_overlay_data)
        overlay_item = OverlayItem(new_overlay_data)
        self.overlay_items_container.add_widget(overlay_item)
