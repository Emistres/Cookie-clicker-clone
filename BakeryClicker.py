import sys
import pygame
from socket import *
from pygame.locals import *
import math


global active_screen 

class Player:

    # Will include all data on player
    # Try to setup to interact with save data

    def __init__ (self, coins=0, click_value=1, passive_income=0):
        
        self.coins = float(coins)
        self.click_value = click_value
        self.passive_income = float(passive_income)


    def coin_update(self, update_type):
        
        # Update type controller
        if self.coins >= 1e+63:
            self.coins = float(math.inf)
            
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
    
    def __init__ (self, price, owned, generation):
        
        self.price = price
        self.owned = owned
        self.generation = generation
        self.base_price = self.price
        
    
    def generation_grow(self, player):
        
        player.passive_income_growth(self.generation)
    

    def cost_increase(self):
        
        if self.price == math.inf:
            pass
        
        else:
            self.price = self.base_price * pow(1.15, self.owned)
        


    def object_bought(self, player):
        
        self.owned += 1
        if self.price == math.inf:
            pass
        else:
            player.coins -= self.price
            self.cost_increase()

            if self.price >= 1e+63:
                self.price = math.inf
    

    def click_increase_check(self,player):

        if self.owned % 10 == 0:
            player.click_value_growth()

    


def get_mouse():
    # Gets coordinates of mouse cursor that frame

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    return mouse_x, mouse_y


