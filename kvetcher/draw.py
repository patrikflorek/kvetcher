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
    def __init__(self, **kwargs):
        super(OverlaysContainer, self).__init__(**kwargs)

        self._touches = []
        self._stroke_touch = None

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return False  # throw away if not originated in sketcher

        # Track all touches
        self._touches.append(touch)
        touch.grab(self)

        if 'multitouch_sim' in touch.profile:
            return False  # don't process multitouch simulation

        if len(self._touches) > 1:
            self._stroke_touch = None  # cancel the stroke if more than one touch
            return  False

        # Create stroke
        self._stroke_touch = touch
        touch.ud['stroke'] = [touch.pos]

        print('OverlaysContainer.on_touch_down() creates stroke:', touch)

        super(OverlaysContainer, self).on_touch_down(touch)

        return False  # parent (Sketcher instance) can take care of touch

    def on_touch_move(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return False  # no drawing allowed outside the area

        if touch != self._stroke_touch:
            return False  # no need to process if it's not stroke touch

        touch.ud['stroke'].append(touch.pos)

        print('OverlaysContainer.on_touch_move() tracks stroke:', touch)

        super(OverlaysContainer, self).on_touch_move(touch)  # children (Overlay instances) can take care of stroke touch

        return True  # stop parent to process stroke touch

    def on_touch_up(self, touch):
        # Stop tracking the touch
        if touch.grab_current == self:
            touch.ungrab(self)

        if touch in self._touches:
            self._touches.remove(touch)

        if touch != self._stroke_touch:
            return False  # no need to process if it's not stroke touch

        touch.ud['stroke'].append(touch.pos)

        self._stroke_touch = None

        print('OverlaysContainer.on_touch_up() releases stroke:', touch)

        if self.collide_point(touch.x, touch.y):
            super(OverlaysContainer, self).on_touch_up(touch)  # children can take care of stroke touch

        return False  # parent (Sketcher instance) can take care of touch
