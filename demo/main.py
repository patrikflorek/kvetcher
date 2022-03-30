import os, sys

sys.path.append(os.path.abspath('../kvetcher'))


from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivy.clock import Clock

from pen import Pen


class SketcherDemoAppRoot(Screen):
    sketcher = ObjectProperty()

    def __init__(self, **kwargs):
        super(SketcherDemoAppRoot, self).__init__(**kwargs)
        Clock.schedule_once(self._initialize_sketcher)  # wait until the component is built

    def _initialize_sketcher(self, dt):
        self.sketcher.size = 320, 640  # overwrites definition from kv file

        self.pen_texture = Pen(color=(1, 0, 0, 1), size=20).texture

        self.sketcher.data = [
            {
                'name': 'Corals',
                'active': True,
                'texture': CoreImage('assets/img/corals_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture
            },
            {
                'name': 'Octopus',
                'active': False,
                'texture': CoreImage('assets/img/octopus_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture
            },
            {
                'name': 'Ice cream',
                'active': False,
                'texture': CoreImage('assets/img/icecream_320x640.png').texture,
                'opacity': 1.0,
                'pen_texture': self.pen_texture
            }
        ]

        # Clock.schedule_once(self._update_sketcher, 5)

    def _update_sketcher(self, dt):
        self.sketcher.data = [
            {
                'name': 'Octopus',
                'active': False,
                'texture': CoreImage('assets/img/octopus_320x640.png').texture,
                'opacity': 0.6,
                'pen_texture': self.pen.texture
            },
            {
                'name': 'Ice cream',
                'active': False,
                'texture': CoreImage('assets/img/icecream_320x640.png').texture,
                'opacity': 0.6,
                'pen_texture': self.pen.texture
            },
            {
                'name': 'Corals',
                'active': True,
                'texture': CoreImage('assets/img/corals_320x640.png').texture,
                'opacity': 0.6,
                'pen_texture': self.pen.texture
            }
        ]


class SketcherDemoApp(App):
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


if __name__ == '__main__':
    app = SketcherDemoApp()
    app.run()