def value_scale_text(coins, passive_income):
    """
    solution taken from:
    https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers/3155023#3155023
    """
    n = float(coins)

    cash_suffix = ['',' K',' M',' B',' T','Qd','Qn',
                   'Sx','Sp','O','N','de','Ud','DD',
                   'tdD','qdD','QnD','sxD','SpD','OcD',
                   'NvD']
    
    infinity = math.isinf(coins)

    if infinity == True:
        return 'inf'

    elif coins < 1000 and passive_income == True:
        return f'{n:.1f}'
    else:
        millidx = max(0,min(len(cash_suffix)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    
        return '{:.0f}{}'.format(n / 10**(3 * millidx), cash_suffix[millidx])



def draw_building_button(screen, location_x, location_y, type, building):

    font = pygame.font.SysFont(None, 30)

    pygame.draw.rect(screen, (255,255,255), (location_x, location_y, 150, 100))
    
    text = text = font.render(type, True, (0, 0, 0))                    # building name
    text_rect = text.get_rect(center=(location_x+75, location_y+10))
    screen.blit(text, text_rect)

    text = text = font.render(str(building.owned), True, (0, 0, 0))     # buildings owned
    text_rect = text.get_rect(center=(location_x+75, location_y+30))
    screen.blit(text, text_rect)

    price = value_scale_text(building.price, False)
    text = text = font.render(price, True, (0, 0, 0))                   # building cost
    text_rect = text.get_rect(center=(location_x+75, location_y+80))
    screen.blit(text, text_rect)


def draw_money(player,screen):

    # Update coin counter display value and coins per second
    font_unique = pygame.font.SysFont(None, 100)
    coin_output = value_scale_text(player.coins, False)
    text = font_unique.render(coin_output, True, (255, 255, 255))
    text_rect = text.get_rect(center=((1920/2), 125))
    screen.blit(text, text_rect)

    font_small = pygame.font.SysFont(None, 35)
    passive_income = value_scale_text(player.passive_income, True)
    text = font_small.render(passive_income+" per second", True, (255, 255, 255))
    text_rect = text.get_rect(center=((1920/2), 225))
    screen.blit(text, text_rect)


def rebirth_screen(player, clock, screen):

    while True:

        clock.tick(60)

        screen.fill((0,0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()
    

def bread_screen(player,clock,screen):
    
    global active_screen

    while True:

        clock.tick(60)

        if active_screen != "bread":
            return

        screen.fill((0,0,0))

        # Loads bread icon every frame
        pygame.draw.rect(screen, (181, 103, 0), ((1920/2)-250, 1080/4, 500, 500), 0) 

        draw_money(player,screen)
        
        mouse_x, mouse_y = get_mouse()

        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                
                if ((1920/2)-250) <= mouse_x < ((1920/2)+250):
                    if ((1080/4)) <= mouse_y < ((1080/4)+500):
                        player.coin_update("Click")

        bottom_bar(screen)

        pygame.display.flip()


def upgrade_screen(player,clock,screen):
    
    while True:

        clock.tick(60)

        screen.fill((0,0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()


def bottom_bar(screen):

    global active_screen
    
    pygame.draw.rect(screen, (255, 255, 255), (0, 980, 1920/4, 100), 0) 
    pygame.draw.rect(screen, (255, 255, 255), ((1920/4)+1, 980, 1920/4, 100), 0) 
    pygame.draw.rect(screen, (255, 255, 255), ((1920/2)+2, 980, 1920/4, 100), 0) 
    pygame.draw.rect(screen, (255, 255, 255), (1920/1.33, 980, 1920/4, 100), 0) 

    font_unique = pygame.font.SysFont(None, 100)
    text = font_unique.render("Town", True, (0, 0, 0))
    text_rect = text.get_rect(center=((1920/8), 1080-50))
    screen.blit(text, text_rect)

    font_unique = pygame.font.SysFont(None, 100)
    text = font_unique.render("Upgrades", True, (0, 0, 0))
    text_rect = text.get_rect(center=((1920/8)+((1920/4)+1), 1080-50))
    screen.blit(text, text_rect)

    font_unique = pygame.font.SysFont(None, 100)
    text = font_unique.render("Incarnation", True, (0, 0, 0))
    text_rect = text.get_rect(center=((1920/2.6)+((1920/4)+2), 1080-50))
    screen.blit(text, text_rect)

    font_unique = pygame.font.SysFont(None, 100)
    text = font_unique.render("Menu", True, (0, 0, 0))
    text_rect = text.get_rect(center=((1920/1.6)+((1920/4)), 1080-50))
    screen.blit(text, text_rect)

    mouse_x, mouse_y = get_mouse()
    for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                
                if (0) <= mouse_x < (980):
                    if (1080-100) <= mouse_y < (1080):
                        active_screen = "bread"
    return 

def game_loop(player, clock, screen):
    #Controls loop for gameplay screen and logic
    
    global active_screen

    #Loads building objects
    clicker = Buildings(10, 0, 0.1)
    uncle = Buildings(100, 0, 1)
    farm = Buildings(1000, 0, 10)
    house = Buildings(10000, 0, 100)
    mill = Buildings(100000, 0, 1000)
    market = Buildings(1000000, 0, 10000)  
    tower = Buildings(10000000, 0, 100000)
    castle = Buildings(100000000, 0, 1000000)
    church = Buildings(1000000000, 0, 10000000)
    
    active_screen = "bread"
    while True:

        player.coin_update("Passive")

        # locks game to 60fps
        clock.tick(60)

        # Clears screen every frame to update dynamic text
        screen.fill((0, 0, 0))

        # Loads bread icon every frame
        if active_screen == "bread":   
            bread_screen(player, clock, screen)

        # Load rebirth button
        pygame.draw.rect(screen, (255, 255, 255), (1520, 70, 150, 100), 0)

        # Loads shop frames
        draw_building_button(screen, ((1920/4)*3), 1080/4, "Clicker", clicker)
        draw_building_button(screen, ((1920/4)*3), (1080/4)+101, "Uncle", uncle) 
        draw_building_button(screen, ((1920/4)*3), (1080/4)+202, "Farm", farm) 
        draw_building_button(screen, ((1920/4)*3), (1080/4)+303, "House", house)
        draw_building_button(screen, ((1920/4)*3), (1080/4)+404, "Mill", mill) 
        draw_building_button(screen, ((1920/4)*3) + 151, (1080/4), "Market", market) 
        draw_building_button(screen, ((1920/4)*3) + 151, (1080/4)+101, "Wizzard Tower", tower) 
        draw_building_button(screen, ((1920/4)*3) + 151, (1080/4)+202, "Castle", castle)
        draw_building_button(screen, ((1920/4)*3) + 151, (1080/4)+303, "Church", church)
        

        # Update coin counter display value and coins per second
        
        draw_money(player, screen)

        # Check mouse location and gives an x and y co-ordinate
        mouse_x, mouse_y = get_mouse()
        
        # Checks is mouse is on rebirth button
        on_rebirth = False
        if mouse_x >= 1520 and mouse_x < 1670:
            if mouse_y >= 70 and mouse_y < 170:
                on_rebirth = True

        # Checks if mouse is hovering over the bakery shop
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
        
        on_house = False
        if mouse_x >= 1440 and mouse_x < 1590:
            if mouse_y >= 270+303 and mouse_y < 370+303:
                on_house = True
        
        on_mill = False
        if mouse_x >= 1440 and mouse_x < 1590:
            if mouse_y >= 270+404 and mouse_y < 370+404:
                on_mill = True
        
        on_market = False
        if mouse_x >= 1440 + 151 and mouse_x < 1590 + 151:
            if mouse_y >= 270 and mouse_y < 370:
                on_market = True
        
        on_tower = False
        if mouse_x >= 1440 + 151 and mouse_x < 1590 + 151:
            if mouse_y >= 270 and mouse_y < 370+101:
                on_tower = True

        on_castle = False
        if mouse_x >= 1440 + 151 and mouse_x < 1590 + 151:
            if mouse_y >= 270 and mouse_y < 370+202:
                on_castle = True

        on_church = False
        if mouse_x >= 1440 + 151 and mouse_x < 1590 + 151:
            if mouse_y >= 270 and mouse_y < 370+303:
                on_church = True
        
        
        

        # TO ADD: save data when to a file when this is called
        for event in pygame.event.get():
            # Ends game when button close is pressed
            if event.type == QUIT:
                return
            
            # Checks if mouse clicks on a box
            elif event.type == MOUSEBUTTONDOWN:
                if on_bread == True:
                    player.coin_update("Click") 

                elif on_rebirth == True:
                    rebirth_screen(player, clock, screen)   
                
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

                elif on_house == True:
                    if player.coins >= house.price:
                        house.object_bought(player)
                        house.generation_grow(player)    
                        house.click_increase_check(player)
                    
                elif on_mill == True:
                    if player.coins >= mill.price:
                        mill.object_bought(player)
                        mill.generation_grow(player)    
                        mill.click_increase_check(player)
                    
                elif on_market == True:
                    if player.coins >= market.price:
                        market.object_bought(player)
                        market.generation_grow(player)    
                        market.click_increase_check(player)
                
                elif on_tower == True:
                    if player.coins >= tower.price:
                        tower.object_bought(player)
                        tower.generation_grow(player)    
                        tower.click_increase_check(player)
                
                elif on_castle == True:
                    if player.coins >= castle.price:
                        castle.object_bought(player)
                        castle.generation_grow(player)    
                        castle.click_increase_check(player)
                
                elif on_church == True:
                    if player.coins >= church.price:
                        church.object_bought(player)
                        church.generation_grow(player)    
                        church.click_increase_check(player)
                    
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
