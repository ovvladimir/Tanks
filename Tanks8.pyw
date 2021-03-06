import pygame as pg
import random
import os
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1'

# print(f'Версия Pygame {pg.version.ver}')
pg.init()
SIZE_WINDOW = WIDTH_WIN, HEIGHT_WIN = 960, 720
BACKGROUND_COLOR = (100, 0, 255)
pg.display.set_caption('Tanks8')
screen = pg.display.set_mode(SIZE_WINDOW)

"""Шрифт"""
info_string = pg.Surface((WIDTH_WIN, 30))
text_font = pg.font.SysFont('Arial', 24, True, True)

FPS = 60
clock = pg.time.Clock()

STARS_SIZE = 16
STARS_MAX = 100
HEIGHT_Earth = 250
speed = 8
life = 11
killed = 0
kil = str(killed)
soundH_stop = True
vec = pg.math.Vector2
mainpath = os.path.dirname(__file__)

"""Звук"""
soundH = pg.mixer.Sound(os.path.join(mainpath, 'Sound/Выстрел Н.wav'))
soundH.set_volume(0.5)
soundT1 = pg.mixer.Sound(os.path.join(mainpath, 'Sound/Выстрел Т1.wav'))
soundT2 = pg.mixer.Sound(os.path.join(mainpath, 'Sound/Выстрел Т2.wav'))


def load_images(path):
    images = []
    for file_name in os.listdir(os.path.join(mainpath, path)):
        image = pg.image.load(os.path.join(mainpath, path + os.sep + file_name))
        images.append(image)
    # print(path, images)
    return images


