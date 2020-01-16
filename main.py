import sys
import math
import random
import pygame

pygame.init()


class block(object):
    rows = 20
    width = 500

    def __init__(self, start, color=(0, 255, 0)):
        self.pos = start
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = block(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirx, c.diry)
        showScore(surface, len(snek.body))

    def reset(self, pos):
        self.head = block(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(block((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(block((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(block((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(block((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)


def drawGrid(w, r, surface):
    thickness = w // r

    x = 0
    y = 0
    for _ in range(r):
        x = x + thickness
        y = y + thickness

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, snek, snack
    surface.fill((0, 0, 0))
    snek.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def showScore(surface, score):
    font = pygame.font.Font("freesansbold.ttf", 32)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    surface.blit(score_text, (50, 300))
    pygame.display.update()


def randomSnack(rows, items):
    positions = items.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(surface):
    font = pygame.font.Font("freesansbold.ttf", 64)
    gameover_text = font.render("GAME OVER!", True, (255, 255, 255))
    surface.blit(gameover_text, (50, 200))
    pygame.display.update()


def main():
    global width, rows, snek, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snek = snake((255, 0, 0), (10, 10))
    snack = block(randomSnack(rows, snek), color=(255, 0, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snek.move(win)
        if snek.body[0].pos == snack.pos:
            snek.addCube()
            snack = block(randomSnack(rows, snek), color=(255, 0, 0))

        for x in range(len(snek.body)):
            if snek.body[x].pos in list(map(lambda z: z.pos, snek.body[x + 1:])):
                print("Score: ", len(snek.body))
                message_box(win)
                pygame.time.delay(2000)
                snek.reset((10, 10))
                break
        redrawWindow(win)


main()
