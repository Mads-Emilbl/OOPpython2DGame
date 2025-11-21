import pygame
import random
import math
from pygame import*

pygame.init()

SPAWN_X = 570  
SPAWN_Y = 335   
ITEM_THING = pygame.Rect(1000,500,50,50)
SWORD_THING = pygame.Rect(200,500,35,80)
armor_picked = False
sword_picked = False
enemy_kills = 0

# loader items
armor_img = pygame.image.load("sprite/armor1.png")
armor_img = pygame.transform.scale(armor_img, (50,50))

sword_img = pygame.image.load("sprite/sword2.png")
sword_img = pygame.transform.scale(sword_img, (35,80))

clock = pygame.time.Clock()
FPS = 60  

# Game window
screen = pygame.display.set_mode((1340, 820))
pygame.display.set_caption("Hello Pygame")

pygame.mixer.music.load("sprite/massobeats - honey jam (freetouse.com).mp3")
pygame.mixer.music.rewind()
pygame.mixer.music.play(loops=-1,start=3.0)

# preloader lyde så de kan spilles senere
swing_sound = pygame.mixer.Sound("sprite/quick-swing-sound-419581.mp3")
swing_sound.set_volume(0.8)

death_sound = pygame.mixer.Sound("sprite/tmp_7901-951678082.mp3")
death_sound.set_volume(0.6)

win_sound = pygame.mixer.Sound("sprite/goodresult-82807.mp3")

class player:
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

player1 = player(100, 100, 100.0 + armor1.extra_health, 5.0 + sword1.extra_damage, 335, 570, 6, "sprite\player.png", 0, 2, 100)

class enemy():
    def __init__(self, player_height, player_width, health, damage, startposy, startposx ,speed):
        self.player_height = player_height
        self.player_width = player_width
        self.health = health
        self.damage = damage
        self.startposx = startposx
        self.startposy = startposy
        self.speed = speed
        self.hitbox = (self.player_height*0.8,self.player_width+10)
        self.attack_range = max(self.player_width, self.player_height) * 0.6
     
    def move_towards(self, target_x, target_y, stop_distance=0, dt=1.0):
        """Move the enemy towards (target_x, target_y).
        Stops when within stop_distance (pixels) from the target.
        dt is seconds since last frame (use clock.tick(FPS)/1000.0).
        """
        pos = pygame.math.Vector2(self.startposx, self.startposy)
        target = pygame.math.Vector2(target_x, target_y)
        direction = target - pos
        dist = direction.length()
        if dist <= 0:
            return
        if dist <= stop_distance:
            return
        # normalize and move by speed
        direction = direction.normalize()
        move_amount = self.speed * dt
        max_move = max(0, dist - stop_distance)
        if move_amount > max_move:
            move_amount = max_move
        pos += direction * move_amount
        self.startposx, self.startposy = pos.x, pos.y

# spawner 5 enemies i starten
ENEMY_DAMAGE_INTERVAL_MS = 1500 
ENEMY_COUNT = 5
enemies = []
SCREEN_W, SCREEN_H = 1340, 820
for _ in range(ENEMY_COUNT):
    sx = random.randint(0, SCREEN_W - 100)  
    sy = random.randint(0, SCREEN_H - 150)  
    e = enemy(75, 50, 70, 5, sy, sx, 120) 
    e.last_damage_time = 0
    enemies.append(e)

running = True

