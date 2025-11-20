import pygame
import random
import math
from pygame import*

# Initialize
pygame.init()

SPAWN_X = 570  
SPAWN_Y = 335   
ITEM_THING = pygame.Rect(1000,500,50,50)
SWORD_THING = pygame.Rect(200,500,35,80)
armor_picked = False
sword_picked = False
enemy_kills = 0

# load item image once (move this before the loop)
armor_img = pygame.image.load("sprite/armor1.png")
armor_img = pygame.transform.scale(armor_img, (50,50))

sword_img = pygame.image.load("sprite/sword2.png")
sword_img = pygame.transform.scale(sword_img, (35,80))

# Create clock object
clock = pygame.time.Clock()
FPS = 60  # Set desired frame rate

# Game window
screen = pygame.display.set_mode((1340, 820))
pygame.display.set_caption("Hello Pygame")

pygame.mixer.music.load("sprite/massobeats - honey jam (freetouse.com).mp3")
pygame.mixer.music.rewind()
pygame.mixer.music.play(loops=-1,start=3.0)

# preload sound effect (use .wav/.ogg if mp3 gives trouble)
swing_sound = pygame.mixer.Sound("sprite/quick-swing-sound-419581.mp3")
swing_sound.set_volume(0.8)

death_sound = pygame.mixer.Sound("sprite/tmp_7901-951678082.mp3")
death_sound.set_volume(0.6)

win_sound = pygame.mixer.Sound("sprite/goodresult-82807.mp3")

class player:
    #Attributes
    def __init__(self, player_height, player_width, health, damage,startposy, startposx,speed,playerimg,angle, hitboxtoggle,max_health ):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.base_damage = damage  
        self.startposy = startposy
        self.startposx = startposx
        self.hitbox =(self.player_height,self.player_width)
        self.speed = speed
        self.playerimg = playerimg
        self.angle = angle
        self.hitboxtoggle = hitboxtoggle
        self.max_health = max_health
    #Methods

class Item:
    def __init__(self,item_img):
        self.item_img = item_img

class Swords(Item):
    def __init__(self,item_img,extra_damage):
        super().__init__(item_img)
        self.extra_damage = extra_damage

sword1 = Swords("sprite/sword.png",0.0)


class Armor(Item):
    def __init__(self,item_img,extra_health):
        super().__init__(item_img)
        self.extra_health = extra_health

armor1 = Armor("sprite/playerarmor1.png",0)
#player1 objekt fra klassen player

player1 = player(100, 100, 200.0 + armor1.extra_health, 5.0 + sword1.extra_damage, 335, 570, 6, "sprite\player.png", 0, 2, 200)

class enemy():
    #Atributes
    def __init__(self, player_height, player_width, health, damage, startposy, startposx ,speed):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposx = startposx
        self.startposy = startposy
        self.speed = speed
        self.hitbox = (self.player_height*0.8,self.player_width+10)
        # attack range in pixels: how close this enemy must get to attack
        # default: ~60% of the larger enemy dimension
        self.attack_range = max(self.player_width, self.player_height) * 0.6
    
    #Methods: 
    def move_towards(self, target_x, target_y, stop_distance=0, dt=1.0):
        """Move the enemy towards (target_x, target_y).
        Stops when within stop_distance (pixels) from the target.
        dt is seconds since last frame (use clock.tick(FPS)/1000.0).
        """
        # current and target as vectors for smooth movement and overshoot prevention
        pos = pygame.math.Vector2(self.startposx, self.startposy)
        target = pygame.math.Vector2(target_x, target_y)
        direction = target - pos
        dist = direction.length()
        if dist <= 0:
            return
        # If already within stopping distance, do nothing
        if dist <= stop_distance:
            return
        # normalize and move by speed*dt, but don't overshoot the stop_distance
        direction = direction.normalize()
        move_amount = self.speed * dt
        # maximum allowed move so we don't pass the stopping distance
        max_move = max(0, dist - stop_distance)
        # clamp move_amount to max_move
        if move_amount > max_move:
            move_amount = max_move
        pos += direction * move_amount
        # write back float positions
        self.startposx, self.startposy = pos.x, pos.y