class Menu:
    def __init__(self, points):
        self.points = points

    def render(self, surface, font, num_point):
        for a in self.points:
            if num_point == a[5]:
                surface.blit(font.render(a[2], 1, a[4]), (a[0], a[1]))
            else:
                surface.blit(font.render(a[2], 1, a[3]), (a[0], a[1]))

    def menu(self):
        pg.mouse.set_visible(True)
        point = 0
        col = 250
        col_block = 0
        fire_block = 1 if int(life) <= 0 else 0
        text_color = (250, 250, 250)
        tx = WIDTH_WIN
        tx_min = -330

        tank1.velocity.y = 0
        tank1.position.x = 150
        tank1.position.y = 450
        helicopter.velocity.x, helicopter.velocity.y = 0, 0
        helicopter.scale = h_max_scale
        helicopter.position.x = 750
        helicopter.position.y = 150
        barrel.position = tank1.position + (25, -15)
        barrel_x = barrel.position.x + images2[0].get_width() * barrel.scale / 1.4
        barrel_y = barrel.position.y - images2[0].get_height() * barrel.scale / 1.4
        fire.position.x = barrel_x
        fire.position.y = barrel_y
        barrel.angle = -10
        fire.angle = barrel.angle
        helicopter.angle = 180
        bullet.angle = helicopter.angle
        bullet.position.x = -1
        tf = 0
        time_fire = 20
        soundH_stop = True
        soundH.stop()

        menu_box = pg.sprite.Group(bullet, helicopter, barrel, tank1, mouseMenu)

        font_menu = pg.font.SysFont('Arial', 96, True, True)
        font_menu_width = font_menu.size('GAME')[0]
        font_menu2 = pg.font.SysFont('Arial', 24, True, True)
        text1 = font_menu2.render("shoot enemies, score points", 1, text_color)
        text1_pos = (600, 20)
        text2 = font_menu2.render(f"Scored points: {killed}", 1, text_color)
        text2_pos = (20, 20)
        if not life == 11:
            text3 = font_menu2.render("Available lives: " + str(int(life)), 1, text_color)
        else:
            text3 = font_menu2.render("Available lives: 10", 1, text_color)
        text3_pos = (20, 80)
        text4 = font_menu2.render("shot of the tank -", 1, text_color)
        text4_pos = (690, 425)
        text5 = font_menu2.render("left mouse button or space", 1, text_color)
        text5_pos = (630, 455)
        text6 = font_menu2.render('"m" key - menu', 1, text_color)
        text6_pos = (70, 300)

        try:
            d = open(os.path.join(mainpath, 'Record/record.dat'), 'r')
            record = int(d.read())
            d.close()
        except FileNotFoundError:
            with open(os.path.join(mainpath, 'Record/record.dat'), 'w') as d:
                record = 0
                d.write(str(record))
        if record < killed:
            record = killed
            d = open(os.path.join(mainpath, 'Record/record.dat'), 'w')
            d.write(str(record))
            d.close()
        text8 = font_menu2.render(f"Current record: {record}", 1, text_color)
        text8_pos = (20, 50)

        burn_img = pg.image.load(os.path.join(mainpath, "Image/Костер/1.png"))
        burn_img.set_alpha(125)
        images13 = [burn_img.subsurface((0, 0, 141, 237)),
                    burn_img.subsurface((141, 0, 141, 237))]
        burn = Burn(x=tank1.position.x, y=tank1.position.y, images=images13)

        run = True
        while run:
            clock.tick(FPS)

            m_pos = pg.mouse.get_pos()
            for b in self.points:
                if b[0] < m_pos[0] < b[0] + font_menu_width and m_pos[1] > b[1]:
                    point = b[5]
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    run = False
                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        run = False
                    if ev.key == pg.K_UP:
                        if point > 0:
                            point -= 1
                    if ev.key == pg.K_DOWN:
                        if point < len(self.points) - 1:
                            point += 1
                    elif ev.key == pg.K_RETURN:
                        if point == 0 and fire_block == 0:
                            helicopter.position.x = WIDTH_WIN * 2
                            helicopter.scale = h_max_scale / 2
                            tank1.position.x = -200
                            pg.mouse.set_visible(False)
                            return True
                        elif point == 1:
                            run = False
                if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                    if point == 0 and fire_block == 0:
                        helicopter.position.x = WIDTH_WIN * 2
                        helicopter.scale = h_max_scale / 2
                        tank1.position.x = -200
                        pg.mouse.set_visible(False)
                        return True
                    elif point == 1:
                        run = False

            bullet.velocity.x, bullet.velocity.y = -15, 0
            if bullet.position.x < 0:
                bullet.position.x = helicopter.position.x - h_width * helicopter.scale / 2.0
                bullet.position.y = helicopter.position.y + h_height * helicopter.scale / 2.5

            if fire_block == 0:
                if tf == 1:
                    fire.velocity = vec(5, 0).rotate(-10)
                    time_fire += 2
                    if time_fire > 20:
                        fire.kill()
                        tf = 0
                elif tf == 0:
                    fire.position.x = barrel_x
                    fire.position.y = barrel_y
                    time_fire -= 1
                    if time_fire < 0:
                        menu_box.add(fire)
                        tf = 1

            if fire_block == 1:
                running_line = font_menu.render('GAME OVER', 1, (col, 250, 250))
                tx_min = -570
                menu_box.add(burn)
            else:
                running_line = font_menu.render('TANKS', 1, (col, 250, 250))
            text7_pos = (tx, 580)
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

            screen.fill((0, 100, 200))
            self.render(screen, font_menu, point)
            screen.blit(text1, text1_pos)
            screen.blit(text2, text2_pos)
            screen.blit(text3, text3_pos)
            screen.blit(text4, text4_pos)
            screen.blit(text5, text5_pos)
            screen.blit(text6, text6_pos)
            screen.blit(running_line, text7_pos)
            screen.blit(text8, text8_pos)

            menu_box.update()
            menu_box.draw(screen)
            pg.display.update()
        return run


class Health(pg.sprite.Sprite):
    def __init__(self, images):
        pg.sprite.Sprite.__init__(self)
        self.images = images
        self.index = 5
        self.image = images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = info_string.get_rect().center

    def update(self):
        self.index = round(life / 2.0)
        self.image = self.images[self.index]


class Earth(pg.sprite.Sprite):
    def __init__(self, x, y, images):
        pg.sprite.Sprite.__init__(self)

        self.images = images
        self.index = 0  # первый кадр (костюм)
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= speed
        if self.rect.x <= -WIDTH_WIN:
            self.rect.x = WIDTH_WIN
            self.index = random.randrange(self.range)
            self.image = self.images[self.index]
            mask()


