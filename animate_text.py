"""
Custom font implementation, text input, and text animation script in pygame
"""

import pygame as pg
import os

def customfont(name,size):
    """Importing custom fonts into pygame"""

    path = os.path.dirname(os.path.abspath(name))
    #print(type(path))
    path = '/Users/colintakeda/final-project-adventure-unlocked/Fonts'
    font = pg.font.Font(os.path.join(path,name), size)
    return font

def checkfonts():
    """Checking font lists loaded in pygame"""

    print(pg.font.get_fonts())

def commandwindow():
    """Creating terminal interface for player"""

    pg.font.init()
    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 32

    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    txt_output = pg.Rect((40 ,40),(500,200))
    font = pg.font.SysFont(None, fontsize)

    output = ["This","is","a","test."]
    text = "TEST TEST TEST TEST TEST TEST TEST TEST TEST"

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        screen.fill((255, 0, 0))
        txt_surface = font.render(text, True, txtcolor)
        screen.blit(txt_surface, (txt_output.x+40, txt_output.y+40))
        pg.draw.rect(screen, color, txt_output, 50)
        pg.display.flip()

def inputtext():
    """Input text bubble that uses custom font choice"""

    pg.font.init()
    screen = pg.display.set_mode((640, 480))

    try:
        font = customfont('DeterminationMonoWeb.ttf',32)
    except RuntimeError:
        print("Still can't search in stream")
        font = pg.font.SysFont(None, 32)


    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')

    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
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
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        #pg.display.flip()
        clock.tick(30)

if __name__ == '__main__':

    pg.init()
    #inputtext()
    commandwindow()
    pg.quit()