#Cooldown timer
last_action_time = 0
last_hitbox_time = 0  
last_damage_time = 0
ACTION_COOLDOWN = 800  
HITBOX_COOLDOWN = 250  
ACTION_DURATION = 500  
DAMAGE_COOLDOWN = 400

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # frame timing
    dt = clock.tick(FPS) / 1000.0  
    current_time = pygame.time.get_ticks()

    screen.fill("white")
    bg = pygame.image.load("sprite/background.webp")
    bg = pygame.transform.scale(bg,(1340,820))
    screen.blit(bg, (0,0))
    circle_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255,0,0,32), (player1.startposx+player1.player_width*0.5,player1.startposy+player1.player_height*0.5), player1.player_height*1.5, 0)
    screen.blit(circle_surface, (0,0))
    player = pygame.image.load(player1.playerimg)
    player = pygame.transform.scale(player, (player1.player_width, player1.player_height))

    # Load and scale sword image
    sword = pygame.image.load(sword1.item_img)  
    sword = pygame.transform.scale(sword, (35, 80))
    sword = pygame.transform.rotate(sword, player1.angle)  

    #Player image on screen
    screen.blit(player, (player1.startposx, player1.startposy))

    #Sword at player's position
    sword_x = player1.startposx + (player1.player_width - sword.get_width()) / 2  
    sword_y = player1.startposy  
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
        
    if keys[pygame.K_h] and (current_time - last_hitbox_time) >= HITBOX_COOLDOWN:
        last_hitbox_time = current_time
        player1.hitboxtoggle = -1 if player1.hitboxtoggle == 2 else 2
    

    if keys[pygame.K_SPACE] and (current_time - last_action_time) >= ACTION_COOLDOWN:
        last_action_time = current_time
        player1.angle = -90
        swing_sound.play()
        attack_radius = player1.player_height * 1.5
        player_center = pygame.math.Vector2(player1.startposx + player1.player_width * 0.5,
                                            player1.startposy + player1.player_height * 0.5)
        dead_enemies = []
        for enemy_obj in enemies:
            enemy_center = pygame.math.Vector2(enemy_obj.startposx + enemy_obj.player_width * 0.5,
                                              enemy_obj.startposy + enemy_obj.player_height * 0.5)
            if (enemy_center - player_center).length() <= attack_radius:
                enemy_obj.health -= player1.damage
                if enemy_obj.health <= 0:
                    dead_enemies.append(enemy_obj)
        for d in dead_enemies:
            if d in enemies:
                enemies.remove(d)
                enemy_kills += 1

    if (current_time - last_action_time) >= ACTION_DURATION:
        player1.angle = 0


    screen_w, screen_h = screen.get_size()
    player1.startposx = max(0, min(player1.startposx, screen_w - player1.player_width))
    player1.startposy = max(0, min(player1.startposy, screen_h - player1.player_height))
   
    pygame.draw.rect(screen,("green"),((60,30),(360*(player1.health/(100+armor1.extra_health)),60)),0)
    pygame.draw.rect(screen,("black"),((60,30),(360,60)),5)
    # Move and draw all enemies
    player_center_x = player1.startposx + player1.player_width * 0.5
    player_center_y = player1.startposy + player1.player_height * 0.5
    player_rect = pygame.Rect(int(player1.startposx), int(player1.startposy), int(player1.player_width), int(player1.player_height))

    enemy_img = pygame.image.load("sprite/enemy.webp")

    player_rect = pygame.Rect(int(player1.startposx), int(player1.startposy), int(player1.player_width), int(player1.player_height))


    for enemy_obj in enemies:
        enemy_obj.move_towards(player_center_x, player_center_y, enemy_obj.attack_range, dt)
        scaled = pygame.transform.scale(enemy_img, (enemy_obj.player_width, enemy_obj.player_height))
        screen.blit(scaled, (enemy_obj.startposx, enemy_obj.startposy))
        pygame.draw.rect(screen, ("white"), ((enemy_obj.startposx-enemy_obj.player_width*0.18, enemy_obj.startposy+enemy_obj.player_height*0.30), (enemy_obj.hitbox)), player1.hitboxtoggle)

        enemy_rect = pygame.Rect(int(enemy_obj.startposx), int(enemy_obj.startposy), int(enemy_obj.player_width), int(enemy_obj.player_height))
        pygame.draw.rect(screen, "white", enemy_rect, player1.hitboxtoggle)
        #Attack if enemy is within its attack_range
        enemy_center = pygame.math.Vector2(enemy_obj.startposx + enemy_obj.player_width * 0.5,
                                          enemy_obj.startposy + enemy_obj.player_height * 0.5)
        player_center = pygame.math.Vector2(player_center_x, player_center_y)
        dist_to_player = (enemy_center - player_center).length()
        if dist_to_player <= enemy_obj.attack_range:
            if (current_time - enemy_obj.last_damage_time) >= ENEMY_DAMAGE_INTERVAL_MS:
                player1.health -= enemy_obj.damage
                enemy_obj.last_damage_time = current_time

                
                if player1.health <= 0:
                    font = pygame.font.Font(None, 74)
                    text = font.render('Press R to respawn', True, ("white"))
                    player1.max_health = 100
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
                                    player1.health = 100
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
        player1.max_health = 100
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
                        player1.health = 100
                        waiting = False
        


                    #spawner enemies når der er få tilbage
    if len(enemies) <= 4:
            for _ in range(7):
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
        player1.max_health = 150
        armor1.extra_health = 50
        new_max = 100 + armor1.extra_health
        player1.health = min(player1.health + armor1.extra_health, new_max)
        player1.playerimg = "sprite/playerarmor1.png"
    
    
    player_rect = pygame.Rect(player1.startposx, player1.startposy, player1.player_width, player1.player_height)
    if not sword_picked and player_rect.colliderect(SWORD_THING):
        sword_picked = True
        sword1.extra_damage = 10.0
        sword1.item_img = "sprite/sword2.png"
        player1.damage = player1.base_damage + sword1.extra_damage

    pygame.display.update()
    clock.tick(FPS) 

pygame.quit()