class Stars(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.speed = random.randint(1, 3)
        self.STARS_SIZE = random.randint(8, 16)
        self.img = pg.image.load(os.path.join(mainpath, 'Image/star16.png'))
        self.image = pg.transform.scale(self.img, (self.STARS_SIZE, self.STARS_SIZE))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH_WIN


class SpriteAnimation(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        pg.sprite.Sprite.__init__(self)
        self.angle = angle
        self.scale = scale
        self.images = [pg.transform.flip(im, dx, dy) for im in images]

        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.position = vec(x, y)
        self.velocity = vec()

    def update(self):
        images = [pg.transform.rotozoom(img, -self.angle, self.scale) for img in self.images]
        self.index += 0.2
        self.image = images[int(self.index % self.range)]

        self.position += self.velocity
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))


class Sprite(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        pg.sprite.Sprite.__init__(self)
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
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))


class Burn(pg.sprite.Sprite):
    def __init__(self, images, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = images
        self.frame = 0
        self.range = len(self.images)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=(int(x), int(y - self.image.get_height() / 3.)))

    def update(self):
        self.frame += 0.2
        self.image = self.images[int(self.frame % self.range)]


def initialize_stars(stars_max):
    for _ in range(stars_max):
        xx = random.randint(0, WIDTH_WIN)
        yy = random.randint(0, HEIGHT_WIN - HEIGHT_Earth)
        all_sprites.add(Stars(xx, yy), layer=-1)


def gravitation():
    tank1.velocity.y += 1
    # tank1.position.y += tank1.velocity.y  # есть в class
    while pg.sprite.spritecollideany(tank1, earthGroup, pg.sprite.collide_mask):
        tank1.position.y -= 1
        tank1.velocity.y = 0
        tank1.rect.centery = int(tank1.position.y)
    tank2.velocity.y += 1
    while pg.sprite.spritecollideany(tank2, earthGroup, pg.sprite.collide_rect_ratio(0.98)):
        tank2.position.y -= 1
        tank2.velocity.y = 0
        tank2.rect.centery = int(tank2.position.y)


def mask():
    for sp in earthGroup:
        sp.mask = pg.mask.from_threshold(sp.image, earthColor, (1, 1, 1, 255))


"""____________________________________________________Main_______________________________________________________"""

salvo = 0
salvoT = False
salvoT2 = False
speedT = 0
speedH = random.randint(-1, 1)
time_fire1 = 0
time_fire2 = 0
expT = False
expT1 = False
expH = False
expH1 = False
hit = False

images0 = load_images(path='Image/Earth')
earth = Earth(x=0, y=HEIGHT_WIN - images0[0].get_height(), images=images0)
earth_clone = Earth(x=WIDTH_WIN, y=HEIGHT_WIN - images0[0].get_height(),
                    images=images0)
earthColor = images0[0].get_at((30, 30))

images1 = load_images(path='Image/Tank1')
tank1_pos = 196
tank_width = images1[0].get_width()
tank1 = SpriteAnimation(x=150, y=450, dx=False, dy=False, images=images1,
                        angle=0, scale=1.7)

images2 = load_images(path='Image/Дуло1')
barrel = Sprite(x=tank1.position.x, y=tank1.position.y, dx=False, dy=False,
                images=images2, angle=-10, scale=1.2)

images3 = load_images(path='Image/Helicopter')
h_max_scale = 0.6
h_width = images3[0].get_width()
h_height = images3[0].get_height()
helicopter = SpriteAnimation(x=750, y=150, dx=False, dy=True, images=images3,
                             angle=180, scale=h_max_scale / 2.0)

images4 = load_images(path='Image/Tank2')
tank2 = SpriteAnimation(x=2000, y=0, dx=False, dy=False, images=images4,
                        angle=0, scale=1.7)

images5 = load_images(path='Image/Дуло2')
barrel2 = Sprite(x=tank2.position.x, y=tank2.position.y, dx=False, dy=False,
                 images=images5, angle=5, scale=1.2)
barrel2_pos = (images5[0].get_width() * barrel2.scale / 2.0,
               images5[0].get_height() * barrel2.scale / 4.0)

images6 = load_images(path='Image/Прицел')
sight = Sprite(x=0, y=0, dx=False, dy=False, images=images6, angle=False, scale=0.5)

images7 = load_images(path='Image/Снаряд')
shell = Sprite(x=-100, y=0, dx=False, dy=False, images=images7, angle=0, scale=0.4)
shell2 = Sprite(x=WIDTH_WIN * 2, y=0, dx=True, dy=False, images=images7, angle=0, scale=0.4)

