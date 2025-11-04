import pygame
from pygame import*

# Initialize
pygame.init()

# Game window
screen = pygame.display.set_mode((1340, 820))
pygame.display.set_caption("Hello Pygame")

class player:
    #Attributes
    def __init__(self, player_height, player_width, health, damage,startposy, startposx,speed):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposy = startposy
        self.startposx = startposx
        self.hitbox =(self.player_height*0.8,self.player_width+10)
        self.speed = speed
        
    
    #Methods


#player1 objekt fra klassen player
player1 = player(150, 100, 200, 5, 335, 570, 3)

class enemy(player):
    #Atributes
    def __init__(self, player_height, player_width, health, damage, startposy, startposx ,speed):
        super().__init__(player_height, player_width, health, damage, startposy, startposx ,speed)
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposx = startposx
        self.startposy = startposy
        self.speed = speed
        self.hitbox = (self.player_height*0.8,self.player_width+10)
    
    #Methods: 

enemy1 = enemy(150, 100, 200, 5, 335, 570+130, 2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1340,820))
    screen.blit(bg, (0,0))
    #pygame.display.set(bg)
    player = pygame.image.load("sprite/player.webp")
    player = pygame.transform.scale(player,(player1.player_width, player1.player_height))
    screen.blit(player, (player1.startposx,player1.startposy))
    pygame.draw.rect(screen,("white"),((player1.startposx-player1.player_width*0.18,player1.startposy+player1.player_height*0.30),(player1.hitbox)),2)


    #Enemy1 sættes på skærmen.
    enemy = pygame.image.load("sprite/enemy.webp")
    # scale the loaded enemy image (pass the Surface), not the enemy object
    enemy = pygame.transform.scale(enemy, (enemy1.player_width, enemy1.player_height))
    screen.blit(enemy,(enemy1.startposx, enemy1.startposy))
    pygame.draw.rect(screen,("white"),((enemy1.startposx-enemy1.player_width*0.18,enemy1.startposy+enemy1.player_height*0.30),(enemy1.hitbox)),2)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player1.startposx -= player1.speed

    if keys[pygame.K_RIGHT]:
        player1.startposx += player1.speed

    if keys[pygame.K_UP]:
        player1.startposy -= player1.speed

    if keys[pygame.K_DOWN]:
        player1.startposy += player1.speed
    pygame.display.update()


# Quit Pygame
pygame.quit()