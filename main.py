import pygame as pg
from copy import deepcopy
from random import choice, randrange
pg.init()
W, H = 10, 20
BLOCK = 50
game_res = W * BLOCK, H * BLOCK
res = 900, 1000
FPS = 60
screen = pg.display.set_mode(res)
pg.display.set_caption("TETRIS")
font = pg.font.SysFont('cambria', 45)


class Block:

    figure_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                  [(0, 0), (-1, 0), (1, 0), (0, -1)],
                  [(0, 0), (1, -1), (0, -1), (0, 1)],
                  [(0, 0), (-1, -1), (0, -1), (0, 1)],
                  [(0, 0), (-1, 0), (1, -1), (0, -1)],
                  [(0, 0), (1, -1), (0, -1), (1, 0)],
                  [(0, 0), (1, 0), (0, -1), (-1, -1)]]
    figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in pos] for pos in figure_pos]
    figure_rect = pg.Rect(1, 1, BLOCK - 2, BLOCK - 2)
    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    score = 0
    lines = 0
    scores = {0: 0, 1: 100, 2: 300, 3: 600, 4: 1000}
    title_score = font.render(("score:"), True, pg.Color("blue"))
    title_record = font.render(("Record:"), True, pg.Color("green"))

    grid = [pg.Rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK) for x in range(W) for y in range(H)]
    colors = lambda: (randrange(35, 256), randrange(35, 256), randrange(35, 256))
    color, next_color = colors(), colors()

    def draw_figure(self):
        for i in range(4):
            self.figure_rect.x = self.figure[i].x * BLOCK
            self.figure_rect.y = self.figure[i].y * BLOCK
            pg.draw.rect(screen, self.color, self.figure_rect)

    def draw_next_figure(self):
        for i in range(4):
            self.figure_rect.x = self.next_figure[i].x * BLOCK + 400
            self.figure_rect.y = self.next_figure[i].y * BLOCK + 500
            pg.draw.rect(screen, self.next_color, self.figure_rect)

    def Grid(self):
        [pg.draw.rect(screen, (pg.Color('white')), i_rect, 1) for i_rect in self.grid]


class Manager:

    def __init__(self):
        self.block = Block()
        self.flor = [[0 for i in range(W)] for j in range(H)]

    def check(self, i):

        if self.block.figure[i].x < 0 or self.block.figure[i].x > W - 1:
            return False
        elif self.block.figure[i].y > H - 1 or self.flor[self.block.figure[i].y][self.block.figure[i].x]:
            return False
        return True


class Move(Block):

    def __init__(self):
        self.manager = Manager()
        self.x = 0
        self.fall_count = 0
        self.fall_speed = 60
        self.fall_limit = 200
        self.rotate = False
        self.record = 0

    def move_rotation(self):
        center = Block.figure[0]
        figure_old = deepcopy(Block.figure)
        if self.rotate:
            for i in range(4):
                x = Block.figure[i].y - center.y
                y = Block.figure[i].x - center.x
                Block.figure[i].x = center.x - x
                Block.figure[i].y = center.y + y
                if not self.manager.check(i):
                    Block.figure = deepcopy(figure_old)
                    break

    def del_line(self):
        line = H - 1
        Block.lines = 0
        for row in range(H - 1, - 1, - 1):
            count = 0
            for i in range(W):
                if self.manager.flor[row][i]:
                    count += 1
                self.manager.flor[line][i] = self.manager.flor[row][i]
            if count < W:
                line -= 1
            else:
                self.fall_limit += 5
                Block.lines += 1

    def score(self):
        Block.score += Block.scores[Block.lines]

    def moveX(self):
        figure_old = deepcopy(Block.figure)
        for i in range(4):
            Block.figure[i].x += self.x
            if not self.manager.check(i):
                Block.figure = deepcopy(figure_old)
                break

    def move_down(self):
        self.fall_count += self.fall_speed
        if self.fall_count > self.fall_limit:
            self.fall_count = 0
            figure_old = deepcopy(Block.figure)
            for i in range(4):
                Block.figure[i].y += 1
                if not self.manager.check(i):
                    for i in range(4):
                        self.manager.flor[figure_old[i].y][figure_old[i].x] = Block.color
                    Block.color = Block.next_color
                    Block.figure = Block.next_figure
                    Block.next_figure = deepcopy(choice(Block.figures))
                    Block.next_color = Block.colors()
                    self.fall_limit = 2000
                    break

    def draw_flor(self):
        for y, row in enumerate(self.manager.flor):
            for x, col in enumerate(row):
                if col:
                    Block.figure_rect.x = x * BLOCK
                    Block.figure_rect.y = y * BLOCK
                    pg.draw.rect(screen, col, Block.figure_rect)

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self):
        rec = max(int(self.record), Block.score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def game_over(self):

        for i in range(W):
            if self.manager.flor[0][i]:
                self.set_record()
                self.manager.flor = [[0 for i in range(W)] for i in range(H)]
                self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
                Block.score = 0


class Draw:
    def __init__(self):
        self.move = Move()
        self.block = Block()
        self.manager = Manager()

    def draw_score(self):
        screen.blit(self.block.title_score, (550, 140))
        screen.blit(font.render(str(self.block.score), True, pg.Color('white')), (720, 140))

    def record(self):
        screen.blit(self.block.title_record, (550, 40))
        screen.blit(font.render(str(self.move.get_record()), True, pg.Color('yellow')), (740, 40))


class GameWindow:

    def __init__(self):
        self.block = Block()
        self.move = Move()
        self.manager = Manager()
        self.draw = Draw()

    def mainLoop(self):
        pg.init()
        clock = pg.time.Clock()
        while True:

            screen.fill(pg.Color('grey'))

            self.move.x = 0
            self.move.rotate = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.move.x = -1
                    elif event.key == pg.K_RIGHT:
                        self.move.x = 1
                    elif event.key == pg.K_DOWN:
                        self.move.fall_limit = 10
                    elif event.key == pg.K_UP:
                        self.move.rotate = True

            self.block.Grid()
            self.block.draw_figure()
            self.block.draw_next_figure()
            self.draw.draw_score()
            self.draw.record()
            self.move.moveX()
            self.move.score()
            self.move.move_down()
            self.move.draw_flor()
            self.move.move_rotation()
            self.move.del_line()
            self.move.game_over()

            pg.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()


main()
