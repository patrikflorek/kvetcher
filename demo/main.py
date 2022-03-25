import os, sys

sys.path.append(os.path.abspath('../kvetcher'))


from kivy.app import App
from kivy.uix.screenmanager import Screen


class SketcherDemoAppRoot(Screen):
    pass


class SketcherDemoApp(App):
    def build(self):
        return SketcherDemoAppRoot()


if __name__ == '__main__':
    app = SketcherDemoApp()
    app.run()
