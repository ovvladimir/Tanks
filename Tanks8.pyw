import pygame as pg
import random
import os
import sys

# print(f'Версия Pygame {pg.version.ver}')
pg.init()
SIZE_WINDOW = WIDTH_WIN, HEIGHT_WIN = 960, 720
BACKGROUND_COLOR = (100, 0, 255)
screen = pg.display.set_mode(SIZE_WINDOW)
pg.display.set_caption('Tanks8')

"""Шрифт"""
info_string = pg.Surface((WIDTH_WIN, 30))
pg.font.init()
text_font = pg.font.SysFont('Arial', 24, True, True)

"""Звук"""
pg.mixer.pre_init(44100, -16, 2, 1024)
pg.mixer.init()

FPS = 120
clock = pg.time.Clock()

STARS_SIZE = 16
STARS_MAX = 100
WIDTH_Earth = 960
HEIGHT_Earth = 300
speed = 8
life = 11
killed = 0


def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pg.image.load(path + os.sep + file_name).convert_alpha()
        images.append(image)
    print(path, images)
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
        global e
        point = 0
        col = 250
        col_block = 0
        fire_block = 0
        text_color = (250, 250, 250)
        tx = WIDTH_WIN
        tx_min = -330

        helicopter.velocity = (0, 0)
        tank1.velocity.y = 0
        tank1.position.x = 150
        tank1.position.y = 450
        helicopter.position.x = 750
        helicopter.position.y = 150
        barrel.position.x = tank1.position.x + 25
        barrel.position.y = tank1.position.y - 15
        salvoH2 = 0
        salvoT2 = 0
        time_fire = 0
        menu_box = pg.sprite.Group(helicopter, barrel, tank1, mouseMenu)
        if int(life) <= 0:
            # menu_box.add(burn)
            fire_block = 1

        font_menu = pg.font.SysFont('Arial', 96, True, True)
        font_menu2 = pg.font.SysFont('Arial', 24, True, True)
        text1 = font_menu2.render("shoot enemies, score points", 1, text_color)
        text1_pos = (600, 20)
        text2 = font_menu2.render("Сейчас очков: " + str(killed), 1, text_color)
        text2_pos = (20, 20)
        if not life == 11:
            text3 = font_menu2.render("Доступно жизней: " + str(int(life)), 1, text_color)
        else:
            text3 = font_menu2.render("Доступно жизней: 10", 1, text_color)
        text3_pos = (20, 80)
        text4 = font_menu2.render("shot of the tank -", 1, text_color)
        text4_pos = (690, 425)
        text5 = font_menu2.render("left mouse button or space", 1, text_color)
        text5_pos = (630, 455)
        text6 = font_menu2.render("m button - menu", 1, text_color)
        text6_pos = (70, 300)

        d = open('Record/record.dat', 'r')
        record = int(d.read())
        d.close()
        if record < killed:
            record = killed
            d = open('Record/record.dat', 'w')
            d.write(str(record))
            d.close()
        text8 = font_menu2.render("Текущий рекорд: " + str(record), 1, text_color)
        text8_pos = (20, 50)

        burn_img = pg.image.load("Image/Костер/1.png").convert(24)
        burn_img.set_alpha(160)
        burn_img.set_colorkey((0, 0, 0))
        images13 = [burn_img.subsurface((0, 0, 141, 237)),
                    burn_img.subsurface((141, 0, 141, 237))]
        burn = Burn(x=tank1.position.x - 70, y=tank1.position.y - 200, images=images13)

        runMenu = True
        while runMenu:
            pg.time.wait(5)

            m_pos = pg.mouse.get_pos()
            for b in self.points:
                if b[0] < m_pos[0] < b[0] + 280 and m_pos[1] > b[1]:  # 280 - ширина букв
                    point = b[5]
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        sys.exit()
                    if e.key == pg.K_UP:
                        if point > 0:
                            point -= 1
                    if e.key == pg.K_DOWN:
                        if point < len(self.points) - 1:
                            point += 1
                    elif e.key == pg.K_RETURN:  # возврвт каретки (ENTER)
                        if point == 0 and fire_block == 0:
                            runMenu = False
                        elif point == 1:
                            sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if point == 0 and fire_block == 0:
                    runMenu = False
                elif point == 1:
                    sys.exit()

            if salvoH2 == 0:
                bullet.position.x = helicopter.position.x
                bullet.position.y = helicopter.position.y + 30
                bullet.velocity = pg.math.Vector2(-25, 0)
                salvoH2 = 1
            elif not bullet.rect.colliderect(helicopter.rect):
                menu_box.add(bullet)
                if bullet.position.x < 0:
                    bullet.velocity = (0, 0)
                    menu_box.remove(bullet)
                    salvoH2 = 0
            if fire_block == 0:
                if salvoT2 == 0:
                    fire.position.x = barrel.position.x
                    fire.position.y = barrel.position.y
                    fire.velocity = pg.math.Vector2(3, 0).rotate(-10)
                    time_fire = 0
                    salvoT2 = 1
                elif not fire.rect.colliderect(barrel.rect):
                    menu_box.add(fire)
                    time_fire += 1
                    if time_fire > 3:
                        menu_box.remove(fire)
                        salvoT2 = 0

            if fire_block == 1:
                running_line = font_menu.render('GAME OVER', 1, (col, 250, 250))
                tx_min = -570
            else:
                running_line = font_menu.render('ТАНКИ', 1, (col, 250, 250))
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
            tank1.update(images1, False, False, 0, 1.8)
            barrel.update(images2, False, False, -10, 1.2)
            helicopter.update(images3, True, False, 0, 0.55)
            bullet.update(images10, False, False, -180, 1)
            fire.update(images9, False, False, -10, 1.5)
            menu_box.draw(screen)
            if fire_block == 1:
                burn.update(screen)
            pg.display.flip()


