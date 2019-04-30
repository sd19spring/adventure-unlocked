import pygame as pg
import os

#Sets the width and height of the screen
WIDTH = 640
HEIGHT = 480

#Initializes the screen - Careful: all pg commands must come after the init
pg.init()
clock = pg.time.Clock()

#Sets the screen note: must be after pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

class Board(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.image.fill((13,13,13))
        self.image.set_colorkey((13,13,13))
        self.rect = self.image.get_rect()
        self.font = pg.font.SysFont("monospace", 24)

    def add(self, letter, pos):
        s = self.font.render(letter, 1, (100, 255, 0))
        self.image.blit(s, pos)

class Cursor(pg.sprite.Sprite):
    def __init__(self, board):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 20))
        self.image.fill((0,255,0))
        self.text_height = 22
        self.text_width = 14
        self.rect = self.image.get_rect(topleft=(self.text_width, self.text_height))
        self.board = board
        self.text = ''
        self.cooldown = 0
        self.cooldowns = {'.': 12,
                        '[': 18,
                        ']': 18,
                        ' ': 5,
                        '\n': 30}

    def write(self, text):
        self.text = list(text)

    def update(self):
        if not self.cooldown and self.text:
            letter = self.text.pop(0)
            if letter == '\n':
                self.rect.move_ip((0, self.text_height))
                self.rect.x = self.text_width
            else:
                self.board.add(letter, self.rect.topleft)
                self.rect.move_ip((self.text_width, 0))
            self.cooldown = self.cooldowns.get(letter, 8)

        if self.cooldown:
            self.cooldown -= 1

    def print(self):
        print(self.text)

all_sprites = pg.sprite.Group()
board = Board()
cursor = Cursor(board)
all_sprites.add(cursor, board)


text = """Hello traveler.
Welcome to Adventure Unlocked.
You are about to start on the quest of
a lifetime. The events that unfold will
be uniquely generated for you.
"""

cursor.write(text)
cursor.print()

#Main loop
running = True
while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pg.display.flip()
    #clock.tick(60)
