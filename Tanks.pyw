import pygame as pg
import pygame.freetype as pgm
import random
import os
from sound_adjustment import Volume

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
SIZE_WINDOW = WIDTH_WIN, HEIGHT_WIN = 960, 720
BACKGROUND_COLOR = (13, 10, 253)

FPS = 60
clock = pg.time.Clock()

vec = pg.math.Vector2
STARS_SIZE = 16
STARS_MAX = 100
HEIGHT_EARTH = 250
mainpath = os.path.dirname(__file__)

count = {'life': 5.9, 'killed': 0}
soundH_stop = [True]
run = [False, True]
speed = 8
salvo = 0
salvoT = False
salvoT2 = False
expT = False
expT1 = False
expH = False
expH1 = False
counting = False
speedT = 0
speedH = random.randint(-1, 1)
projectile_velocity = 24
time_fire = 0
tank1_pos = 196
h_max_scale = 0.6

"Звук"
soundH = pg.mixer.Sound(os.path.join(mainpath, 'Sound', 'H.wav'))
soundT1 = pg.mixer.Sound(os.path.join(mainpath, 'Sound', 'T1.wav'))
soundT2 = pg.mixer.Sound(os.path.join(mainpath, 'Sound', 'T2.wav'))
soundH.set_volume(0), soundT1.set_volume(0), soundT2.set_volume(0)

"Шрифт"
font_menu = pgm.SysFont('Arial', 96, True, True)
font_rect = font_menu.get_rect('PAUSE')
font_rect1 = font_menu.get_rect('GAME OVER')
font_rect2 = font_menu.get_rect('TANKS')
font_menu2 = pg.font.SysFont('Arial', 24, True, True)

"Пункты меню"
points = [[330, 250, 'GAME', (250, 250, 30), (250, 30, 250), 0],
          [350, 350, 'QUIT', (250, 250, 30), (250, 30, 250), 1]]

pg.display.set_caption('Tanks8')
screen = pg.display.set_mode(SIZE_WINDOW)  # , pg.SCALED | pg.FULLSCREEN)
font_rect.center = screen.get_rect().center


class Health(pg.sprite.Sprite):
    def __init__(self, images):
        self._layer = 2
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.images = images
        self.index = 5
        self.image = images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().centerx, self.image.get_height() // 2 + 1

        self.font = pgm.SysFont('Consolas', 24)
        self.pos1, self.pos2 = (10, 4), (WIDTH_WIN - 100, 4)
        self.color = pg.Color('white')

    def update(self):
        self.index = int(count['life'])
        self.image = self.images[self.index]

        self.font.render_to(screen, self.pos1, f"Points: {count['killed']}", fgcolor=self.color)
        self.font.render_to(screen, self.pos2, f"Life: {int(count['life'])}", fgcolor=self.color)


class Earth(pg.sprite.Sprite):
    def __init__(self, x, y, images):
        self._layer = 2
        pg.sprite.Sprite.__init__(self, all_sprites, earthGroup)
        self.images = images
        self.index = 0  # первый кадр
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= speed
        if self.rect.x <= -WIDTH_WIN:
            self.rect.x = WIDTH_WIN
            self.index = random.randrange(self.range)
            self.image = self.images[self.index]
            self.mask = pg.mask.from_surface(self.image)


