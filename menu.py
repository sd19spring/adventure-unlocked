import pygame
from pygame.locals import *
import os

screen_width = 1280
screen_height = 720

def start_menu(win):
    """
    Renders the start menu for the game. Can choose to start game, get help info, or quit
    """
    # Colors
    ACTIVE_COLOR = (255, 0 ,0)
    TEXT_COLOR = (255, 255, 255)

    # Keeps track of which menu item is currently active
    menu_items = [ACTIVE_COLOR, TEXT_COLOR, TEXT_COLOR]
    item_pos = 0
    while 1:
        win.fill((0, 0, 0))
        # Background image
        img = pygame.image.load("mansion.png")
        win.blit(img, (screen_width - img.get_width() - 10, 0))

        # Title 
        title_font = pygame.font.SysFont('helvetica', 100)
        title = title_font.render('Adventure Unlocked', 1, TEXT_COLOR)
        win.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - 100))
        
        # Menu items
        item_font = pygame.font.SysFont('helvetica', 40)
        start = item_font.render('Start', 1, menu_items[0])
        win.blit(start, (screen_width / 2 - start.get_width() / 2, screen_height / 2 + 50))
        help = item_font.render('Help', 1, menu_items[1])
        win.blit(help, (screen_width / 2 - help.get_width() / 2, screen_height / 2 + 120))
        quit = item_font.render('Quit', 1, menu_items[2])
        win.blit(quit, (screen_width / 2 - quit.get_width() / 2, screen_height / 2 + 190))
        
        # Handle events for selecting and choosing menu items
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYUP:
                if event.key == K_UP and item_pos - 1 >= 0:
                    menu_items[item_pos] = TEXT_COLOR
                    item_pos -= 1
                    menu_items[item_pos] = ACTIVE_COLOR
                if event.key == K_DOWN and item_pos + 1 < len(menu_items):
                    menu_items[item_pos] = TEXT_COLOR
                    item_pos += 1
                    menu_items[item_pos] = ACTIVE_COLOR
                if event.key == K_RETURN:
                    if item_pos == 0:
                        return True
                    elif item_pos == 1:
                        # Pass along quit
                        if not help_menu(win):
                            return False
                    else:
                        return False
        
        pygame.display.update()

def help_menu(win):
    """
    Renders the help menu that displays game info
    """

    # Colors
    ACTIVE_COLOR = (255, 0 ,0)

    while 1:
        win.fill((0, 0, 0))

        # Title 
        title_font = pygame.font.SysFont('helvetica', 75)
        title = title_font.render('Help', 1, (255, 255, 255))
        win.blit(title, (screen_width / 2 - title.get_width() / 2, 60))
        
        # Text
        item_font = pygame.font.SysFont('helvetica', 30)
        text = item_font.render('This is a generative text based adventure game. What this means is that while the story', 1, (255, 255, 255))
        win.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - 100))
        text = item_font.render('follows an overarching plot, many of the game elements are generated, like the rooms, items,', 1, (255, 255, 255))
        win.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - 50))
        text = item_font.render('and music. Interact with the world using the text box in the bottom by typing in commands,', 1, (255, 255, 255))
        win.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2))
        text = item_font.render('and explore the adventure that awaits.', 1, (255, 255, 255))
        win.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 + 50))

        font = pygame.font.SysFont('helvetica', 30)
        back = font.render('Back (↵)', 1, ACTIVE_COLOR)
        win.blit(back, (screen_width / 2 - back.get_width() / 2, screen_height - 150))

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    return True

        pygame.display.update()

def game_end(win, msg):
    """
    Renders game end screen
    """

    while 1:
        win.fill((0, 0, 0))

        # Title 
        title_font = pygame.font.SysFont('helvetica', 75)
        title = title_font.render('Game Over', 1, (255, 255, 255))
        win.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - 50))
        
        # Text
        item_font = pygame.font.SysFont('helvetica', 30)
        text = item_font.render(msg, 1, (255, 255, 255))
        win.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
