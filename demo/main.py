import os, sys

sys.path.append(os.path.abspath('../kvetcher'))


from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

class SketcherDemoAppRoot(Screen):
    sketcher = ObjectProperty()

    def __init__(self, **kwargs):
        super(SketcherDemoAppRoot, self).__init__(**kwargs)
        Clock.schedule_once(self._initialize_sketcher)  # wait until the component is built

    def _initialize_sketcher(self, dt):
        self.sketcher.size = 320, 640  # overwrites definition from kv file

        self.sketcher.data = [
            {
                'name': 'Corals',
                'texture': CoreImage('assets/img/corals_320x640.png').texture,
                'active': True,
                'opacity': 1.0
            },
            {
                'name': 'Octopus',
                'texture': CoreImage('assets/img/octopus_320x640.png').texture,
                'active': False,
                'opacity': 1.0
            },
            {
                'name': 'Ice cream',
                'texture': CoreImage('assets/img/icecream_320x640.png').texture,
                'active': False,
                'opacity': 1.0
            }
        ]

        Clock.schedule_once(self._update_sketcher, 5)

    def _update_sketcher(self, dt):
        self.sketcher.data = [
            {
                'name': 'Octopus',
                'texture': CoreImage('assets/img/octopus_320x640.png').texture,
                'active': False,
                'opacity': 0.6
            },
            {
                'name': 'Ice cream',
                'texture': CoreImage('assets/img/icecream_320x640.png').texture,
                'active': False,
                'opacity': 0.6
            },
            {
                'name': 'Corals',
                'texture': CoreImage('assets/img/corals_320x640.png').texture,
                'active': True,
                'opacity': 0.6
            }
        ]


class SketcherDemoApp(App):
    def build(self):
        app_root = SketcherDemoAppRoot()
        self.sketcher = app_root.sketcher
        return app_root


if __name__ == '__main__':
    app = SketcherDemoApp()
    app.run()
