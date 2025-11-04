import pygame
from pygame import*

# Initialize
pygame.init()

# Game window
screen = pygame.display.set_mode((1240, 820))
pygame.display.set_caption("Hello Pygame")

class player:
    #Attributes
    def __init__(self, player_height, player_width, health, damage):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.hitbox =(self.player_height + 10,self.player_width + 10)
    
    #Methods


#player1 objekt fra klassen player
player1 = player(150, 100, 200, 5)

class enemy(player):
    #Atributes
    def __init__(self, player_height, player_width, health, damage):
        super().__init__(player_height, player_width, health, damage)
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
    
    #Methods: 

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1240,820))
    screen.blit(bg, (0,0))
    #pygame.display.set(bg)
    player = pygame.image.load("sprite/player.webp")
    player = pygame.transform.scale(player,(player1.player_width, player1.player_height))
    screen.blit(player, (570, 335))
    pygame.draw.rect(screen,("white"),((570,335),(player1.hitbox)),2)
    pygame.display.update()

    
# Quit Pygame
pygame.quit()