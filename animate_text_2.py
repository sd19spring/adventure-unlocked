"""
Secondary test script to work on a different approach to outputting text
"""

import pygame as pg
import time

class Terminal():
    """
    Stores the current text to be displayed in the game
    """

    def __init__(self):
        self.text = ['Welcome to Adventure Unlocked','You are a person','This is a test','I am Colin.']

    def update(self,input):
        self.text.pop(0)
        self.text.append(input)

    def render_multi_line(self,x,y,fsize,screen,font):
        #lines = text.splitlines()
        for i, l in enumerate(self.text):
            print('YES')
            time.sleep(1)
            screen.blit(font.render(l, 0, (255,0,0)), (x, y + fsize*i))


def main():

    terminal = Terminal()
    pg.font.init()

    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 20

    X = 640
    Y = 480

    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption('Adventure Unlocked')
    font = pg.font.SysFont(None, fontsize)

    running = True

    while running:
        screen.fill((255,255,255))
        print(X,Y,fontsize,screen)
        terminal.render_multi_line(terminal.text,X,Y,fontsize,screen,font)
        terminal.update(input("Update list:"))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        pg.display.update()
        pg.display.flip()

if __name__ == '__main__':
    main()
