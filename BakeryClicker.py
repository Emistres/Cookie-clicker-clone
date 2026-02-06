import sys
import math
import pygame
from socket import *
from pygame.locals import *
import time


class Player:

    # Will include all data on player
    # Try to setup to interact with save data

    def __init__ (self, coins=0, click_value=1, passive_income=0):
        
        self.coins = coins
        self.click_value = click_value
        self.passive_income = passive_income


    def coin_update(self, update_type):
        
        # Will contain all math logic for the players coins
        # Setup to call when an instance of money increase is created
        
        if update_type == "Click":
            self.coins += self.click_value
        
        return
    
    # Function to increment click value




    # Function to adjust total passive income ammount






class Buildings:

    # Create a parent with easily ajustable values can be used by children
    
    
    
    
    # Incremental building cost function that works with all values

    pass



def get_mouse():
    # Gets coordinates of mouse cursor that frame

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    return mouse_x, mouse_y
    


def game_loop(font,player,clock,screen):

    while True:
        # locks game to 60fps
        clock.tick(60)

        # Clears screen every frame to update dynamic text
        screen.fill((0, 0, 0))

        # Loads bread icon every frame
        pygame.draw.rect(screen, (181, 103, 0), (150, 1080/4, 500, 500)) 

        # Update coin counter display value
        font_unique = pygame.font.SysFont(None, 100)
        text = font_unique.render(str(player.coins), True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 125))
        screen.blit(text, text_rect)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = get_mouse()

        # Checks if mouse is hovering over the bakery shape
        on_box = False
        if mouse_x >= 150 and mouse_x <= 650:
            if mouse_y >= 270 and mouse_y <= 770:
                on_box = True

        
        # TO ADD: save data when to a file when this is called
        for event in pygame.event.get():
            # Ends game when button close is pressed
            if event.type == QUIT:
                return
            
            # Checks if mouse clicks on box
            elif event.type == MOUSEBUTTONDOWN and on_box == True:
                player.coin_update("Click")               
            
        pygame.display.flip()


def main_menu(font,player,clock,screen):

    while True:
        # 60 fps limit
        clock.tick(60)

        # Clears screen every frame to update dynamic text
        screen.fill((0, 0, 0))

        # Writes name of game in larger font
        font_unique = pygame.font.SysFont(None, 200)
        text = font_unique.render("Bakery clicker", True, (225, 225, 255))
        text_rect = text.get_rect(center=(1920/2, 150))
        screen.blit(text, text_rect)

        # Draws menu buttons
        pygame.draw.rect(screen, (225, 225, 255), (540, 400, 850, 100)) #new game
        pygame.draw.rect(screen, (225, 225, 255), (540, 550, 850, 100)) #load save
        pygame.draw.rect(screen, (225, 225, 255), (540, 700, 850, 100)) #quit game

        # Writes text on menu buttons
        text = font.render("New game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 450))
        screen.blit(text, text_rect)

        text = font.render("Load game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 600))
        screen.blit(text, text_rect)

        text = font.render("Quit game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 750))
        screen.blit(text, text_rect)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = get_mouse()
        

        # Advances main menu based on what button is pressed
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
    

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Bakery Clicker")
    font = pygame.font.SysFont(None, 50)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    player = Player()
    
    # Opens main menu of game
    main_menu(font,player,clock,screen)
    
    # Start main gameplay loop
    game_loop(font,player,clock,screen)


if __name__ == "__main__":

    main()
