import pygame as pg
from copy import deepcopy
from random import choice

W, H = 10, 20
BLOCK = 50
game_res = W * BLOCK, H * BLOCK
FPS = 60
screen = pg.display.set_mode(game_res)


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
    figure = deepcopy(choice(figures))
    grid = [pg.Rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK) for x in range(W) for y in range(H)]

    def draw_figure(self):
        for i in range(4):
            self.figure_rect.x = self.figure[i].x * BLOCK
            self.figure_rect.y = self.figure[i].y * BLOCK
            pg.draw.rect(screen, pg.Color('white'), self.figure_rect)

    def Grid(self):
        [pg.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in self.grid]


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



class Move():

    def __init__(self):
        self.block = Block()
        self.manager = Manager()
        self.x = 0
        self.fall_count = 0
        self.fall_speed = 60
        self.fall_limit = 200
        self.rotate = False

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
        for row in range(H - 1, - 1, - 1):
            count = 0
            for i in range(W):
                if self.manager.flor[row][i]:
                    count += 1
                self.manager.flor[line][i] = self.manager.flor[row][i]
            if count < W:
                line -= 1

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
                        self.manager.flor[figure_old[i].y][figure_old[i].x] = pg.Color('White')
                    Block.figure = deepcopy(choice(Block.figures))
                    self.fall_limit = 2000
                    break

    def draw_flor(self):
        for y, row in enumerate(self.manager.flor):
            for x, col in enumerate(row):
                if col:
                    self.block.figure_rect.x = x * BLOCK
                    self.block.figure_rect.y = y * BLOCK
                    pg.draw.rect(screen, col, self.block.figure_rect)





class GameWindow:

    def __init__(self):
        self.block = Block()
        self.move = Move()
        self.manager = Manager()


    def mainLoop(self):
        pg.init()
        clock = pg.time.Clock()
        while True:

            screen.fill(pg.Color('black'))
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
            self.move.moveX()
            self.move.move_down()
            self.move.draw_flor()
            self.move.move_rotation()
            self.move.del_line()

            pg.display.flip()
            clock.tick(FPS)



def main():
    window = GameWindow()
    window.mainLoop()


main()