class Health(pg.sprite.Sprite):
    def __init__(self, images):
        super(Health, self).__init__()
        self.images = images
        self.index = 5
        self.image = images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = info_string.get_rect().center

    def update(self):
        self.index = round(life / 2)
        self.image = self.images[self.index]


class Earth(pg.sprite.Sprite):
    def __init__(self, x, y, images):
        super(Earth, self).__init__()

        self.images = images
        self.index = 0  # первый кадр (костюм)
        self.image = images[self.index]

        self.position = pg.math.Vector2(x, y)
        self.rect = self.image.get_rect()

    def update(self):
        self.position.x -= speed
        if self.position.x <= 0 - WIDTH_Earth / 2:
            self.position.x = WIDTH_WIN + WIDTH_Earth / 2
            self.index += random.randint(1, 2)
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

        self.rect.center = self.position


class Stars:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)
        self.STARS_SIZE = random.randint(8, 16)
        self.image_filename = 'Image/star16.png'
        self.image = pg.image.load(self.image_filename).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.STARS_SIZE, self.STARS_SIZE))

    def move_star(self):
        self.x = self.x - self.speed
        if self.x < 0:
            self.x = WIDTH_WIN

    def draw_star(self):
        screen.blit(self.image, (self.x, self.y))


class SpriteAnimation(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        super(SpriteAnimation, self).__init__()

        images = [pg.transform.flip(image, dx, dy) for image in images]
        images = [pg.transform.rotozoom(image, -angle, scale) for image in images]
        self.images = images
        self.index = 0
        self.image = images[self.index]

        self.velocity = pg.math.Vector2(0, 0)
        self.position = pg.math.Vector2(x, y)
        self.rect = self.image.get_rect()

    def update(self, images, dx, dy, angle, scale):
        images = [pg.transform.flip(image, dx, dy) for image in images]
        images = [pg.transform.rotozoom(image, -angle, scale) for image in images]
        self.images = images
        self.index += 0.2
        self.image = self.images[int(self.index % len(self.images))]

        self.position += self.velocity
        self.rect.center = self.position
        self.rect = self.image.get_rect(center=self.rect.center)


class Sprite(pg.sprite.Sprite):
    def __init__(self, images, x, y, dx, dy, angle, scale):
        super(Sprite, self).__init__()
        images = [pg.transform.flip(image, dx, dy) for image in images]
        images = [pg.transform.rotozoom(image, -angle, scale) for image in images]
        self.images = images
        self.image = images[0]

        self.velocity = pg.math.Vector2(0, 0).rotate(angle)
        self.position = pg.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, images, dx, dy, angle, scale):
        images = [pg.transform.flip(image, dx, dy) for image in images]
        images = [pg.transform.rotozoom(image, -angle, scale) for image in images]
        self.images = images
        self.image = self.images[0]

        self.position += self.velocity
        self.rect.center = self.position
        self.rect = self.image.get_rect(center=self.rect.center)