images8 = load_images(path='Image/Взрыв')
explosion = SpriteAnimation(x=-200, y=-200, dx=False, dy=False, images=images8,
                            angle=False, scale=0.01)
explosion2 = SpriteAnimation(x=-200, y=-200, dx=False, dy=False, images=images8,
                             angle=False, scale=0.01)

images9 = load_images(path='Image/fire')
fire = Sprite(x=-100, y=-100, dx=False, dy=False, images=images9, angle=0, scale=1.5)

fire2 = Sprite(x=-100, y=-100, dx=True, dy=False, images=images9, angle=0, scale=1.5)

images10 = load_images(path='Image/Bullet')
bullet = Sprite(x=helicopter.position.x, y=helicopter.position.y, dx=False, dy=False,
                images=images10, angle=0, scale=1.0)

images11 = load_images(path='Image/Здоровье')
health = Health(images=images11)

images12 = load_images(path='Image/Mouse')
mouseMenu = Sprite(x=780, y=330, dx=False, dy=False, images=images12,
                   angle=0, scale=0.2)

earthGroup = pg.sprite.Group(earth, earth_clone)
bullet_box = pg.sprite.Group(bullet)
shell_box = pg.sprite.Group(shell)
shell2_box = pg.sprite.Group(shell2)
player_box = pg.sprite.Group(tank1)
other_box = pg.sprite.Group(helicopter, barrel2, tank2, barrel)
all_sprites = pg.sprite.LayeredUpdates(health, earth, earth_clone)
all_sprites.add(other_box, layer=2)
all_sprites.add(player_box, layer=3)
all_sprites.add(sight, layer=5)
all_sprites.add(bullet_box, layer=0)
all_sprites.add(shell2, layer=0)

initialize_stars(STARS_MAX)
mask()

"""Пункты меню"""
menu_points = [(330, 250, 'GAME', (250, 250, 30), (250, 30, 250), 0),
               (350, 350, 'QUIT', (250, 250, 30), (250, 30, 250), 1)]
game = Menu(points=menu_points)
runGame = game.menu()

"""___________________________________________игровой цикл__________________________________________________"""

