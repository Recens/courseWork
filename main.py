import pygame as pg
from copy import deepcopy
from random import choice

W, H = 10, 20
BLOCK = 50
game_res = W * BLOCK, H * BLOCK
FPS = 60

screen = pg.display.set_mode(game_res)
grid = [pg.Rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK) for x in range(W) for y in range(H)]


class Block:



    def figures(self):
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
        for i in range(4):
            figure_rect.x = figure[i].x * BLOCK
            figure_rect.y = figure[i].y * BLOCK
            pg.draw.rect(screen, pg.Color('white'), figure_rect)

    def Grid(self):
        [pg.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]


class GameWindow:

    def __init__(self):
        self.manager = Block()

    def mainLoop(self):
        pg.init()
        clock = pg.time.Clock()
        while True:

            screen.fill(pg.Color('black'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()

            self.manager.Grid()
            self.manager.figures()

            pg.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()
main()

"""    
pg.init()


grid = [pg.Rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK) for x in range(W) for y in range(H)]

figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in pos] for pos in figure_pos]
figure_rect = pg.Rect(1, 1, BLOCK - 2, BLOCK - 2)
figure = deepcopy(choice(figures))
fall_count, fall_speed, fall_limit = 0, 60, 200

flor = [[0 for i in range(W)]for j in range(H)]
def check():
    if figure[i].x < 0 or figure[i].x > W-1:
        return False
    elif figure[i].y > H - 1 or flor[figure[i].y][figure[i].x]:
        return  False
    return True


while True:
    yx = 0
    rotate = False
    game_cs.fill(pg.Color('black'))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                yx = -1
            elif event.key == pg.K_RIGHT:
                yx = 1
            elif event.key == pg.K_DOWN:
                fall_limit = 10
            elif event.key == pg.K_UP:
                rotate = True
    # rotation

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check():
                figure = deepcopy(figure_old)
                break
    # delete line
    line = H - 1
    for row in range(H - 1, - 1, - 1):
        count = 0
        for i in range(W):
            if flor[row][i]:
                count += 1
            flor[line][i] = flor[row][i]
        if count < W:
            line -= 1


    # move left or right
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += yx
        if not check():
            figure = deepcopy(figure_old)
            break
    # move down
    fall_count += fall_speed
    if fall_count > fall_limit:
        fall_count = 0
        figure_old = deepcopy(figure)
        for i in range (4):
            figure[i].y += 1
            if not check():
                for i in range(4):
                    flor[figure_old[i].y][figure_old[i].x] = pg.Color('White')
                figure = deepcopy(choice(figures))
                fall_limit = 2000
                break

    # draw grid
    [pg.draw.rect(game_cs, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * BLOCK
        figure_rect.y = figure[i].y * BLOCK
        pg.draw.rect(game_cs, pg.Color('white'), figure_rect)
    # draw flor
    for y, row in enumerate(flor):
        for x, col in enumerate(row):
            if col:
                figure_rect.x = x * BLOCK
                figure_rect.y = y * BLOCK
                pg.draw.rect(game_cs, col, figure_rect)

    
"""