class Burn:
    def __init__(self, images, x, y):
        self.x = x
        self.y = y
        self.images = images
        self.frame = 0
        self.image = images[self.frame]

    def update(self, scr):
        self.frame += 0.2
        self.image = self.images[int(self.frame % len(self.images))]
        scr.blit(self.image, (self.x, self.y))


def initialize_stars(stars_max, star):
    for n in range(0, stars_max):
        xx = random.randint(0, WIDTH_WIN)
        yy = random.randint(0, HEIGHT_WIN - HEIGHT_Earth)
        star.append(Stars(xx, yy))


def gravitation():
    tank1.velocity.y += 1
    while tank1.rect.colliderect(earth.rect) or tank1.rect.colliderect(earth_clone.rect):
        tank1.rect.y -= 1
        tank1.position.y -= 1
        tank1.velocity.y = 0
    tank2.velocity.y += 1
    while tank2.rect.colliderect(earth.rect) or tank2.rect.colliderect(earth_clone.rect):
        tank2.rect.y -= 1
        tank2.position.y -= 1
        tank2.velocity.y = 0


"""____________________________________________________Main_______________________________________________________"""
stars = []
initialize_stars(STARS_MAX, stars)

tank_width = 84
tank1_dx = False  # 1 - True, 0 - False
tank1_dy = False
tank1_angle = 0
tank1_scale = 1.80
tank1_pos = 196
barrel_dx = False
barrel_dy = False
barrel_angle = -10
barrel_scale = 1.20
h_dx = False
h_dy = True
h_angle = 0
h_scale = 0.35
h_max_scale = 0.6
h_height = 150
tank2_dx = False
tank2_dy = False
tank2_angle = 0
tank2_scale = 1.80
barrel2_dx = False
barrel2_dy = False
barrel2_angle = 5
barrel2_scale = 1.2
sight_dx = False
sight_dy = False
sight_angle = 0
sight_scale = 0.5
shell_dx = False
shell_dy = False
shell_angle = 0
shell_scale = 0.4
shell2_dx = True
shell2_angle = 0
explosion_dx = False
explosion_dy = False
explosion_angle = 0
explosion_scale = 0.01
explosion2_scale = 0.01
fire2_dx = True
fire2_angle = 0
fire_dx = False
fire_dy = False
fire_angle = 0
fire_scale = 1.5
bullet_dx = False
bullet_dy = False
bullet_angle = 0
bullet_scale = 1.0
blocking = 0
salvoT = 0
salvoH = 0
speedT = 0
speedH = random.randint(-1, 1)
time_fire1 = 0
time_fire2 = 0
expT = 0
expT1 = 0
expH = 0
expH1 = 0
hit = 0

images0 = load_images(path='Image/Earth')
earth = Earth(x=WIDTH_Earth / 2, y=HEIGHT_WIN - HEIGHT_Earth / 2, images=images0)
earth_clone = Earth(x=WIDTH_Earth / 2 + WIDTH_Earth, y=HEIGHT_WIN - HEIGHT_Earth / 2, images=images0)

images1 = load_images(path='Image/Tank1')
tank1 = SpriteAnimation(x=tank1_pos, y=420,
                        dx=tank1_dx, dy=tank1_dy,
                        images=images1,
                        angle=tank1_angle, scale=tank1_scale)

