"""
Secondary test script to work on a different approach to outputting text
"""

import pygame as pg
import time

pg.init

class Terminal():
    """
    Stores the current text to be displayed in the game
    """

    def __init__(self):
        self.mansion = self.mansion_name()
        self.text = ['Welcome to Adventure Unlocked','You are a wandering the ' + self.mansion +' Mansion','Your objective is unclear',
        'Your memories are hazy...','How did you end up here...','Maybe taking a look around will help you remember.','-------------------------------------------------------------------------',' ',' ',' ',' ',' ',' ']

    def update(self,input):
        self.text.pop(0)
        self.text.append(input)

    def render_multi_line(self,x,y,fsize,screen,font):
        #lines = text.splitlines()
        for i, l in enumerate(self.text):
            #print('YES')
            txt_surf = font.render(l, 0, (0,255,0))
            txtRect = txt_surf.get_rect()
            txtRect.x = x
            txtRect.y = y + fsize*i
            screen.blit(txt_surf, txtRect)

    def mansion_name(self):

        return '[Default Name]'

def main():

    # pg.init()
    terminal = Terminal()
    pg.font.init()

    clock = pg.time.Clock()

    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 30

    X = 640
    Y = 480

    input_box = pg.Rect(20, Y-60, 300, fontsize*1.5)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')

    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption('Adventure Unlocked')
    font = pg.font.SysFont(None, fontsize)
    text = ''
    active = False
    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        terminal.update(text)
                        text = ''

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0,0,0))

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(X-40, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)


        # screen.fill((255,255,255))
        #print(X,Y,fontsize,screen)
        terminal.render_multi_line(24,24,fontsize,screen,font)
        #terminal.update(input("Update list:"))

#        pg.display.update()
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
