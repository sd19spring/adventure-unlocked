import pygame as pg
import random
import time
import os
import theENGINE as engine
import generate
from menu import start_menu, help_menu, game_end
from generation.world import ROOMS

class Terminal():
    """
    Stores the current text to be displayed in the game
    """
    def __init__(self, rooms, notes, decisions):
        self.mansion = self.mansion_name()
        self.text = ['Welcome to Adventure Unlocked','You are a wandering the ' + self.mansion,'Your objective is unclear',
        'Your memories are hazy...','How did you end up here...','Maybe taking a look around will help you remember.',
        'Total rooms: ' + str(rooms), 'Notes left to uncover: ' + str(notes), 'You have ' + str(decisions) + ' decisions to piece together the story.',
        '[Try using commands such as "go _", "pick up _", or "help"]',
        '-------------------------------------------------------------------------']

    def update(self,input):
        for line in input:
            self.text.append(line)
            if len(self.text) > 20:
                self.text.pop(0)

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
    # Generate game
    r = random.randint(5, len(ROOMS))
    decisions = r * 7

    generate.mkdir('./content')
    generate.generate_notes()
    generate.write_attributes()
    generate.generate_world(r)

    # Set window position
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Initializing pygame, fonts, and the terminal class
    pg.init()

    #Screen size
    X = 1280
    Y = 720

    # Game window
    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption('Adventure Unlocked')

    # Menu
    if not start_menu(screen):
        pg.quit()
        return

    terminal = Terminal(r, 15, decisions)
    game, res = engine.startGame()
    terminal.update(res)
    pg.font.init()
    clock = pg.time.Clock()

    #Font colors and size
    color = (0,0,255)
    txtcolor = (0,0,0)
    fontsize = 30

    #Definiting input box
    input_box = pg.Rect(20, Y-60, 300, fontsize*1.5)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')


    #Trying to get custom fonts to work
    try:
        font = pg.font.Font("Fonts/DeterminationMonoWeb.ttf",fontsize)
    except RuntimeError:
        font = pg.font.SysFont(None, fontsize)

    #Intializing text input and setting game loop to be running
    text = ''
    active = False
    running = True

    # Step counter
    decision = 0
    # Note checker
    notes = {}

    while running:
        # Game over state
        if decision >= decisions:
            game_end(screen, 'Someone destroyed the notes before you could solve the mystery')
            return
        else:
            #----- Checking for quit sequence and taking in user input -----
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    return
                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN and active:
                    if event.key == pg.K_RETURN:
                        if len(notes) >= 15: # Game finish state
                            game_end(screen, 'You have unraveled the story, but was too late to stop the murder.')
                            return
                        terminal.update(['> ' + text ])
                        terminal.update([''])
                        terminal.update(game.handleInput(text, notes))
                        text = ''
                        decision += 1

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

            #----- Render decisions and notes left -------
            d_surf = font.render('Decisions made: ' + str(decision) + '/' + str(decisions), True, (255, 0, 0))
            screen.blit(d_surf, (X - d_surf.get_width() - 50, 20))
            d_surf = font.render('Notes left: ' + str(15 - len(notes)) + '/15', True, (255, 0, 0))
            screen.blit(d_surf, (X - d_surf.get_width() - 50, 50))

            pg.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    #Run game
    main()
