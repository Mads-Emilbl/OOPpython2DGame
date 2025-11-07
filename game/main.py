import pygame
import random
import math
from pygame import*

# Initialize
pygame.init()

SPAWN_X = 570  
SPAWN_Y = 335  
DAMAGE_BLOCK = pygame.Rect(0, 800, 1340,20)  

# Create clock object
clock = pygame.time.Clock()
FPS = 60  # Set desired frame rate

# Game window
screen = pygame.display.set_mode((1340, 820))
pygame.display.set_caption("Hello Pygame")

class player:
    #Attributes
    def __init__(self, player_height, player_width, health, damage,startposy, startposx,speed,playerimg,angle, hitboxtoggle ):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposy = startposy
        self.startposx = startposx
        self.hitbox =(self.player_height,self.player_width)
        self.speed = speed
        self.playerimg = playerimg
        self.angle = angle
        self.hitboxtoggle = hitboxtoggle
    #Methods

class Item:
    def __init__(self,item_img):
        self.item_img = item_img

class Swords(Item):
    def __init__(self,item_img,extra_damage):
        super().__init__(item_img)
        self.extra_damage = extra_damage


class Armor(Item):
    def __init__(self,item_img,extra_health):
        super().__init__(item_img)
        self.extra_health = extra_health

#player1 objekt fra klassen player
player1 = player(100, 100, 200.0, 5, 335, 570, 6, "sprite\player.png", 0, 2)

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

# Add cooldown timer (milliseconds)
last_action_time = 0
last_hitbox_time = 0  # New timer for hitbox toggle
last_damage_time = 0
ACTION_COOLDOWN = 800  # 800 ms = 0.8 s
HITBOX_COOLDOWN = 250  # 250 ms = 0.25 sec
ACTION_DURATION = 500  # how long the swing/angle stays active (ms)
DAMAGE_COOLDOWN = 400

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1340,820))
    screen.blit(bg, (0,0))
    # Create transparent surface
    circle_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255,0,0,32), (player1.startposx+player1.player_width*0.5,player1.startposy+player1.player_height*0.5), player1.player_height*1.4, 0)
    screen.blit(circle_surface, (0,0))
    player = pygame.image.load(player1.playerimg)
    player = pygame.transform.scale(player, (player1.player_width, player1.player_height))

    # Load and scale sword image
    sword = pygame.image.load("sprite/sword.png")  # Use forward slashes for paths
    sword = pygame.transform.scale(sword, (35, 80))
    sword = pygame.transform.rotate(sword, player1.angle)  # Rotate the sword based on player's angle

    # Blit the player image onto the screen
    screen.blit(player, (player1.startposx, player1.startposy))

    # Blit the sword onto the screen at the player's position
    sword_x = player1.startposx + (player1.player_width - sword.get_width()) / 2  # Center sword
    sword_y = player1.startposy  # Adjust as needed
    screen.blit(sword, (sword_x+30, sword_y+20))
    pygame.draw.rect(screen,("white"),((player1.startposx,player1.startposy),(player1.hitbox)),player1.hitboxtoggle)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player1.startposx -= player1.speed

    if keys[pygame.K_RIGHT]:
        player1.startposx += player1.speed

    if keys[pygame.K_UP]:
        player1.startposy -= player1.speed

    if keys[pygame.K_DOWN]:
        player1.startposy += player1.speed
        
    # Simple toggle with H key
    if keys[pygame.K_h] and (current_time - last_hitbox_time) >= HITBOX_COOLDOWN:
        last_hitbox_time = current_time
        player1.hitboxtoggle = -1 if player1.hitboxtoggle == 2 else 2
    
    current_time = pygame.time.get_ticks()

    # Q action: only trigger if cooldown has elapsed
    if keys[pygame.K_q] and (current_time - last_action_time) >= ACTION_COOLDOWN:
        last_action_time = current_time
        player1.angle = -90
        pygame.mixer.music.load("sprite\quick-swing-sound-419581.mp3")
        pygame.mixer.music.play(1)

    # Reset angle after the short action duration has passed
    if (current_time - last_action_time) >= ACTION_DURATION:
        player1.angle = 0


    screen_w, screen_h = screen.get_size()
    player1.startposx = max(0, min(player1.startposx, screen_w - player1.player_width))
    player1.startposy = max(0, min(player1.startposy, screen_h - player1.player_height))
   
    pygame.draw.rect(screen,("green"),((60,30),(360*(player1.health/200),60)),0)
    pygame.draw.rect(screen,("black"),((60,30),(360,60)),5)
    

    
    pygame.draw.rect(screen, "red", DAMAGE_BLOCK)
    
    
    player_rect = pygame.Rect(player1.startposx, player1.startposy, player1.player_width, player1.player_height)
    if player_rect.colliderect(DAMAGE_BLOCK):
        damage_amount = random.uniform(0.5, 2)  # Generate random damage between 0.5 and 2
        player1.health -= damage_amount
        
        # Round health up to the nearest whole number
        if player1.health < 0:
            player1.health = 0  # Prevent negative health
        else:
            player1.health = int(player1.health) + (1 if player1.health % 1 > 0 else 0)  # Round up if there's a fraction

        if player1.health <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render('Press R to respawn', True, ("white"))
            screen.blit(text, (450, 200))
            pygame.display.update()
            
        
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            player1.startposx = SPAWN_X
                            player1.startposy = SPAWN_Y
                            player1.health = 200
                            waiting = False
    font = pygame.font.Font(None, 35)
    health_text=f"{player1.health}/200"
    text = font.render(health_text, True, ("white"))
    screen.blit(text, (60, 100))

    pygame.display.update()
    clock.tick(FPS)  # Limit frame rate


# Quit Pygame
pygame.quit()