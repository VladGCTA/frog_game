import pygame as pg
from os import path
from random import randrange


""""""
images_dir = path.join(path.dirname(__file__), "images")   # путь к изображениям, для верного отображения на разных ОС
fonts_dir = path.join(path.dirname(__file__), "fonts", "Monoid-Regular.ttf")   # путь к папке со шрифтами


""""""

pg.init()

""""""
width = 910   # ширина
height = 540   # высота
display_size = (width, height)   # площадь экрана
display = pg.display.set_mode(display_size)   # дисплей
current_display = pg.display.set_mode(display_size)
pg.display.set_caption("Frog game")   # название
display_color = (190, 215, 200)   # цвет бэкграунда
fps = 60   # фпс
game_state = "open"   # состояние игры
clock = pg.time.Clock()   # часы для менеджмента фпс
all_sprites = pg.sprite.Group()   # группа спрайтов - все спрайты
score = 0
speedx = 9
speedy = 9
""""""

"""Меню"""
menu_display = pg.display.set_mode((width, height))
menu_background = pg.image.load(path.join(images_dir, "menu_back.png"))


font_monoid = pg.font.Font(fonts_dir, 36)
text_color = (255, 255, 255)
text_play = font_monoid.render("Play", True, text_color)
text_play_x, text_play_y = text_play.get_size()
text_speedup = font_monoid.render("Speed up", True, text_color)
text_speedup_x, text_speedup_y = text_speedup.get_size()
text_exit = font_monoid.render("Exit", True, text_color)
text_exit_x, text_exit_y = text_exit.get_size()

buttons_color = (23, 107, 135)
play_button_color = buttons_color
speedup_button_color = buttons_color
exit_button_color = buttons_color

menu_speedup = pg.surface.Surface((250, 60))
speedup_width = menu_speedup.get_width()
speedup_height = menu_speedup.get_height()


menu_play = pg.surface.Surface((250, 60))
play_width = menu_play.get_width()
play_height = menu_play.get_height()

menu_exit = pg.surface.Surface((250, 60))
exit_width = menu_exit.get_width()
exit_height = menu_exit.get_height()

score_bar = pg.image.load(path.join(images_dir, "score.png")).convert_alpha()   # спрайт подложки счёта
score_bar_width = score_bar.get_width()
score_bar_height = score_bar.get_height()
""""""

""""""
background = pg.image.load(path.join(images_dir, "background.png")).convert_alpha()   # бэкграунд
player_img = pg.image.load(path.join(images_dir, "frog.png")).convert_alpha()   # спрайт игрока с альфаканалом
fly_img = pg.image.load(path.join(images_dir, "fly.png")).convert_alpha()   # спрайт моба с альфаканалом
""""""

""""""
max_speed = 16
cost = 40

text_cost = font_monoid.render("Cost: " + str(cost), True, text_color)
text_costx, text_costy = text_cost.get_size()
""""""


