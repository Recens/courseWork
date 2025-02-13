import pygame as pg
from copy import deepcopy
from random import choice
from random import randrange
pg.init()
FPS = 120
W, H = 10, 20
BLOCK = 50
size = 1000, 1000

screen = pg.display.set_mode(size)
pg.display.set_caption("TETRIS")
font = pg.font.SysFont('cambria', 45)
background = pg.image.load('res/background.jpg').convert()
title_score = font.render("Score:", True, pg.Color("blue"))
title_record = font.render("Record:", True, pg.Color("green"))


class Parameter:
    # кординаты фигур на игровом поле:
    figure_xy = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], [(0, 0), (-1, 0), (1, 0), (0, -1)], [(0, 0), (1, -1), (0, -1), (0, 1)],
                 [(0, 0), (-1, -1), (0, -1), (0, 1)], [(0, 0), (-1, 0), (1, -1), (0, -1)], [(0, 0), (1, -1), (0, -1), (1, 0)],
                 [(0, 0), (1, 0), (0, -1), (-1, -1)]]
    # сложная конструкция генератора масива списка фигур экземпляра Rect:
    figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in pos] for pos in figure_xy]
    # Ещё один экземпляр для отрисовки каждой части фигуры
    figureRect = pg.Rect(0, 0, BLOCK - 2, BLOCK - 2)
    # переменые хранящие текущую и следущею фигуру
    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    score = 0
    lines = 0
    scores = {0: 0, 1: 10, 2: 30, 3: 60, 4: 100}
    # сложная конструкция генератора списка сетки(блоков):
    grid = [pg.Rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK) for x in range(W) for y in range(H)]
    # Выбор рандомного цвета в системе RGB с помощью lambda
    colors = lambda: (randrange(200, 255), randrange(200, 255), randrange(200, 255))
    # Цвет для текущеё фигуры и следуйщей
    color, next_color = colors(), colors()


class Collision:

    def __init__(self):
        self.parameter = Parameter()
        # Заполнение игрового поля нулями для проверки.
        self.flor = [[0 for i in range(W)] for j in range(H)]

    # логика границ для движений фигур
    def collision(self, i):

        if self.parameter.figure[i].x < 0 or self.parameter.figure[i].x > 9:
            return False
        elif self.parameter.figure[i].y > 19 or self.flor[self.parameter.figure[i].y][self.parameter.figure[i].x]:
            return False
        return True


class Function(Parameter):

    def __init__(self):
        self.collision = Collision()
        self.x = 0
        self.fall_count = 0
        self.fall_speed = 40
        self.fall_limit = 200
        self.rotate = False


    def move_rotation(self):
        center = Parameter.figure[0]
        figure_old = deepcopy(Parameter.figure)
        if self.rotate:
            for i in range(4):
                x = Parameter.figure[i].y - center.y
                y = Parameter.figure[i].x - center.x
                Parameter.figure[i].x = center.x - x
                Parameter.figure[i].y = center.y + y
                if not self.collision.collision(i):
                    Parameter.figure = deepcopy(figure_old)
                    break

    def del_line(self):
        coun = 0
        line = 19
        Parameter.lines = 0
        for row in range(19, - 1, - 1):
            count = 0
            for i in range(W):
                if self.collision.flor[row][i]:
                    count += 1
                self.collision.flor[line][i] = self.collision.flor[row][i]
            if count < W:
                line -= 1
                coun += 1
            elif coun == 5:
                self.fall_speed += 2
                coun = 0
            else:
                Parameter.lines += 1

    def score(self):
        Parameter.score += Parameter.scores[Parameter.lines]

    def moveX(self):
        figure_old = deepcopy(Parameter.figure)
        for i in range(4):
            Parameter.figure[i].x += self.x
            if not self.collision.collision(i):
                Parameter.figure = deepcopy(figure_old)
                break

    def move_down(self):
        self.fall_count += self.fall_speed
        if self.fall_count > self.fall_limit:
            self.fall_count = 0
            figure_old = deepcopy(Parameter.figure)
            for i in range(4):
                Parameter.figure[i].y += 1
                if not self.collision.collision(i):
                    for i in range(4):
                        self.collision.flor[figure_old[i].y][figure_old[i].x] = Parameter.color
                    Parameter.color = Parameter.next_color
                    Parameter.figure = Parameter.next_figure
                    Parameter.next_figure = deepcopy(choice(Parameter.figures))
                    Parameter.next_color = Parameter.colors()
                    self.fall_limit = 1500
                    break

    def flor(self):
        for y, row in enumerate(self.collision.flor): # перебор листа по индексу элемента и самого элемента
            for x, col in enumerate(row):
                if col:
                    Parameter.figureRect.x = x * BLOCK
                    Parameter.figureRect.y = y * BLOCK
                    pg.draw.rect(screen, col, Parameter.figureRect)

    def get_record(self):
        # исключение
        try:
            with open('Record') as f:
                return f.readline()

        except FileNotFoundError: # Файл или директория не существует.
            with open('Record', 'w') as f:
                f.write('0')

    def set_record(self):
        rec = max(int(self.get_record()), Parameter.score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def game_over(self):

        for i in range(W):
            if self.collision.flor[0][i]:
                self.set_record()
                self.collision.flor = [[0 for i in range(W)] for j in range(H)]
                self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
                Parameter.score = 0


class Draw:
    def __init__(self):
        self.func = Function()
        self.parameter = Parameter()


    def draw_figure(self):
        # Цикл отрисовки фигур
        for i in range(4):
            self.parameter.figureRect.x = self.parameter.figure[i].x * BLOCK
            self.parameter.figureRect.y = self.parameter.figure[i].y * BLOCK
            pg.draw.rect(screen, self.parameter.color, self.parameter.figureRect)

    def draw_next_figure(self):
        for i in range(4):
            self.parameter.figureRect.x = self.parameter.next_figure[i].x * BLOCK + 500
            self.parameter.figureRect.y = self.parameter.next_figure[i].y * BLOCK + 500
            pg.draw.rect(screen, self.parameter.next_color, self.parameter.figureRect)

    def Grid(self):
        for i in self.parameter.grid:
            pg.draw.rect(screen, (pg.Color('white')), i, 1)

    def draw_score(self):
        screen.blit(title_score, (550, 140))
        screen.blit(font.render(str(self.parameter.score), True, pg.Color('white')), (720, 140))

    def record(self):
        screen.blit(title_record, (550, 40))
        screen.blit(font.render(str(self.func.get_record()), True, pg.Color('yellow')), (740, 40))


class GameWindow:

    def __init__(self):
        self.func = Function()
        self.draw = Draw()

    def mainLoop(self):

        clock = pg.time.Clock()
        while True:

            screen.blit(background, (0, 0))

            self.func.x = 0
            self.func.rotate = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.func.x = -1
                    elif event.key == pg.K_RIGHT:
                        self.func.x = 1
                    elif event.key == pg.K_DOWN:
                        self.func.fall_limit = 10
                    elif event.key == pg.K_UP:
                        self.func.rotate = True

            self.draw.Grid()
            self.draw.draw_figure()
            self.draw.draw_next_figure()
            self.draw.draw_score()
            self.draw.record()
            self.func.moveX()
            self.func.score()
            self.func.move_down()
            self.func.flor()
            self.func.move_rotation()
            self.func.del_line()
            self.func.game_over()

            pg.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()


main()
