import sys
import math
import pygame
from socket import *
from pygame.locals import *
import time


class Player:

    #dhirtsdjfnhisfhishhisdtsih

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
    # Event loop
    while True:
        # locks game to 60fps
        clock.tick(60)

        # Clears screen every frame to update dynamic text
        screen.fill((0, 0, 0))

        # Loads screen elements every frame
        pygame.draw.rect(screen, (0, 0, 255), (150, 1080/4, 500, 500)) 

        # Update coin counter display value
        text = font.render(str(player.coins), True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 25))
        screen.blit(text, text_rect)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = pygame.mouse.get_pos()

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


if __name__ == "__main__":

    main()
