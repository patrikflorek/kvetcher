from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Fbo, Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty

from PIL import Image as PILImage


def copy_texture(texture, size=None):
    if size is None:
        size = texture.size

    fbo = Fbo(size=size)
    with fbo:
        Rectangle(size=size, texture=texture)
    fbo.draw()

    return fbo.texture


def texture_to_bitmap(texture):
    bitmap = PILImage.frombytes(mode='RGBA', size=texture.size, data=texture.pixels, decoder_name='raw')
    
    return bitmap


def bitmap_to_texture(bitmap):
    texture = Texture.create(bitmap.size, colorfmt='rgba')
    texture.blit_buffer(bitmap.tobytes(), colorfmt='rgba')
    
    return texture


class Overlay(Image):
    pen_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(Overlay, self).__init__(**kwargs)
        self.name = ''
        self.active = True
        self.texture = Texture.create(size=self.size, colorfmt='rgba')
        self.bitmap = texture_to_bitmap(self.texture)
        self.opacity = 1.0
        self.pen_texture = None
        self.pen_bitmap = None

    def on_texture(self, instance, texture):
        self.bitmap = texture_to_bitmap(texture)

    def on_pen_texture(self, instance, pen_texture):
        self.pen_bitmap = texture_to_bitmap(pen_texture)

    def on_touch_down(self, touch):
        return False  # do nothing; other touch events will take care of the stroke

    def _get_pen_crop_box(self, x, y):
        pen_width, pen_height = self.pen_bitmap.size

        pen_crop_box = [0, 0, pen_width - 1, pen_height - 1]
        if x < pen_width // 2:
            pen_crop_box[0] = pen_width // 2 - x
        if y < pen_height // 2:
            pen_crop_box[1] = pen_height // 2 - y
        if x > self.width - pen_width // 2:
            pen_crop_box[2] = self.width - x + pen_width // 2 - 1
        if y > self.height - pen_height // 2:
            pen_crop_box[3] = self.height - y + pen_height // 2 - 1

        return pen_crop_box

    def _get_overlay_paste_box(self, x, y):
        pen_width, pen_height = self.pen_bitmap.size

        overlay_paste_box = [0, 0, self.width - 1, self.height - 1]
        if x > pen_width // 2:
            overlay_paste_box[0] = x - pen_width // 2
        if y > pen_height // 2:
            overlay_paste_box[1] = y - pen_height // 2
        if x < self.width - pen_width // 2:
            overlay_paste_box[2] = x + pen_width // 2 - 1
        if y < self.height - pen_height // 2:
            overlay_paste_box[3] = y + pen_height // 2 - 1

        return overlay_paste_box

    def _pen_make_line(self, x, y, prev_x, prev_y):
        x_dist = abs(x - prev_x)
        y_dist = abs(y - prev_y)
        max_dist = max(x_dist, y_dist)
        dx = 0 if max_dist == 0 else (x - prev_x) / max_dist
        dy = 0 if max_dist == 0 else (y - prev_y) / max_dist

        for i in range(int(max_dist)):
            x_i = int(prev_x + i * dx)
            y_i = int(prev_y + i * dy)
            
            if not self.collide_point(x_i, y_i):
                continue
            
            pen_crop_box = self._get_pen_crop_box(x_i, y_i)
            pen_region = self.pen_bitmap.crop(pen_crop_box)

            overlay_paste_box = self._get_overlay_paste_box(x_i, y_i)
            self.bitmap.paste(pen_region, overlay_paste_box, pen_region)
        
        self.texture = bitmap_to_texture(self.bitmap)  # ineffective since on_texture creates a new bitmap copy

    def _pen_make_dot(self, x, y):
        pen_crop_box = self._get_pen_crop_box(x, y)
        pen_region = self.pen_bitmap.crop(pen_crop_box)

        overlay_paste_box = self._get_overlay_paste_box(x, y)
        self.bitmap.paste(pen_region, overlay_paste_box, pen_region)

        self. texture = bitmap_to_texture(self.bitmap)  # ineffective since on_texture creates a new bitmap copy

    def on_touch_move(self, touch):
        if not self.active  or self.pen_texture is None:
            return False

        x = int(touch.x)
        y = int(touch.y)
        prev_x = int(touch.ud['stroke'][-2][0])
        prev_y = int(touch.ud['stroke'][-2][1])

        self._pen_make_line(x, y, prev_x, prev_y)

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

        prev_x = touch.ud['stroke'][-2][0]
        prev_y = touch.ud['stroke'][-2][1]
        if (not self.collide_point(touch.x, touch.y)
                and not self.collide_point(prev_x, prev_y)):
            return False  # no drawing  except when previous touch was in the area

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