while runGame:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            runGame = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                salvo = 1
    key = pg.key.get_pressed()

    gravitation()
    """Танк1"""
    if tank1.position.x < tank1_pos:
        tank1.position.x += speed / 1.5
        all_sprites.remove(shell_box)
        all_sprites.remove(fire)
        if tank1.position.x < 0:
            tank1.velocity.y = 0

    """Вертолет"""
    helicopter.angle = (tank1.position - helicopter.position).as_polar()[1]
    helicopter.velocity = vec(speed + speedH, 0.3).rotate(helicopter.angle)
    if helicopter.position.x < WIDTH_WIN:
        helicopter.scale += 0.004
        if helicopter.scale > h_max_scale:
            helicopter.scale = h_max_scale

    """Танк2"""
    tank2.position.x -= speed + speedT
    if tank2.position.x > WIDTH_WIN + tank_width * 2 or tank2.position.x < 0 \
            or tank2.position.y < 0 or tank2.position.y > HEIGHT_WIN:
        tank2.position.y = HEIGHT_WIN - HEIGHT_Earth
        tank2.velocity.y = 0

    """Дуло"""
    barrel.angle = barrel.velocity.angle_to(pg.mouse.get_pos() - barrel.position)
    if barrel.angle > 10:
        barrel.angle = 10
    if barrel.angle < -25:
        barrel.angle = -25
    barrel.position = tank1.position + (25, -15)
    barrel2.position = tank2.position + (-20, -15)

    """Прицел"""
    sight.position = pg.mouse.get_pos()

    """Залп танка 1"""
    if (key[pg.K_SPACE] or salvo == 1) and tank1.position.x >= tank1_pos and hit is False and salvoT is False:
        shell_box.add(shell)
        fire.position = barrel.position
        shell.position = barrel.position + (0, -1)
        fire.angle = barrel.angle
        shell.angle = barrel.angle
        fire.velocity = vec(15, 0).rotate(fire.angle)
        shell.velocity = vec(15, 0).rotate(shell.angle)
        salvoT = True
        time_fire1 = 0
        soundT1.play()
    elif not pg.sprite.collide_rect(fire, barrel):
        all_sprites.add(shell_box, layer=0)
        all_sprites.add(fire, layer=1)
        time_fire1 += 1
        if time_fire1 > 2:
            all_sprites.remove(fire)
            fire.velocity.x, fire.velocity.y = 0, 0
            fire.position = barrel.position
    shell.update()
    fire.update()
    salvo = 0

    """Залп танка 2"""
    if tank2.position.x > WIDTH_WIN:
        time_fire2 = 0
    if tank2.position.x < random.randrange(500, 701, 10):
        if time_fire2 == 0:
            salvoT2 = True
            all_sprites.add(fire2, layer=1)
            fire2.position = barrel2.position - barrel2_pos
            shell2.position = barrel2.position - barrel2_pos
            fire2.angle = barrel2.angle
            shell2.angle = barrel2.angle
            fire2.velocity = vec(-15 - speed - speedT, 0).rotate(fire2.angle)
            shell2.velocity = vec(-15 - speed - speedT, 0).rotate(shell2.angle)
            soundT2.play()
    if salvoT2:
        time_fire2 += 1
        if time_fire2 > 2:
            all_sprites.remove(fire2)
            salvoT2 = False

    """Стрельба вертолета"""
    if helicopter.position.x < WIDTH_WIN:
        bullet.angle = helicopter.angle - 180
        bullet.velocity = vec(-15 - speed - speedH, 0).rotate(bullet.angle)
        if soundH_stop:
            soundH.play(-1)
            soundH_stop = False
    if bullet.position.x < 0 or helicopter.position.x > WIDTH_WIN \
            or pg.sprite.collide_rect(bullet, earth) or pg.sprite.collide_rect(bullet, earth_clone) \
            or expH1:
        bullet.velocity.x, bullet.velocity.y = 0, 0
        bullet.position.x = helicopter.position.x - h_width * helicopter.scale / 2.0
        bullet.position.y = helicopter.position.y + h_height * helicopter.scale / 1.4
        expH1 = False

    """Снаряды - collision"""
    if pg.sprite.spritecollide(tank2, shell_box, True):
        # print('снаряд - T2')
        killed += 1
        life += 0.2
        all_sprites.add(explosion, layer=4)
        expT = True
    elif pg.sprite.spritecollide(helicopter, shell_box, True, pg.sprite.collide_circle_ratio(.6)):
        # print('снаряд - H')
        killed += 1
        life += 0.2
        all_sprites.add(explosion, layer=4)
        expH = True
    elif pg.sprite.spritecollideany(shell, earthGroup) or shell.position.x >= WIDTH_WIN - 10:
        all_sprites.remove(shell_box)
        all_sprites.add(explosion, layer=4)
        shell.velocity.x, shell.velocity.y = 0, 0
        if explosion.scale < 0.2:
            explosion.position = shell.position
            explosion.scale += 0.01
        else:
            salvoT = False
            shell.position = barrel.position + (0, -1)
            fire.velocity.x, fire.velocity.y = 0, 0
            fire.position = barrel.position
            explosion.scale = 0.01
            all_sprites.remove(explosion)
    elif pg.sprite.spritecollide(helicopter, player_box, True, pg.sprite.collide_rect_ratio(.7)):
        life -= 1
        # print('H-T1')
        all_sprites.remove(other_box)
        hit = True
    elif pg.sprite.spritecollide(tank2, player_box, True):
        life -= 1
        # print('T1-T2')
        all_sprites.remove(other_box)
        hit = True
    elif pg.sprite.spritecollideany(tank1, bullet_box):
        if killed <= 100:
            life -= 0.2
        elif 100 < killed < 1000:
            kil = float(f'0.{(str(killed))[0]}')
            life -= 0.2 + kil
        else:
            life -= 1
        expH1 = True
        # print('пули - Т1')
    elif shell2.position.x < 1:
        explosion2.position = (0, shell2.position.y)
        expT1 = True
    elif pg.sprite.spritecollideany(tank1, shell2_box):
        explosion2.position = tank1.position
        if killed <= 100:
            life -= 0.2
        elif 100 < killed < 1000:
            kil = str(killed)
            life -= 0.2 * (int(kil[0]) + 1)
        else:
            life -= 2
        expT1 = True
        # print('снаряд2 - Т1')

    if expT1:
        shell2.position.x = WIDTH_WIN * 2
        shell2.velocity.x, shell2.velocity.y = 0, 0
        all_sprites.add(explosion2, layer=4)
        if explosion2.scale < 0.2:
            explosion2.scale += 0.01
        else:
            explosion2.scale = 0.01
            all_sprites.remove(explosion2)
            expT1 = False
    if expT:
        if explosion.scale < 0.2:
            shell.velocity.x, shell.velocity.y = 0, 0
            tank2.position.x += speed + speedT
            explosion.position = tank2.position
            explosion.scale += 0.01
        else:
            tank2.position.x = WIDTH_WIN * random.randint(2, 3)
            barrel2.angle = random.randint(1, 5)
            explosion.scale = 0.01
            shell.position = barrel.position + (0, -1)
            all_sprites.remove(explosion)
            all_sprites.remove(shell_box)
            speedT = random.randint(0, 1)
            salvoT = False
            expT = False
    if expH:
        bullet.position.x = WIDTH_WIN * 2
        bullet.velocity.x, bullet.velocity.y = 0, 0
        soundH.stop()
        soundH_stop = True
        if explosion.scale < 0.2:
            shell.velocity.x, shell.velocity.y = 0, 0
            helicopter.velocity.x, helicopter.velocity.y = -1, 2
            explosion.position = helicopter.position
            explosion.scale += 0.01
        else:
            helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
            helicopter.position.y = random.randint(-200, HEIGHT_WIN - HEIGHT_Earth * 1.5)
            explosion.scale = 0.01
            shell.position = barrel.position + (0, -1)
            all_sprites.remove(explosion)
            all_sprites.remove(shell_box)
            helicopter.scale = h_max_scale / 2
            speedH = random.randint(-1, 1)
            salvoT = False
            expH = False
    if hit:
        bullet.position.x = WIDTH_WIN * 2
        bullet.velocity.x, bullet.velocity.y = 0, 0
        all_sprites.remove(explosion)
        all_sprites.remove(explosion2)
        all_sprites.remove(shell_box)
        all_sprites.remove(fire)
        all_sprites.remove(fire2)
        all_sprites.add(other_box, layer=2)
        player_box.add(tank1)
        all_sprites.add(player_box, layer=3)
        tank1.position.x = -WIDTH_WIN // 2
        tank2.position.x = WIDTH_WIN * random.randint(2, 3)
        helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
        helicopter.position.y = random.randint(-200, HEIGHT_WIN - HEIGHT_Earth * 1.5)
        barrel.position = tank1.position + (25, -15)
        barrel2.position = tank2.position + (-21, -15)
        barrel2.angle = random.randint(1, 5)
        helicopter.scale = h_max_scale / 2
        speedH = random.randint(-1, 1)
        speedT = random.randint(0, 1)
        fire.velocity.x, fire.velocity.y = 0, 0
        fire.position = barrel.position
        shell2.velocity.x, shell2.velocity.y = 0, 0
        shell2.position.x = WIDTH_WIN * 2
        shell.velocity.x, shell.velocity.y = 0, 0
        shell.position = barrel.position + (0, -1)
        soundH_stop = True
        soundH.stop()
        salvoT = False
        hit = False

    if life > 10:
        life = 10
    elif int(life) <= 0:
        life = 0
        menu_points[0] = (330, 250, 'CLICK', (250, 250, 30), (250, 250, 30), 0)
        runGame = game.menu()
    elif key[pg.K_m]:
        menu_points[0] = (330, 250, 'PAUSE', (250, 250, 30), (250, 30, 250), 0)
        runGame = game.menu()
    if not runGame:
        break

    all_sprites.update()
    screen.fill(BACKGROUND_COLOR)

    info_string.fill((90, 0, 255))
    info_string.blit(text_font.render(f'Points: {killed}', 1, (255, 255, 255)), (10, 2))
    info_string.blit(text_font.render(f'Life: {int(life)}', 1, (255, 255, 255)), (868, 2))
    screen.blit(info_string, (0, 0))

    all_sprites.draw(screen)
    pg.display.set_caption(f'Tanks8   FPS: {int(clock.get_fps())}')
    pg.display.update()

print('[EXIT]')
sys.exit(0)
