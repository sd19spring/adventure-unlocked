"""
Secondary test script to work on a different approach to outputting text
"""

import pygame as pg
import random
import time
import os
import theENGINE as engine

class Terminal():
    """
    Stores the current text to be displayed in the game
    """

    def __init__(self):
        self.mansion = self.mansion_name()
        self.text = ['Welcome to Adventure Unlocked','You are a wandering the ' + self.mansion,'Your objective is unclear',
        'Your memories are hazy...','How did you end up here...','Maybe taking a look around will help you remember.',
        '-------------------------------------------------------------------------',
        ' ',' ',' ',' ',' ',' ']

    def update(self,input):
        for line in input:
            self.text.pop(0)
            self.text.append(line)

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

        mansion_names = ['Bayview Manor','Humbleblossom Residence','Riverswood Estate','Ivory Manor','Green Meadow Chateau','Beauhold Mansion','Rosenphrey Estate',
        'Davenlyn Residence','Rottlyn Chateau','Shanders Residence','Elm Estate','Whisperwind Residence','Jade River Estate','Beaverlake Estate','Humble Hill Chateau','Ruxstrong Manor','Monstrong Residence',
        'Gregford Residence','Palbrook Manor','Pickdel Estate','Evergreen Valley Residence','Crystal Lake Chateau','Evergreen Mansion','Whitland Chateau','Honeydrop Residence','Stratkett Manor',
        'Pitgor Residence','Meastrong Estate','Chalger Manor','Woodmier Manor','Ivylane Manor','Grapevine Manor','Woodrest Manor','Hazelbend Mansion','Belcourt Residence','Gallotero Estate','Spenperd Estate',
        'Harringsen Mansion','Palding Residence','Shearcomb Chateau','Graceview Chateau','Stonewill Mansion','Poinsetta Manor',"Raven's Nest Residence",'Dewberry Residence','Fielgett Manor']

        return mansion_names[random.randint(0,len(mansion_names)-1)]

def main():

    # Initializing pygame, fonts, and the terminal class
    pg.init()

    terminal = Terminal()
    game,startRoom = engine.startGame()
    terminal.update([startRoom])
    pg.font.init()
    clock = pg.time.Clock()

    #Font colors and size
    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 30

    #Screen size
    X = 640
    Y = 480

    #Definiting input box
    input_box = pg.Rect(20, Y-60, 300, fontsize*1.5)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')

    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption('Adventure Unlocked')


    #Trying to get custom fonts to work
    try:
        font = pg.font.Font("Fonts/DeterminationMonoWeb.ttf",fontsize)
    except RuntimeError:
        font = pg.font.SysFont(None, fontsize)

    #Intializing text input and setting game loop to be running
    text = ''
    active = False
    running = True

    while running:

        #----- Checking for quit sequence and taking in user input -----
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
                        terminal.update([text])
                        terminal.update(engine.handleInput(game, text))
                        text = ''

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        #----- Fill screen black ------
        screen.fill((0,0,0))

        #----- Rendering the text box current state -----
        txt_surface = font.render(text, True, color)
        width = max(X-40, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)

        #----- Rendering the text for the game output -----
        terminal.render_multi_line(24,24,fontsize,screen,font)

        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    #Run game
    main()