images2 = load_images(path='Image/Дуло1')
barrel = Sprite(x=tank1.position.x + 25, y=tank1.position.y - 15,
                dx=barrel_dx, dy=barrel_dy,
                images=images2,
                angle=barrel_angle, scale=barrel_scale)

images3 = load_images(path='Image/Helicopter')
helicopter = SpriteAnimation(x=700, y=150,
                             dx=h_dx, dy=h_dy,
                             images=images3,
                             angle=h_angle, scale=h_scale)

images4 = load_images(path='Image/Tank2')
tank2 = SpriteAnimation(x=2000, y=420,
                        dx=tank2_dx, dy=tank2_dy,
                        images=images4,
                        angle=tank2_angle, scale=tank2_scale)

images5 = load_images(path='Image/Дуло2')
barrel2 = Sprite(x=2000, y=420,
                 dx=barrel2_dx, dy=barrel2_dy,
                 images=images5,
                 angle=barrel2_angle, scale=barrel2_scale)

images6 = load_images(path='Image/Прицел')
sight = Sprite(x=0, y=0,
               dx=sight_dx, dy=sight_dy,
               images=images6,
               angle=sight_angle, scale=sight_scale)

images7 = load_images(path='Image/Снаряд')
shell = Sprite(x=-100, y=0,
               dx=shell_dx, dy=shell_dy,
               images=images7,
               angle=shell_angle, scale=shell_scale)
shell2 = Sprite(x=1000, y=0,
                dx=shell2_dx, dy=shell_dy,
                images=images7,
                angle=shell2_angle, scale=shell_scale)

images8 = load_images(path='Image/Взрыв')
explosion = SpriteAnimation(x=-200, y=-200,
                            dx=explosion_dx, dy=explosion_dy,
                            images=images8,
                            angle=explosion_angle, scale=explosion_scale)
explosion2 = SpriteAnimation(x=-200, y=-200,
                             dx=explosion_dx, dy=explosion_dy,
                             images=images8,
                             angle=explosion_angle, scale=explosion2_scale)

images9 = load_images(path='Image/fire')
fire = Sprite(x=-300, y=-300,
              dx=fire_dx, dy=fire_dy,
              images=images9,
              angle=fire_angle, scale=fire_scale)

fire2 = Sprite(x=-300, y=-300,
               dx=fire2_dx, dy=fire_dy,
               images=images9,
               angle=fire2_angle, scale=fire_scale)

images10 = load_images(path='Image/Bullet')
bullet = Sprite(x=-500, y=100,
                dx=bullet_dx, dy=bullet_dy,
                images=images10,
                angle=bullet_angle, scale=bullet_scale)

images11 = load_images(path='Image/Здоровье')
health = Health(images=images11)

images12 = load_images(path='Image/Mouse')
mouseMenu = Sprite(x=780, y=330,
                   dx=False, dy=False,
                   images=images12,
                   angle=0, scale=0.2)

"""images13 = load_images(path='Image/Костер')
burn = SpriteAnimation(x=tank1.position.x-40, y=tank1.position.y-45,
                       dx=False, dy=False,
                       images=images13,
                       angle=0, scale=0.3)"""

bullet_box = pg.sprite.Group(bullet)
shell_box = pg.sprite.Group(shell)
shell2_box = pg.sprite.Group(shell2)
player_box = pg.sprite.Group(tank1)
sight_box = pg.sprite.Group(sight)
other_box = pg.sprite.Group(helicopter, barrel2, tank2, barrel)
all_sprites = pg.sprite.LayeredUpdates(health, earth, earth_clone)
all_sprites.add(other_box, layer=2)
all_sprites.add(player_box, layer=3)
all_sprites.add(sight_box, layer=5)

"""Пункты меню"""
menu_points = [(330, 250, 'GAME', (250, 250, 30), (250, 30, 250), 0),
               (350, 350, 'QUIT', (250, 250, 30), (250, 30, 250), 1)]
game = Menu(points=menu_points)
game.menu()

