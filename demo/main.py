import os, sys

sys.path.append(os.path.abspath('../kvetcher'))

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

from pen import Pen
from demo.overlayspopup import OverlaysPopup
from demo.penpopup import PenPopup


from id_generator import get_new_id


class PenModeDropDown(DropDown):
    pass


class SketcherDemoAppRoot(Screen):
    pen_mode_dropdown_main_button = ObjectProperty()

    sketcher_container = ObjectProperty()
    sketcher = ObjectProperty()

    def __init__(self, **kwargs):
        super(SketcherDemoAppRoot, self).__init__(**kwargs)

        Clock.schedule_once(self._initialize_sketcher)  # wait until the component is built

    def _initialize_sketcher(self, dt):
        self.sketcher.size = 300, 600  # overwrites size from kv file

        self.pen_texture = app.pen.texture

        self.sketcher.data = [
            {
                'id': get_new_id(),
                'name': 'Corals',
                'active': True,
                'texture': CoreImage('assets/img/corals_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture,
                'pen_mode': 'pen'
            },
            {
                'id': get_new_id(),
                'name': 'Octopus',
                'active': False,
                'texture': CoreImage('assets/img/octopus_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture,
                'pen_mode': 'pen'
            },
            {
                'id': get_new_id(),
                'name': 'Ice cream',
                'active': False,
                'texture': CoreImage('assets/img/icecream_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture,
                'pen_mode': 'pen'
            }
        ]

    def _set_pen_mode(self, instance, mode):
        self.pen_mode_dropdown_main_button.text = mode.capitalize()
        app.set_pen_mode(mode)

    def open_pen_mode_dropdown(self, instance):
        dropdown = PenModeDropDown()
        dropdown.container.padding = [0, '10dp']
        dropdown.bind(on_select=self._set_pen_mode)
        dropdown.open(instance)


class SketcherDemoApp(App):
    def __init__(self, **kwargs):
        super(SketcherDemoApp, self).__init__(**kwargs)
        self.overlays_popup = OverlaysPopup()
        self.pen = Pen(color=(0, 1, 1, 1), size=20)
        self.pen_popup = PenPopup()

    def build(self):
        app_root = SketcherDemoAppRoot()
        self.sketcher = app_root.sketcher
        self.sketcher_container = app_root.sketcher_container

        return app_root

    def reset_transformations(self):
        self.sketcher.apply_transform(self.sketcher.transform_inv)
        self.sketcher.center = self.sketcher_container.center

    def clear_overlays(self):
        new_sketcher_data = self.sketcher.data
        for overlay_data in new_sketcher_data:
            overlay_data['texture'] = None
        self.sketcher.data = new_sketcher_data

    def open_overlays_popup(self):
        self.overlays_popup.overlays_data_list = self.sketcher.data
        self.overlays_popup.pen_texture = self.pen.texture  # to add new overlay
        self.overlays_popup.open()

    def update_overlays_data(self, data):
        self.sketcher.data = [d for d in data if d]  # omit deleted overlays
        self.overlays_popup.dismiss()

    def set_pen_mode(self, mode):
        new_sketcher_data = self.sketcher.data
        for overlay_data in new_sketcher_data:
            overlay_data['pen_mode'] = mode
        self.sketcher.data = new_sketcher_data

    def open_pen_popup(self):
        self.pen_popup.pen_color = self.pen.color
        self.pen_popup.pen_size = self.pen.size
        self.pen_popup.open()

    def update_pen(self, color, size):
        self.pen.update_texture(color, size)
        new_sketcher_data = self.sketcher.data
        for overlay_data in new_sketcher_data:
            overlay_data['pen_texture'] = self.pen.texture
        self.sketcher.data = new_sketcher_data
        self.pen_popup.dismiss()


if __name__ == '__main__':
    app = SketcherDemoApp()
    app.run()
