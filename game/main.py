import pygame
from pygame import*

# Initialize
pygame.init()

# Game window
screen = pygame.display.set_mode((1340, 820))
pygame.display.set_caption("Hello Pygame")

class player:
    #Attributes
    def __init__(self, player_height, player_width, health, damage,startposy, startposx,speed,playerimg,angle):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposy = startposy
        self.startposx = startposx
        self.hitbox =(self.player_height*0.8,self.player_width+10)
        self.speed = speed
        self.playerimg = playerimg
        self.angle = angle
    
    #Methods


#player1 objekt fra klassen player
player1 = player(150, 100, 200, 5, 335, 570, 5,"sprite\player.webp",0 )

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
ACTION_COOLDOWN = 800  # 800 ms = 0.8 s
ACTION_DURATION = 500  # how long the swing/angle stays active (ms)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1340,820))
    screen.blit(bg, (0,0))
    #pygame.display.set(bg)
    player = pygame.image.load(player1.playerimg)
    player = pygame.transform.scale(player,(player1.player_width, player1.player_height))
    player = pygame.transform.rotate(player,player1.angle)
    screen.blit(player, (player1.startposx,player1.startposy))
    pygame.draw.rect(screen,("white"),((player1.startposx-player1.player_width*0.18,player1.startposy+player1.player_height*0.30),(player1.hitbox)),2)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player1.startposx -= player1.speed

    if keys[pygame.K_RIGHT]:
        player1.startposx += player1.speed

    if keys[pygame.K_UP]:
        player1.startposy -= player1.speed

    if keys[pygame.K_DOWN]:
        player1.startposy += player1.speed
    
    current_time = pygame.time.get_ticks()

    # Q action: only trigger if cooldown has elapsed
    if keys[pygame.K_q] and (current_time - last_action_time) >= ACTION_COOLDOWN:
        last_action_time = current_time
        player1.angle = -90
        player1.player_height + 350
        pygame.mixer.music.load("sprite\quick-swing-sound-419581.mp3")
        pygame.mixer.music.play(1)

    # Reset angle after the short action duration has passed
    if (current_time - last_action_time) >= ACTION_DURATION:
        player1.angle = 0
        player1.player_height - 350


    screen_w, screen_h = screen.get_size()
    player1.startposx = max(47, min(player1.startposx, screen_w - player1.player_width-32))
    player1.startposy = max(-35, min(player1.startposy, screen_h - player1.player_height-15))
   
    health = pygame.image.load("sprite\Healthbarfull.png")
    health = pygame.transform.scale(health,(500,250))
    screen.blit(health,(-100,-80))
    pygame.display.update()


# Quit Pygame
pygame.quit()