"""Звук"""
soundT1 = pg.mixer.Sound('Sound/Выстрел Т1.wav')
soundT2 = pg.mixer.Sound('Sound/Выстрел Т2.wav')
soundH = pg.mixer.Sound('Sound/Выстрел Н.wav')
"""___________________________________________игровой цикл__________________________________________________"""
while True:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            sys.exit()

    """Танк1"""
    if tank1.position.x < tank1_pos:
        tank1.position.x += speed / 1.5
        all_sprites.remove(shell_box)
        all_sprites.remove(fire)
        tank1.velocity.y = 0

    """Вертолет"""
    _, h_angle = (tank1.position - helicopter.position).as_polar()
    helicopter.velocity = pg.math.Vector2(speed + speedH, 1).rotate(h_angle)
    if helicopter.position.x < WIDTH_WIN:
        h_scale += 0.003
        if h_scale > h_max_scale:
            h_scale = h_max_scale

    """Танк2"""
    tank2.position.x -= speed + speedT
    if tank2.position.x > WIDTH_WIN + tank_width * 2 or tank2.position.x < 0 \
            or tank2.position.y < 0 or tank2.position.y > HEIGHT_WIN:
        tank2.position.y = HEIGHT_WIN - HEIGHT_Earth * 1.2
        tank2.rect.y = tank2.position.y
        tank2.velocity.y = 0

    """Дуло"""
    _, barrel_angle = (pg.mouse.get_pos() - barrel.position).as_polar()
    if barrel_angle > 10:
        barrel_angle = 10
    if barrel_angle < -25:
        barrel_angle = -25
    barrel.position = tank1.position + (25, -15)
    barrel2.position = tank2.position + (-20, -15)

    """Прицел"""
    pg.mouse.set_visible(False)
    sight.position = pg.mouse.get_pos()

    """Снаряд"""
    if pg.sprite.spritecollide(tank2, shell_box, True):
        print('снаряд - T2')
        killed += 1
        life += 0.2
        all_sprites.add(explosion, layer=4)
        expT = 1
    elif pg.sprite.spritecollide(helicopter, shell_box, True, pg.sprite.collide_rect_ratio(.4)):
        print('снаряд - H')
        killed += 1
        life += 0.2
        all_sprites.add(explosion, layer=4)
        expH = 1
    elif shell.rect.colliderect(earth.rect) \
            or shell.rect.colliderect(earth_clone.rect) or shell.position.x >= WIDTH_WIN:
        # print('снаряд - E')
        all_sprites.remove(shell_box)
        all_sprites.add(explosion, layer=4)
        if explosion_scale <= 0.2:
            shell.velocity = (0, 0)
            explosion.position = shell.position
            explosion_scale += 0.01
        else:
            blocking = 0
            shell.velocity = (0, 0)
            shell.position = barrel.position + (0, -1)
            fire.velocity = (0, 0)
            fire.position = barrel.position
            explosion_scale = 0.01
            all_sprites.remove(explosion)
    elif pg.sprite.spritecollide(helicopter, player_box, True, pg.sprite.collide_rect_ratio(.7)):
        life -= 1
        print('H-T1')
        all_sprites.remove(other_box)
        hit = 1
    elif pg.sprite.spritecollide(tank2, player_box, True):
        life -= 1
        print('T1-T2')
        all_sprites.remove(other_box)
        hit = 1
    elif expT == 1:
        if explosion_scale <= 0.2:
            shell.velocity = (0, 0)
            tank2.position.x += speed + speedT
            explosion.position = tank2.position
            explosion_scale += 0.01
        else:
            tank2.position.x = WIDTH_WIN * random.randint(2, 3)
            barrel2.position = tank2.position
            explosion_scale = 0.01
            shell.position = barrel.position + (0, -1)
            all_sprites.remove(explosion)
            all_sprites.remove(shell_box)
            speedT = random.randint(0, 1)
            barrel2_angle = random.randint(2, 5)
            blocking = 0
            expT = 0
    elif expH == 1:
        if explosion_scale <= 0.2:
            shell.velocity = (0, 0)
            helicopter.velocity = (-1, 2)
            explosion.position = helicopter.position
            explosion_scale += 0.01
        else:
            helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
            helicopter.position.y = random.randint(0, HEIGHT_WIN - HEIGHT_Earth * 1.2)
            explosion_scale = 0.01
            shell.position = barrel.position + (0, -1)
            all_sprites.remove(explosion)
            all_sprites.remove(shell_box)
            h_scale = 0.35
            speedH = random.randint(-1, 1)
            blocking = 0
            expH = 0
    elif hit == 1:
        all_sprites.remove(bullet_box)
        all_sprites.remove(explosion)
        all_sprites.remove(explosion2)
        all_sprites.remove(shell_box)
        all_sprites.remove(shell2_box)
        all_sprites.remove(fire)
        all_sprites.remove(fire2)
        all_sprites.add(other_box, layer=2)
        player_box.add(tank1)
        all_sprites.add(player_box, layer=3)
        tank1.position.x = -tank_width * 5
        tank2.position.x = WIDTH_WIN * random.randint(2, 3)
        helicopter.position.x = WIDTH_WIN * random.randint(2, 3)
        helicopter.position.y = random.randint(0, HEIGHT_WIN - HEIGHT_Earth * 1.2)
        barrel.position = tank1.position + (25, -15)
        barrel2.position = tank2.position + (-21, -15)
        h_scale = 0.35
        speedH = random.randint(-1, 1)
        speedT = random.randint(0, 1)
        barrel2_angle = random.randint(2, 5)
        fire.velocity = (0, 0)
        fire.position = barrel.position
        shell2.velocity = (0, 0)
        shell2.position = barrel2.position
        fire2.velocity = (0, 0)
        fire2.position = barrel.position
        shell.velocity = (0, 0)
        shell.position = barrel.position + (0, -1)
        bullet.velocity = (0, 0)
        blocking = 0
        salvoT = 0
        salvoH = 0
        hit = 0

    """Стрельба вертолета"""
    if helicopter.position.x < 800:
        if salvoH == 0 and expH == 0 and expH1 == 0 and hit == 0:
            bullet_box.add(bullet)
            bullet.position.x = helicopter.position.x
            bullet.position.y = helicopter.position.y + h_height * h_scale / 3
            bullet_angle = h_angle - 180
            bullet.velocity = pg.math.Vector2(-25, 0).rotate(bullet_angle)
            salvoH = 1
            soundH.play()
        elif not bullet.rect.colliderect(helicopter.rect):
            all_sprites.add(bullet_box, layer=0)

    """Пули - collision"""
    if expH1 == 1 or bullet.position.x < 0 \
            or bullet.rect.colliderect(earth.rect) or bullet.rect.colliderect(earth_clone.rect):
        bullet.velocity = (0, 0)
        bullet.position.x = helicopter.position.x
        bullet.position.y = helicopter.position.y + h_height * h_scale / 3
        all_sprites.remove(bullet_box)
        expH1 = 0
        salvoH = 0
    elif pg.sprite.spritecollide(tank1, bullet_box, True):
        life -= 0.2
        expH1 = 1
        print('пули - Т1')

    """Залп танка_2"""
    if tank2.position.x < 700 and barrel2.position.x > 500:
        if salvoT == 0 and expT == 0 and expT1 == 0 and hit == 0:
            shell2_box.add(shell2)
            fire2.position = barrel2.position
            shell2.position = barrel2.position
            fire2_angle = barrel2_angle
            shell2_angle = barrel2_angle
            fire2.velocity = pg.math.Vector2(-15, 0).rotate(fire2_angle)
            shell2.velocity = pg.math.Vector2(-15, 0).rotate(shell2_angle)
            time_fire2 = 0
            salvoT = 1
            soundT2.play()
        elif not shell2.rect.colliderect(barrel2.rect):
            all_sprites.add(shell2_box, layer=0)
            all_sprites.add(fire2, layer=1)
            time_fire2 += 1
            if time_fire2 > 2:
                all_sprites.remove(fire2)

    """Снаряд_2 - collision"""
    if pg.sprite.spritecollide(tank1, shell2_box, True):
        expT1 = 1
        life -= 0.2
        explosion2.position = tank1.position
        print('снаряд2 - Т1')
    elif shell2.position.x < 1:
        explosion2.position = (0, shell2.position.y)
        expT1 = 1
    elif expT1 == 1 and hit == 0:
        all_sprites.add(explosion2, layer=4)
        if explosion2_scale <= 0.2:
            explosion2_scale += 0.01
        else:
            explosion2_scale = 0.01
            all_sprites.remove(explosion2)
            expT1 = 0
    if expT1 == 1:
        fire2.velocity = (0, 0)
        fire2.position = barrel2.position
        shell2.velocity = (0, 0)
        shell2.position = barrel2.position
        all_sprites.remove(shell2_box)
        salvoT = 0

    """Залп танка_1"""
    key = pg.key.get_pressed()
    if key[pg.K_SPACE] and blocking == 0 and tank1.position.x >= tank1_pos and hit == 0:
        shell_box.add(shell)
        fire.position = barrel.position
        shell.position = barrel.position + (0, -1)
        fire_angle = barrel_angle
        shell_angle = barrel_angle
        fire.velocity = pg.math.Vector2(20, 0).rotate(fire_angle)
        shell.velocity = pg.math.Vector2(20, 0).rotate(shell_angle)
        blocking = 1
        time_fire1 = 0
        soundT1.play()
    elif not fire.rect.colliderect(barrel.rect):
        all_sprites.add(shell_box, layer=0)
        all_sprites.add(fire, layer=1)
        time_fire1 += 1
        if time_fire1 > 2:
            all_sprites.remove(fire)
            fire.velocity = (0, 0)
            fire.position = barrel.position
    elif key[pg.K_m]:
        pg.mouse.set_visible(True)
        menu_points[0] = (330, 250, 'PAUSE', (250, 250, 30), (250, 30, 250), 0)
        game.menu()

    if life >= 10:
        life = 10
    elif int(life) <= 0:
        life = 0
        pg.mouse.set_visible(True)
        menu_points[0] = (330, 250, 'CLICK', (250, 250, 30), (250, 250, 30), 0)
        game.menu()

    screen.fill(BACKGROUND_COLOR)
    for i in stars:
        i.move_star()
        i.draw_star()

    info_string.fill((90, 0, 255))
    info_string.blit(text_font.render('Очки: ' + str(killed), 1, (255, 255, 255)), (10, 2))
    info_string.blit(text_font.render('Жизни: ' + str(int(life)), 1, (255, 255, 255)), (840, 2))
    screen.blit(info_string, (0, 0))

    gravitation()
    health.update()
    earth.update()
    earth_clone.update()
    tank1.update(images1, tank1_dx, tank1_dy, tank1_angle, tank1_scale)
    barrel.update(images2, barrel_dx, barrel_dy, barrel_angle, barrel_scale)
    helicopter.update(images3, h_dx, h_dy, h_angle, h_scale)
    tank2.update(images4, tank2_dx, tank2_dy, tank2_angle, tank2_scale)
    barrel2.update(images5, barrel2_dx, barrel2_dy, barrel2_angle, barrel2_scale)
    sight.update(images6, sight_dx, sight_dy, sight_angle, sight_scale)
    shell.update(images7, shell_dx, shell_dy, shell_angle, shell_scale)
    shell2.update(images7, shell2_dx, shell_dy, shell2_angle, shell_scale)
    explosion.update(images8, explosion_dx, explosion_dy, explosion_angle, explosion_scale)
    explosion2.update(images8, explosion_dx, explosion_dy, explosion_angle, explosion2_scale)
    fire.update(images9, fire_dx, fire_dy, fire_angle, fire_scale)
    fire2.update(images9, fire2_dx, fire_dy, fire2_angle, fire_scale)
    bullet.update(images10, bullet_dx, bullet_dy, bullet_angle, bullet_scale)
    all_sprites.draw(screen)
    pg.display.update()
