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
        self.text = ['Welcome to Adventure Unlocked','You are a person','This is a test','I am Colin.']

    def update(self,input):
        self.text.pop(0)
        self.text.append(input)

    def render_multi_line(self,x,y,fsize,screen,font):
        #lines = text.splitlines()
        for i, l in enumerate(self.text):
            #print('YES')
            txt_surf = font.render(l, 0, (255,0,0))
            txtRect = txt_surf.get_rect()
            txtRect.x = x
            txtRect.y = y + fsize*i
            screen.blit(txt_surf, txtRect)

def main():

    # pg.init()
    terminal = Terminal()
    pg.font.init()

    clock = pg.time.Clock()

    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 20
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')


    X = 640
    Y = 480

    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption('Adventure Unlocked')
    font = pg.font.SysFont(None, fontsize)
    text = ''
    active = False
    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
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

        screen.fill((255,255,255))

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
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