class Stars(pg.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 0
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.speed = random.randint(1, 3)
        self.STARS_SIZE = random.randint(8, 16)
        self.img = pg.image.load(os.path.join(mainpath, 'Image', 'star16.png'))
        self.image = pg.transform.scale(self.img, (self.STARS_SIZE, self.STARS_SIZE))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH_WIN


class SpriteAnimation(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        self._layer = 4
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.angle = angle
        self.scale = scale
        self.images = [pg.transform.flip(im, dx, dy) for im in images]

        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.position = vec(x, y)
        self.velocity = vec()
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        images = [pg.transform.rotozoom(img, -self.angle, self.scale) for img in self.images]
        self.index += 0.2
        self.image = images[int(self.index % self.range)]

        self.position += self.velocity
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pg.mask.from_surface(self.image)


class Sprite(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        self._layer = 3
        pg.sprite.Sprite.__init__(self, all_sprites)
        self.angle = angle
        self.scale = scale
        self.images = pg.transform.flip(images[0], dx, dy)
        self.image = self.images

        self.rect = self.image.get_rect()
        self.velocity = vec().rotate(angle)
        self.position = vec(x, y)

    def update(self):
        self.image = pg.transform.rotozoom(self.images, -self.angle, self.scale)
        self.position += self.velocity
        self.rect = self.image.get_rect(center=self.position)


class Burn(pg.sprite.Sprite):
    def __init__(self, images, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = images
        self.frame = 0
        self.range = len(self.images)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=(x, y - self.image.get_height() / 3.))

    def update(self):
        self.frame += 0.2
        self.image = self.images[int(self.frame % self.range)]


def load_images(path):
    images = []
    for file_name in sorted(os.listdir(os.path.join(path))):
        image = pg.image.load(os.path.join(path, file_name))
        images.append(image)
    # print(path, images)
    return images


def menu():
    menu_box = pg.sprite.Group(bullet, helicopter, barrel, tank1, mouseMenu, vol)
    pg.mouse.set_visible(True)

    background_color_primary = (2, 117, 216)
    point = 0
    col = 250
    text_color = (col, col, col)
    col_block = 0
    fire_block = 1 if int(count['life']) <= 0 else 0
    tx = WIDTH_WIN
    if fire_block == 1:
        tx_min = -font_rect1.w
        menu_box.add(burn)
    else:
        tx_min = -font_rect2.w

    tank1.position.x, tank1.position.y = 150, 450
    tank1.velocity.x, tank1.velocity.y = 0, 0
    helicopter.velocity.x, helicopter.velocity.y = 0, 0
    helicopter.scale = h_max_scale
    helicopter.position.x, helicopter.position.y = 750, 150
    barrel.position = tank1.position + (25, -15)
    barrel_x = barrel.position.x + images2[0].get_width() / 1.2
    barrel_y = barrel.position.y - images2[0].get_height() / 1.2
    fire.position.x, fire.position.y = barrel_x, barrel_y
    barrel.angle = fire.angle = -10
    helicopter.angle = bullet.angle = 180
    bullet.position.x = -WIDTH_WIN
    time_fire = 0
    soundH.stop()

    record_file = os.path.join(mainpath, 'Record', 'record.dat')
    with open(record_file, 'a+') as d:
        d.seek(0)
        record = d.read()
        if record == '':
            record = '0'
        else:
            if int(record) < count['killed']:
                record = str(count['killed'])
        d.truncate(0)
        d.write(record)

    text1 = font_menu2.render("shoot enemies, score points", True, text_color)
    text1_pos = (600, 20)
    text2 = font_menu2.render(f"Scored points: {count['killed']}", True, text_color)
    text2_pos = (20, 20)
    text3 = font_menu2.render(f"Available lives: {int(count['life'])}", True, text_color)
    text3_pos = (20, 80)
    text4 = font_menu2.render("shot of the tank -", True, text_color)
    text4_pos = (690, 425)
    text5 = font_menu2.render("left mouse button or space", True, text_color)
    text5_pos = (630, 455)
    text6 = font_menu2.render('"m" key - menu', True, text_color)
    text6_pos = (70, 300)
    text7 = font_menu2.render(f'Current record: {record}', True, text_color)
    text7_pos = (20, 50)

    while run[1]:
        m_pos = pg.mouse.get_pos()
        for b in points:
            if b[0] < m_pos[0] < b[0] + font_rect.w and b[1] < m_pos[1] < b[1] + font_rect.h:
                point = b[5]

        # Выстрелы
        bullet.velocity.x, bullet.velocity.y = -speed * 2, 0
        if bullet.position.x < 0:
            bullet.position.x = helicopter.position.x - h_width * helicopter.scale / 2.0
            bullet.position.y = helicopter.position.y + h_height * helicopter.scale / 2.5

        if fire_block == 0:
            if fire.position.x == barrel_x:
                time_fire += 1
                if time_fire == 20:
                    menu_box.add(fire)
                    fire.velocity = vec(speed // 2, 0).rotate(fire.angle)
            if fire.position.x >= WIDTH_WIN / 3.:
                fire.position.x = barrel_x
                fire.position.y = barrel_y
                fire.kill()
                time_fire = 0

        # Бегущий текст
        tx -= 2
        if tx == tx_min:
            tx = WIDTH_WIN
        if col_block == 0:
            col -= 1
            if col == 0:
                col_block = 1
        if col_block == 1:
            col += 1
            if col == 250:
                col_block = 0

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                menu_box.empty()
                end()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    menu_box.empty()
                    end()
                elif ev.key == pg.K_UP:
                    if point == 1:
                        point = 0
                elif ev.key == pg.K_DOWN:
                    if point == 0:
                        point = 1
                elif ev.key == pg.K_RETURN:
                    if point == 0:
                        menu_box.empty()
                        start()
                        pg.mouse.set_visible(False)
                        run.reverse()
                        if fire_block == 1:
                            count['life'], count['killed'] = 5.9, 0
                    elif point == 1:
                        menu_box.empty()
                        end()
            elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1 \
                    and font_rect.left < m_pos[0] < font_rect.right:
                if point == 0:
                    menu_box.empty()
                    start()
                    pg.mouse.set_visible(False)
                    run.reverse()
                    if fire_block == 1:
                        count['life'], count['killed'] = 5.9, 0
                elif point == 1:
                    menu_box.empty()
                    end()
            elif m_pos[0] < vol.rect.right and m_pos[1] > vol.rect.top:
                if ev.type == pg.MOUSEMOTION:
                    vol.render(ev.buttons[0], m_pos, soundH, soundT1, soundT2)

        screen.fill(background_color_primary)
        for a in points:
            if point == a[5]:
                font_menu.render_to(screen, (a[0], a[1]), a[2], a[4])
            else:
                font_menu.render_to(screen, (a[0], a[1]), a[2], a[3])
        if fire_block == 1:
            font_menu.render_to(screen, (tx, 600), 'GAME OVER', (col, 250, 250))
        else:
            font_menu.render_to(screen, (tx, 600), 'TANKS', (col, 250, 250))
        screen.blit(text1, text1_pos)
        screen.blit(text2, text2_pos)
        screen.blit(text3, text3_pos)
        screen.blit(text4, text4_pos)
        screen.blit(text5, text5_pos)
        screen.blit(text6, text6_pos)
        screen.blit(text7, text7_pos)
        screen.blit(vol_img, vol_img_rect)

        menu_box.update()
        menu_box.draw(screen)
        display_update()


def initialize_stars(stars_max):
    for _ in range(stars_max):
        Stars(random.randint(0, WIDTH_WIN), random.randint(0, HEIGHT_WIN - HEIGHT_EARTH))


def gravitation():
    tank1.velocity.y += 1
    if pg.sprite.spritecollideany(tank1, earthGroup, pg.sprite.collide_mask):
        tank1.position.y -= 1
        tank1.velocity.y = 0
        tank1.rect.centery = tank1.position.y

    if tank2.position.x > WIDTH_WIN + tank2_width or tank2.position.x < 0 - tank2_width:
        tank2.position.y = tank_position_y
        tank2.velocity.y = 0
    else:
        tank2.velocity.y += 1
        if pg.sprite.spritecollideany(tank2, earthGroup, pg.sprite.collide_mask):
            tank2.position.y -= 1
            tank2.velocity.y = 0
            tank2.rect.centery = tank2.position.y


def start():
    bullet.position.x = WIDTH_WIN * 2
    bullet.velocity.x, bullet.velocity.y = 0, 0
    tank1.position.x = -WIDTH_WIN // 2
    tank2.position.x = WIDTH_WIN * random.randint(2, 3)
    helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
    helicopter.position.y = random.randint(-200, HEIGHT_WIN - HEIGHT_EARTH * 1.5)
    barrel.position = tank1.position + (25, -15)
    barrel2.position = tank2.position + (-21, -15)
    barrel2.angle = random.randint(1, 5)
    helicopter.scale = h_max_scale / 2.
    fire.velocity.x, fire.velocity.y = 0, 0
    fire.position = barrel.position
    fire2.velocity.x, fire2.velocity.y = 0, 0
    fire2.position.x = WIDTH_WIN * 2
    shell2.velocity.x, shell2.velocity.y = 0, 0
    shell2.position.x = WIDTH_WIN * 2
    shell.velocity.x, shell.velocity.y = 0, 0
    shell.position = barrel.position
    explosion.kill(), explosion2.kill()
    soundH_stop[0] = True
    soundH.stop()


def icon():
    size, text = 32, '\u0056\u004F'
    sur = pg.Surface((size, size), pg.SRCALPHA)
    pg.draw.circle(sur, '#44475a59', (size // 2, size // 2), size // 2)
    rect_text = health.font.get_rect(text)
    rect_text.center = sur.get_rect().center
    health.font.render_to(sur, rect_text, text, fgcolor='#ff0000')
    pg.display.set_icon(sur)


def display_update():
    pg.display.set_caption(f'Tanks8   FPS: {int(clock.get_fps())}')
    pg.display.update()
    clock.tick(FPS)


def end():
    all_sprites.empty()
    run[0], run[1] = False, False


"____________________________________________________Main_______________________________________________________"

all_sprites = pg.sprite.LayeredUpdates()
earthGroup = pg.sprite.Group()

images0 = load_images(os.path.join(mainpath, 'Image', 'Earth'))
earth = Earth(x=0, y=HEIGHT_WIN - images0[0].get_height(), images=images0)
earth_clone = Earth(x=WIDTH_WIN, y=HEIGHT_WIN - images0[0].get_height(), images=images0)

images1 = load_images(os.path.join(mainpath, 'Image', 'Tank1'))
tank1 = SpriteAnimation(x=150, y=450, dx=False, dy=False, images=images1, angle=0, scale=1.7)

images2 = load_images(os.path.join(mainpath, 'Image', 'Barrel1'))
barrel = Sprite(x=tank1.position.x, y=tank1.position.y, dx=False, dy=False, images=images2, angle=-10, scale=1.2)

images3 = load_images(os.path.join(mainpath, 'Image', 'Helicopter'))
helicopter = SpriteAnimation(x=750, y=150, dx=False, dy=True, images=images3, angle=180, scale=h_max_scale / 2.)
h_width, h_height = helicopter.rect.w, helicopter.rect.h

images4 = load_images(os.path.join(mainpath, 'Image', 'Tank2'))
tank2 = SpriteAnimation(x=WIDTH_WIN * 2, y=0, dx=False, dy=False, images=images4, angle=0, scale=1.7)
tank2.position.y = tank_position_y = earth.rect.top - tank2.rect.h * tank2.scale // 2
tank2_width = tank2.rect.w

images5 = load_images(os.path.join(mainpath, 'Image', 'Barrel2'))
barrel2 = Sprite(x=tank2.position.x, y=tank2.position.y, dx=False, dy=False, images=images5, angle=5, scale=1.2)
barrel2_size = barrel2.rect.w * barrel2.scale / 2.0, barrel2.rect.h * barrel2.scale / 4.0

images6 = load_images(os.path.join(mainpath, 'Image', 'Sight'))
sight = Sprite(x=0, y=0, dx=False, dy=False, images=images6, angle=False, scale=0.5)

images7 = load_images(os.path.join(mainpath, 'Image', 'Shell'))
shell = Sprite(x=-100, y=0, dx=False, dy=False, images=images7, angle=0, scale=0.4)
shell2 = Sprite(x=WIDTH_WIN * 2, y=0, dx=True, dy=False, images=images7, angle=0, scale=0.4)

images8 = load_images(os.path.join(mainpath, 'Image', 'Explosion'))
explosion = SpriteAnimation(x=-200, y=-200, dx=False, dy=False, images=images8, angle=False, scale=0.01)
explosion2 = SpriteAnimation(x=-200, y=-200, dx=False, dy=False, images=images8, angle=False, scale=0.01)

images9 = load_images(os.path.join(mainpath, 'Image', 'Fire'))
fire = Sprite(x=-100, y=-100, dx=False, dy=False, images=images9, angle=0, scale=1.5)
fire2 = Sprite(x=-100, y=-100, dx=True, dy=False, images=images9, angle=0, scale=1.5)

images10 = load_images(os.path.join(mainpath, 'Image', 'Bullet'))
bullet = Sprite(x=helicopter.position.x, y=helicopter.position.y, dx=False, dy=False,
                images=images10, angle=0, scale=1.0)

images11 = load_images(os.path.join(mainpath, 'Image', 'Health'))
health = Health(images=images11)

images12 = load_images(os.path.join(mainpath, 'Image', 'Mouse'))
mouseMenu = Sprite(x=780, y=330, dx=False, dy=False, images=images12, angle=0, scale=0.2)

burn_img = pg.image.load(os.path.join(mainpath, 'Image', 'Burn', '1.png'))
burn_img.set_alpha(125)
images13 = [burn_img.subsurface((0, 0, 141, 237)), burn_img.subsurface((141, 0, 141, 237))]
burn = Burn(x=tank1.position.x, y=tank1.position.y, images=images13)

vol = Volume(20, HEIGHT_WIN - 80)
vol_img = pg.image.load(os.path.join(mainpath, 'Image', 'vol.png'))
vol_img = pg.transform.scale(vol_img, (vol_img.get_width() / 1.5, vol_img.get_height() / 1.5))
vol_img_rect = vol_img.get_rect(center=(vol.rect.centerx + vol.radius // 2, vol.rect.top - vol.rect.w))

bullet_box = pg.sprite.Group(bullet)
shell2_box = pg.sprite.Group(shell2)
all_sprites.change_layer(shell, 1)
all_sprites.change_layer(shell2, 1)
all_sprites.change_layer(bullet, 1)
all_sprites.change_layer(sight, 6)
all_sprites.remove(mouseMenu)

icon()
menu()
initialize_stars(STARS_MAX)

"___________________________________________игровой цикл__________________________________________________"


while run[0]:
    gravitation()

    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            end()
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                salvo = 1
    key = pg.key.get_pressed()

    "Вертолет"
    helicopter.angle = (tank1.position - helicopter.position).as_polar()[1]
    helicopter.velocity = vec(speed + speedH, 1).rotate(helicopter.angle)
    if helicopter.position.x < WIDTH_WIN:
        helicopter.scale += 0.004
        if helicopter.scale > h_max_scale:
            helicopter.scale = h_max_scale

    "Танк1 - движение на позицию"
    if tank1.position.x < tank1_pos:
        tank1.position.x += speed / 1.5
        if tank1.position.x < 0:
            tank1.position.y = tank_position_y

    "Танк2"
    tank2.position.x -= speed + speedT

    "Дуло танков"
    barrel.angle = barrel.velocity.angle_to(pg.mouse.get_pos() - barrel.position)
    if barrel.angle > 10:
        barrel.angle = 10
    if barrel.angle < -25:
        barrel.angle = -25
    barrel.position = tank1.position + (25, -15)
    barrel2.position = tank2.position + (-20, -15)

    "Прицел"
    sight.position = pg.mouse.get_pos()

    "Залп танка 1"
    if (key[pg.K_SPACE] or salvo == 1) and tank1.position.x >= tank1_pos and not salvoT:
        all_sprites.add(fire, layer=2)
        shell.position = fire.position = barrel.position
        shell.angle = fire.angle = barrel.angle
        shell.velocity = vec(projectile_velocity, 0).rotate(shell.angle)
        fire.velocity = vec().rotate(fire.angle)
        barrel.position = tank1.position + (25, -15)
        salvoT = True
        counting = True
        salvo = 0
        soundT1.play()
    elif counting and fire.position.x > barrel.rect.right - speed:
        counting = False
    elif fire.position.x > barrel.rect.right + fire.rect.w:
        fire.velocity.x, fire.velocity.y = 0, 0
        fire.position = barrel.position
        all_sprites.remove(fire)

    "Залп танка 2"
    if tank2.position.x > WIDTH_WIN:
        time_fire = 0
    elif tank2.position.x < random.randrange(500, 701, 10):
        if time_fire == 0:
            salvoT2 = True
            all_sprites.add(fire2, layer=2)
            fire2.position = shell2.position = barrel2.position - barrel2_size
            shell2.angle = fire2.angle = barrel2.angle
            shell2.velocity = vec(-projectile_velocity, 0).rotate(shell2.angle)
            fire2.velocity = vec().rotate(fire2.angle)
            soundT2.play()
    if salvoT2:
        time_fire += 1
        if time_fire > 2:
            fire2.velocity.x, fire2.velocity.y = 0, 0
            all_sprites.remove(fire2)
            salvoT2 = False

    "Стрельба вертолета"
    if helicopter.position.x < WIDTH_WIN:
        bullet.angle = helicopter.angle - 180
        bullet.velocity = vec(-projectile_velocity, 0).rotate(bullet.angle)
        if soundH_stop[0]:
            soundH.play(-1)
            soundH_stop[0] = False
    if helicopter.position.x >= WIDTH_WIN or expH1 \
            or pg.sprite.collide_rect(bullet, earth) or pg.sprite.collide_rect(bullet, earth_clone):
        bullet.velocity.x, bullet.velocity.y = 0, 0
        bullet.position.x = helicopter.position.x - h_width * helicopter.scale / 2.
        bullet.position.y = helicopter.position.y + h_height * helicopter.scale / 1.4
        expH1 = False
    if expH or helicopter.position.x < barrel.rect.right + helicopter.rect.w / 2.:
        bullet.velocity.x, bullet.velocity.y = 0, 0
        bullet.position.x = WIDTH_WIN * 2
        soundH_stop[0] = True
        soundH.stop()

    "Снаряды - collision"
    pg.mask.from_surface(shell.image)
    pg.mask.from_surface(tank2.image)
    if pg.sprite.spritecollideany(tank1, bullet_box):
        # print('пули - Т1')
        if count['killed'] < 100:
            count['life'] -= 0.1
        elif count['killed'] >= 100:
            count['life'] -= 0.2
        expH1 = True
    if pg.sprite.collide_mask(tank1, helicopter):
        # print('H-T1')
        count['life'] -= 1.
        start()
        speedH = random.randint(-1, 1)
        speedT = random.randint(0, 1)
        salvoT = False
    elif pg.sprite.collide_mask(tank1, tank2):
        # print('T1-T2')
        count['life'] -= 1.
        start()
        speedH = random.randint(-1, 1)
        speedT = random.randint(0, 1)
        salvoT = False
    elif pg.sprite.collide_mask(shell, tank2):
        # print('снаряд - T2')
        count['killed'] += 1
        count['life'] += 0.1
        shell.velocity.x, shell.velocity.y = 0, 0
        shell.position.x = -WIDTH_WIN
        explosion.position = tank2.position
        all_sprites.add(explosion, layer=5)
        expT = True
    elif pg.sprite.collide_mask(shell, helicopter):
        # print('снаряд - H')
        count['killed'] += 1
        count['life'] += 0.1
        shell.velocity.x, shell.velocity.y = 0, 0
        shell.position.x = -WIDTH_WIN
        soundH.stop()
        soundH_stop[0] = True
        all_sprites.add(explosion, layer=5)
        explosion.position = helicopter.position
        expH = True
    elif pg.sprite.spritecollideany(shell, earthGroup) or shell.position.x >= WIDTH_WIN - 10:
        # print('снаряд - земля или граница')
        shell.velocity.x, shell.velocity.y = 0, 0
        all_sprites.add(explosion, layer=5)
        explosion.position = shell.position
        if explosion.scale < 0.2:
            explosion.scale += 0.01
        else:
            shell.position.x = -WIDTH_WIN
            explosion.scale = 0.01
            all_sprites.remove(explosion)
            salvoT = False
    elif shell2.position.x < 1:
        shell2.position.x = WIDTH_WIN * 2
        shell2.velocity.x, shell2.velocity.y = 0, 0
        all_sprites.add(explosion2, layer=5)
        explosion2.position = (0, shell2.position.y)
        expT1 = True
    elif pg.sprite.spritecollideany(tank1, shell2_box):
        # print('снаряд2 - Т1')
        if count['killed'] <= 10:
            count['life'] -= 0.1
        elif 10 < count['killed'] < 100:
            count['life'] -= 0.2
        elif count['killed'] >= 100:
            count['life'] -= 0.25
        shell2.position.x = WIDTH_WIN * 2
        shell2.velocity.x, shell2.velocity.y = 0, 0
        all_sprites.add(explosion2, layer=5)
        explosion2.position = tank1.position
        expT1 = True

    if expT1:
        if explosion2.scale < 0.2:
            explosion2.scale += 0.01
        else:
            explosion2.scale = 0.01
            all_sprites.remove(explosion2)
            expT1 = False
    if expT:
        if explosion.scale < 0.2:
            tank2.position.x += speed + speedT
            explosion.scale += 0.01
        else:
            tank2.position.x = WIDTH_WIN * random.randint(2, 3)
            barrel2.angle = random.randint(1, 5)
            speedT = random.randint(0, 1)
            explosion.scale = 0.01
            all_sprites.remove(explosion)
            salvoT = False
            expT = False
    if expH:
        if explosion.scale < 0.2:
            helicopter.velocity.x, helicopter.velocity.y = -1, 2
            explosion.scale += 0.01
        else:
            helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
            helicopter.position.y = random.randint(-200, HEIGHT_WIN - HEIGHT_EARTH * 1.5)
            helicopter.scale = h_max_scale / 2.
            speedH = random.randint(-1, 1)
            explosion.scale = 0.01
            all_sprites.remove(explosion)
            salvoT = False
            expH = False

    if count['life'] > 5.9:
        count['life'] = 5.9
    elif int(count['life']) <= 0:
        count['life'] = 0
        points[0][:3:2] = (330, 'GAME')
        run.reverse()
        menu()
    elif key[pg.K_m]:
        points[0][:3:2] = (310, 'PAUSE')
        run.reverse()
        menu()

    screen.fill(BACKGROUND_COLOR)
    all_sprites.update()
    fire.image.set_alpha(0) if counting else fire.image.set_alpha(255)
    all_sprites.draw(screen)
    display_update()

print('[EXIT]')
pg.quit()
exit()
