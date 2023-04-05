from pygame import sprite, freetype, Surface, draw, gfxdraw, SRCALPHA


class Volume(sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        sprite.Sprite.__init__(self)
        self.image = Surface((21, 140), SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.rect.w // 2
        self.x, self.y = self.radius, self.rect.h - self.radius
        self.color_circle = (255, 255, 255, 255)
        self.color_rect = (0, 185, 218, 128)
        self.color_text = (0, 0, 220, 255)
        self.alpha = 255
        self.volume = 0
        self.font = freetype.SysFont('arial', 16, True)

    def update(self):
        self.image.set_alpha(self.alpha)
        draw.rect(self.image, self.color_rect, [0, 0, *self.rect[2:]], border_radius=self.radius)
        gfxdraw.aacircle(self.image, self.x, self.y, self.radius, self.color_circle)
        gfxdraw.filled_circle(self.image, self.x, self.y, self.radius, self.color_circle)
        text = str(round(self.volume * 100))
        text_rect = self.font.get_rect(text, size=11)
        self.font.render_to(
            self.image, (self.x - text_rect[2] / 2., self.y - text_rect[3] / 2.), text,
            self.color_text, rotation=0, size=11)

    def render(self, e_buttons, e_pos, soundH, soundT1, soundT2):
        if self.rect.left < e_pos[0] < self.rect.right and \
                self.rect.top < e_pos[1] < self.rect.bottom and \
                e_buttons:
            self.y = abs(self.rect.top - e_pos[1])
            if self.y > self.rect.h - self.radius:
                self.y = self.rect.h - self.radius
            elif self.y < self.radius:
                self.y = self.radius
            self.volume = (100 - (self.y - self.radius) / 1.2) / 100.
            return soundH.set_volume(self.volume / 2.), soundT1.set_volume(self.volume), \
                soundT2.set_volume(self.volume)


"""
from sound_adjustment import Volume

vol = Volume(20, HEIGHT_WIN - 80)
menu_box.add(vol)

if ev.pos[0] < vol.rect.right and ev.pos[1] > vol.rect.top:
    if ev.type == pg.MOUSEMOTION:
        vol.render(e.buttons[0], ev.pos, soundH, soundT1, soundT2)
"""
