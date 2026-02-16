import sys
import pygame
from socket import *
from pygame.locals import *


class Player:

    # Will include all data on player
    # Try to setup to interact with save data

    def __init__ (self, coins=0, click_value=1, passive_income=0):
        
        self.coins = float(coins)
        self.click_value = click_value
        self.passive_income = passive_income


    def coin_update(self, update_type):
        
        # Update type controller
        
        if update_type == "Click":
            self.coins += self.click_value
        
        elif update_type == "Passive":
            self.coins += float(self.passive_income/60)
        
        return
    

    # Function to increment click value
    def click_value_growth(self):
        
        self.click_value = self.click_value*2


    # Function to adjust total passive income ammount
    def passive_income_growth(self, external_passive_income):
        
        self.passive_income += external_passive_income


class Buildings:
    # Contains all logic for buildings
    
    def __init__ (self, price=10, owned=0, generation=1):
        
        self.price = price
        self.owned = owned
        self.generation = generation
        
    
    def generation_grow(self, player):
        
        player.passive_income_growth(self.generation)
    

    def cost_increase(self):
        
        self.price += int(self.price/(5/(self.owned*0.25)))


    def object_bought(self, player):

        self.owned += 1
        player.coins -= self.price
        self.cost_increase()
    

    def click_increase_check(self,player):

        if self.owned == 10:
            player.click_value_growth()

        elif self.owned == 100:
            player.click_value_growth()


def get_mouse():
    # Gets coordinates of mouse cursor that frame

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    return mouse_x, mouse_y


def value_scale_text(coins):

    coins = int(coins)
    if coins < 1000000:
        return str(coins) + " Coins"
   
    elif coins >= 1000000 and coins < 1000000000:
        coins = coins/1000000
        coins = round(coins, 2)
        return str(coins) + " M Coins"
    
    elif coins >= 1000000000 and coins < 1000000000000:
        coins = coins/1000000000
        coins = round(coins, 2)
        return str(coins) + " B Coins"

    elif coins >= 1000000000000 and coins < 1000000000000000:
        coins = coins/1000000000000
        coins = round(coins, 2)
        return str(coins) + " T Coins"


def draw_building_button(screen, location_x, location_y, type, building):

    font = pygame.font.SysFont(None, 30)

    pygame.draw.rect(screen, (255,255,255), (location_x, location_y, 150, 100))
    
    text = text = font.render(type, True, (0, 0, 0))                    # building name
    text_rect = text.get_rect(center=(location_x+75, location_y+10))
    screen.blit(text, text_rect)

    text = text = font.render(str(building.owned), True, (0, 0, 0))     # buildings owned
    text_rect = text.get_rect(center=(location_x+75, location_y+30))
    screen.blit(text, text_rect)

    price = value_scale_text(building.price)
    text = text = font.render(price, True, (0, 0, 0))                   # building cost
    text_rect = text.get_rect(center=(location_x+75, location_y+80))
    screen.blit(text, text_rect)



def game_loop(player, clock, screen):
    #Controls loop for gameplay screen and logic

    #Loads building objects
    clicker = Buildings(10, 0, 1)
    uncle = Buildings(100, 0, 10)
    farm = Buildings(1000, 0, 100)
    
    
    while True:

        player.coin_update("Passive")

        # locks game to 60fps
        clock.tick(60)

        # Clears screen every frame to update dynamic text
        screen.fill((0, 0, 0))

        # Loads bread icon every frame
        pygame.draw.rect(screen, (181, 103, 0), (150, 1080/4, 500, 500)) 

        # Loads shop frames
        draw_building_button(screen, ((1920/4)*3), 1080/4, "clicker", clicker)
        draw_building_button(screen, ((1920/4)*3), (1080/4)+101, "uncle", uncle) 
        draw_building_button(screen, ((1920/4)*3), (1080/4)+202, "farm", farm) 

        # Update coin counter display value
        font_unique = pygame.font.SysFont(None, 100)
        coin_output = value_scale_text(player.coins)
        text = font_unique.render(coin_output, True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 125))
        screen.blit(text, text_rect)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = get_mouse()
        
        # Checks if mouse is hovering over the bakery shape
        on_bread = False
        if mouse_x >= 150 and mouse_x < 650:
            if mouse_y >= 270 and mouse_y < 770:
                on_bread = True
        
        # Checks if mouse over a shop icon
        on_clicker = False
        if mouse_x >= 1440 and mouse_x < 1590:
            if mouse_y >= 270 and mouse_y < 370:
                on_clicker = True
        
        on_uncle = False
        if mouse_x >= 1440 and mouse_x < 1590:
            if mouse_y >= 270+101 and mouse_y < 370+101:
                on_uncle = True
        
        on_farm = False
        if mouse_x >= 1440 and mouse_x < 1590:
            if mouse_y >= 270+202 and mouse_y < 370+202:
                on_farm = True
        

        # TO ADD: save data when to a file when this is called
        for event in pygame.event.get():
            # Ends game when button close is pressed
            if event.type == QUIT:
                return
            
            # Checks if a key was pressed that frame
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # Terminates game when escape is pressed (mostly a debugging thing)
                if event.mod & pygame.KMOD_escape:
                    return 
            
            # Checks if mouse clicks on a box
            elif event.type == MOUSEBUTTONDOWN:
                if on_bread == True:
                    player.coin_update("Click")    
                
                elif on_clicker == True:
                    if player.coins >= clicker.price:
                        clicker.object_bought(player)
                        clicker.generation_grow(player)    
                        clicker.click_increase_check(player)

                elif on_uncle == True:
                    if player.coins >= uncle.price:
                        uncle.object_bought(player)
                        uncle.generation_grow(player)    
                        uncle.click_increase_check(player)
                
                elif on_farm == True:
                    if player.coins >= farm.price:
                        farm.object_bought(player)
                        farm.generation_grow(player)    
                        farm.click_increase_check(player)
                    
        pygame.display.flip()


def main_menu(font_base,player,clock,screen):
    # Controls the main menu logic for the game and loads as inital screen
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
        text = font_base.render("New game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 450))
        screen.blit(text, text_rect)

        text = font_base.render("Load game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 600))
        screen.blit(text, text_rect)

        text = font_base.render("Quit game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(1920/2, 750))
        screen.blit(text, text_rect)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = get_mouse()

        on_new_game = False
        if mouse_x >= 539 and mouse_x < 1390:
            if mouse_y >= 399 and mouse_y < 497:
                on_new_game = True

        on_load_game = False
        if mouse_x >= 539 and mouse_x < 1390:
            if mouse_y >= 399+150 and mouse_y < 497+150:
                on_load_game = True
        
        on_close_game = False
        if mouse_x >= 539 and mouse_x < 1390:
            if mouse_y >= 399+300 and mouse_y < 497+300:
                on_close_game = True

        # Advances main menu based on what button is pressed
        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                if on_new_game == True:
                    return
                
                elif on_load_game == True:
                    print ("load")
                    return
                
                elif on_close_game == True:
                    sys.exit()

                return

        pygame.display.flip()
    

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Bakery Clicker")
    font_base = pygame.font.SysFont(None, 50)

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
    main_menu(font_base,player,clock,screen)
    
    # Start main gameplay loop
    game_loop(player,clock,screen)


if __name__ == "__main__":

    main()