# Create multiple enemies with random spawn positions
ENEMY_DAMAGE_INTERVAL_MS = 1500  # 2.5 seconds
ENEMY_COUNT = 5
enemies = []
# screen size constants (match the window created above)
SCREEN_W, SCREEN_H = 1340, 820
for _ in range(ENEMY_COUNT):
    sx = random.randint(0, SCREEN_W - 100)  # enemy width is 100 in our class usage
    sy = random.randint(0, SCREEN_H - 150)  # enemy height is 150
    e = enemy(75, 50, 70, 5, sy, sx, 120)  # speed in px/sec for visible movement
    e.last_damage_time = 0
    enemies.append(e)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # frame timing
    dt = clock.tick(FPS) / 1000.0  # seconds since last frame
    current_time = pygame.time.get_ticks()

    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1340,820))
    screen.blit(bg, (0,0))
    # Create transparent surface
    circle_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255,0,0,32), (player1.startposx+player1.player_width*0.5,player1.startposy+player1.player_height*0.5), player1.player_height*2.5, 0)
    screen.blit(circle_surface, (0,0))
    player = pygame.image.load(player1.playerimg)
    player = pygame.transform.scale(player, (player1.player_width, player1.player_height))

    # Load and scale sword image
    sword = pygame.image.load(sword1.item_img)  # Use forward slashes for paths
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
    
    if keys[pygame.K_a]:
        player1.startposx -= player1.speed

    if keys[pygame.K_d]:
        player1.startposx += player1.speed

    if keys[pygame.K_w]:
        player1.startposy -= player1.speed

    if keys[pygame.K_s]:
        player1.startposy += player1.speed
        
    # Simple toggle with H key
    if keys[pygame.K_h] and (current_time - last_hitbox_time) >= HITBOX_COOLDOWN:
        last_hitbox_time = current_time
        player1.hitboxtoggle = -1 if player1.hitboxtoggle == 2 else 2
    

    # Q action: only trigger if cooldown has elapsed
    if keys[pygame.K_SPACE] and (current_time - last_action_time) >= ACTION_COOLDOWN:
        last_action_time = current_time
        player1.angle = -90
        swing_sound.play()
        # Player melee attack: damage all enemies inside the player's red circle
        attack_radius = player1.player_height * 2.5
        player_center = pygame.math.Vector2(player1.startposx + player1.player_width * 0.5,
                                            player1.startposy + player1.player_height * 0.5)
        dead_enemies = []
        for enemy_obj in enemies:
            enemy_center = pygame.math.Vector2(enemy_obj.startposx + enemy_obj.player_width * 0.5,
                                              enemy_obj.startposy + enemy_obj.player_height * 0.5)
            if (enemy_center - player_center).length() <= attack_radius:
                enemy_obj.health -= player1.damage
                # clamp
                if enemy_obj.health <= 0:
                    dead_enemies.append(enemy_obj)
        # remove dead enemies after iterating
        for d in dead_enemies:
            if d in enemies:
                enemies.remove(d)
                enemy_kills += 1

    # Reset angle after the short action duration has passed
    if (current_time - last_action_time) >= ACTION_DURATION:
        player1.angle = 0


    screen_w, screen_h = screen.get_size()
    player1.startposx = max(0, min(player1.startposx, screen_w - player1.player_width))
    player1.startposy = max(0, min(player1.startposy, screen_h - player1.player_height))
   
    pygame.draw.rect(screen,("green"),((60,30),(360*(player1.health/(200+armor1.extra_health)),60)),0)
    pygame.draw.rect(screen,("black"),((60,30),(360,60)),5)
    # Move and draw all enemies
    player_center_x = player1.startposx + player1.player_width * 0.5
    player_center_y = player1.startposy + player1.player_height * 0.5
    # player's rect for collision checks (use updated player position)
    player_rect = pygame.Rect(int(player1.startposx), int(player1.startposy), int(player1.player_width), int(player1.player_height))

    # cache enemy image once per frame
    enemy_img = pygame.image.load("sprite/enemy.webp")

    # player's rect for collision checks (use updated player position)
    player_rect = pygame.Rect(int(player1.startposx), int(player1.startposy), int(player1.player_width), int(player1.player_height))


    for enemy_obj in enemies:
        # move toward the player but stop once inside the enemy's attack range
        enemy_obj.move_towards(player_center_x, player_center_y, enemy_obj.attack_range, dt)
        scaled = pygame.transform.scale(enemy_img, (enemy_obj.player_width, enemy_obj.player_height))
        screen.blit(scaled, (enemy_obj.startposx, enemy_obj.startposy))
        pygame.draw.rect(screen, ("white"), ((enemy_obj.startposx-enemy_obj.player_width*0.18, enemy_obj.startposy+enemy_obj.player_height*0.30), (enemy_obj.hitbox)), player1.hitboxtoggle)

        enemy_rect = pygame.Rect(int(enemy_obj.startposx), int(enemy_obj.startposy), int(enemy_obj.player_width), int(enemy_obj.player_height))
        pygame.draw.rect(screen, "white", enemy_rect, player1.hitboxtoggle)
        # enemy attack condition: if the enemy is within its attack_range of the player's center
        enemy_center = pygame.math.Vector2(enemy_obj.startposx + enemy_obj.player_width * 0.5,
                                          enemy_obj.startposy + enemy_obj.player_height * 0.5)
        player_center = pygame.math.Vector2(player_center_x, player_center_y)
        dist_to_player = (enemy_center - player_center).length()
        if dist_to_player <= enemy_obj.attack_range:
            # within attack range: apply damage with per-enemy cooldown
            if (current_time - enemy_obj.last_damage_time) >= ENEMY_DAMAGE_INTERVAL_MS:
                player1.health -= enemy_obj.damage
                enemy_obj.last_damage_time = current_time

                
                # CHECK FOR DEATH HERE (add this block)
                if player1.health <= 0:
                    font = pygame.font.Font(None, 74)
                    text = font.render('Press R to respawn', True, ("white"))
                    player1.max_health = 200
                    armor1.extra_health = 0
                    sword1.extra_damage = 0
                    enemy_kills = 0
                    armor_picked = False
                    sword_picked = False
                    player1.playerimg = "sprite/PLAYER.PNG"
                    sword1.item_img = "sprite/sword.png"
                    screen.blit(text, (450, 200))
                    death_sound.play()
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
    health_text=f"{player1.health}/{player1.max_health}"
    text = font.render(health_text, True, ("white"))
    screen.blit(text, (60, 100))
    pygame.draw.rect(screen,"white",ITEM_THING,-1)

    #viser kills på skærm eller noget
    kills_text=f"Kills: {enemy_kills}"
    kills_show = font.render(kills_text,True,("white"))
    screen.blit(kills_show,(1170,30))
    
    if enemy_kills >= 25:
        font = pygame.font.Font(None, 174)
        text = font.render('YOU WIN!', True, ("white"))
        win_screen = pygame.Surface((SCREEN_W, SCREEN_H))
        win_screen.set_alpha()
        win_screen.fill((0,0,0))
        screen.blit(win_screen,(0,0))
        player1.max_health = 200
        armor1.extra_health = 0
        sword1.extra_damage = 0
        enemy_kills = 0
        armor_picked = False
        sword_picked = False
        player1.playerimg = "sprite/PLAYER.PNG"
        sword1.item_img = "sprite/sword.png"
        screen.blit(text, (450, 200))
        win_sound.play()
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
        


                    #spawn enemies when less than two are left
    if len(enemies) <= 4:
            for _ in range(4):
                sx = random.randint(0, SCREEN_W - 100)
                sy = random.randint(0, SCREEN_H - 150)
                e = enemy(75, 50, 70, 5, sy, sx, 120)
                e.last_damage_time = 0
                enemies.append(e)

    
    if not armor_picked:
        screen.blit(armor_img, ITEM_THING.topleft)
        pygame.draw.rect(screen, (255,0,0), ITEM_THING, -1)  
    
    pygame.draw.rect(screen,"white",SWORD_THING,-1)
    
    if not sword_picked:
        screen.blit(sword_img, SWORD_THING.topleft)
        pygame.draw.rect(screen, (255,0,0), SWORD_THING, -1) 

    
    player_rect = pygame.Rect(player1.startposx, player1.startposy, player1.player_width, player1.player_height)
    if not armor_picked and player_rect.colliderect(ITEM_THING):
        armor_picked = True
        player1.max_health = 300
        armor1.extra_health = 100
        new_max = 200 + armor1.extra_health
        player1.health = min(player1.health + armor1.extra_health, new_max)
        player1.playerimg = "sprite/playerarmor1.png"
    
    
    player_rect = pygame.Rect(player1.startposx, player1.startposy, player1.player_width, player1.player_height)
    if not sword_picked and player_rect.colliderect(SWORD_THING):
        sword_picked = True
        sword1.extra_damage = 10.0
        sword1.item_img = "sprite/sword2.png"
        # update player's damage to include the sword bonus
        player1.damage = player1.base_damage + sword1.extra_damage

    pygame.display.update()
    clock.tick(FPS) 

# Quit Pygame
pygame.quit()