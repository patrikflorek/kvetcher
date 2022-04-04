from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Fbo, Rectangle
from kivy.graphics.texture import Texture


def copy_texture(texture):
    fbo = Fbo(size=texture.size)
    with fbo:
        Rectangle(size=fbo.size, texture=texture)
    fbo.draw()

    return fbo.texture


class Overlay(Image):
    def __init__(self, **kwargs):
        super(Overlay, self).__init__(**kwargs)
        self.name = ''
        self.active = True
        self.texture = Texture.create(size=self.size, colorfmt='rgba')
        self.opacity = 1.0
        self.pen_texture = None

    def on_touch_down(self, touch):
        return False  # do nothing; other touch events will take care of the stroke

    def on_touch_move(self, touch):
        if not self.active  or self.pen_texture is None:
            return False

        prev_x, prev_y = touch.ud['stroke'][-2]
        x_dist = abs(touch.x - prev_x)
        y_dist = abs(touch.y - prev_y)
        max_dist = max(x_dist, y_dist)
        dx = 0 if max_dist == 0 else (touch.x - prev_x) / max_dist
        dy = 0 if max_dist == 0 else (touch.y - prev_y) / max_dist

        fbo = Fbo(size=self.size)
        with fbo:
            Rectangle(size=self.size, pos=self.pos, texture=self.texture)  # original overlay's texture
            pen_size = self.pen_texture.size

            for i in range(int(max_dist)):
                x = int(prev_x + i * dx)
                y = int(prev_y + i * dy)
                Rectangle(size=pen_size, 
                        pos=(x - pen_size[0] / 2, y - pen_size[1] / 2),
                        texture=self.pen_texture)
        fbo.draw()
        self.texture = fbo.texture

        return False

    def on_touch_up(self, touch):
        if not self.active or self.pen_texture is None:
            return False

        if len(touch.ud['stroke']) == 2:
            # no movement between touch_down and touch_up
            fbo = Fbo(size=self.size)
            with fbo:
                Rectangle(size=self.size, pos=self.pos, texture=self.texture)  # original overlay's texture
                pen_size = self.pen_texture.size

                Rectangle(size=pen_size, 
                          pos=(touch.x - pen_size[0] / 2, touch.y - pen_size[1] / 2),
                          texture=self.pen_texture)
            fbo.draw()
            self.texture = fbo.texture

        return False


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

        super(OverlaysContainer, self).on_touch_down(touch)

        return False  # parent (Sketcher instance) can take care of touch

    def on_touch_move(self, touch):
        if touch != self._stroke_touch:
            return False  # no need to process if it's not stroke touch

        touch.ud['stroke'].append(touch.pos)  # keep touch position for overlays to use it later 

        if not self.collide_point(touch.x, touch.y):
            return False  # no drawing allowed outside the area

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

        if self.collide_point(touch.x, touch.y):
            super(OverlaysContainer, self).on_touch_up(touch)  # children can take care of stroke touch

        return False  # parent (Sketcher instance) can take care of touch