class Player(pg.sprite.Sprite):   # класс игрока
    def __init__(self):   # инициализация атрибутов игрока
        pg.sprite.Sprite.__init__(self)   # инициализация родительского класса pygame спрайтов
        self.image = player_img   # атрибут изображение (спрайт игрока)
        self.rect = self.image.get_rect()   # атрибут прямоугольника (колизия) поверх спрайта игрока
        self.rect.centerx = width / 2   # атрибут центра спрайта по горизонтали в точке ширина / 2
        self.rect.bottom = height - 10   # атрибут нижней части спрайта = высота - 10 (на 10 пикселей выше нижнего края)
        self.speedx = 0
        self.speedy = 0

    def move(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speedx = -speedx
        if keystate[pg.K_d]:
            self.speedx = speedx
        self.rect.x += self.speedx
        if keystate[pg.K_w]:
            self.speedy = -speedy
        if keystate[pg.K_s]:
            self.speedy = speedy
        self.rect.y += self.speedy

        if self.rect.right > width:   # если правый край дальше ширины
            self.rect.right = width   # правый край = координате ширины
        if self.rect.left < 0:   # если левый край меньше 0 координаты ширины
            self.rect.left = 0   # координата левого края = 0

        if self.rect.top < 0:   # если верхний край ниже 0 координаты
            self.rect.top = 0   # верхний край = 0
        if self.rect.bottom > height:   # если нижний край ниже макс y координаты
            self.rect.bottom = height   # координата нижнего края = макс координате y


class Mobs(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = fly_img
        self.rect = self.image.get_rect()
        self.rect.x = randrange(width - self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.speedy = randrange(5, 8)
        self.speedx = randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left <= 0:   # условие отражения от левой стенки
            self.speedx = -self.speedx
        if self.rect.right >= width:   # условие отражения от правой стенки
            self.speedx = -self.speedx

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:   # условия переспавна
            self.rect.x = randrange(height - self.rect.width)   # место спавна моба по горизонтали
            self.rect.y = randrange(-100, -40)   # место спавна моба по вертикали
            self.speedy = randrange(4, 10)   # скорость по вертикали
            self.speedx = randrange(-8, 8)   # скорость по горизонтали (отвечает за угол движения)

    def eated(self):
        global fly
        global score
        if pg.sprite.collide_rect(self, player):
            self.kill()
            if score < 10 ** 7:
                score += 1
            fly = Mobs()
            all_sprites.add(fly)


player = Player()   # создание экземпляра класса
fly = Mobs()
all_sprites.add(player)   # добавляем экземпляр класса (собственно спрайт игрока) в группу спрайтов
all_sprites.add(fly)


def start_game():   # функция старта игры
    """тело игры"""
    global game_state, speedx, speedy, score, current_display
    play_rect = menu_play.get_rect(topleft=((width - play_width) // 2, 100))
    speedup_rectangle = menu_speedup.get_rect(topleft=((width - speedup_width) // 2, 230))
    exit_rect = menu_exit.get_rect(topleft=((width - exit_width) // 2, 360))

    global text_color
    global play_button_color, speedup_button_color, exit_button_color, cost

    while True:
        # цикл игры
        text_score = font_monoid.render("Score: " + str(score), True, (255, 255, 255))
        text_cost = font_monoid.render("Cost: " + str(cost), True, text_color)
        score_width = text_score.get_width()

        for event in pg.event.get():   # обработка событий
            if event.type == pg.QUIT:   # выход
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg. K_SPACE and game_state == "open":
                    game_state = "game"
                elif event.key == pg.K_ESCAPE:
                    if game_state == "menu":
                        game_state = "game"
                    elif game_state == "game":
                        game_state = "menu"
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        play_button_color = buttons_color
                        game_state = "game"
                    if speedup_rectangle.collidepoint(event.pos):
                        if speedx < max_speed and speedy < max_speed and score >= cost:
                            score -= cost
                            cost += 10
                            speedx += 1
                            speedy += 1
                        elif speedx and speedy >= max_speed:
                            cost = "Solded"
                    if exit_rect.collidepoint(event.pos):
                        exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_rect.collidepoint(event.pos) and pg.mouse.get_pressed():
                        play_button_color = (15, 90, 120)
                    if speedup_rectangle.collidepoint(event.pos) and pg.mouse.get_pressed():
                        speedup_button_color = (15, 90, 120)
                    if exit_rect.collidepoint(event.pos) and pg.mouse.get_pressed():
                        exit_button_color = (15, 90, 120)

            elif event.type == pg.MOUSEBUTTONUP:
                play_button_color = buttons_color
                speedup_button_color = buttons_color
                exit_button_color = buttons_color

        display.blit(background, (0, 0))  # заливка бэкграунда

        all_sprites.draw(display)   # отрисовка всех спрайтов

        if game_state == "game":   # если game_state - игра, то игровой режим (если нет, то меню)
            all_sprites.update()   # обновление всех спрайтов
            display.blit(text_score, ((width - score_width) // 2, 10))
            player.move()   # метод класса игрока (движение)
            fly.eated()

        elif game_state == "menu" or "open":
            display.blit(menu_background, (0, 0))
            menu_display.blit(text_score, ((width - score_width) // 2, 10))

            menu_display.blit(menu_play, ((width - play_width) // 2, 100))
            menu_play.fill(play_button_color)
            menu_play.blit(text_play, ((play_width - text_play_x) // 2,
                                       (play_height - text_play_y) // 2))

            current_display.blit(menu_speedup, ((width - speedup_width) // 2, 230))
            menu_speedup.fill(speedup_button_color)
            menu_speedup.blit(text_speedup, ((speedup_width - text_speedup_x) // 2,
                                             (speedup_height - text_speedup_y) // 2))
            menu_display.blit(text_cost, ((width - text_costx - 20) // 2, 170))

            current_display.blit(menu_exit, ((width - exit_width) // 2, 360))
            menu_exit.fill(exit_button_color)
            menu_exit.blit(text_exit, ((exit_width - text_exit_x) // 2,
                                       (exit_height - text_exit_y) // 2))

        pg.display.update()   # обновление экрана
        clock.tick(fps)   # лок фпс


start_game()   # старт игры
