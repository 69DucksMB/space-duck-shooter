# =============================== #
# oops_mark.py
# Mark Balagtas
# 6/10/2021
# Using OOP to create:
# Explosive space ducks shooter
# =============================== #

import random
import pygame
from os import path # path directory

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 800
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0) # colours uwu
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init() # inits pygame 
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # open game window
pygame.display.set_caption("My Game")
clock = pygame.time.Clock() # for fps
all_sprites = pygame.sprite.Group() # group holding all sprites

# ========= classes ======== #
            
class Player(pygame.sprite.Sprite): # creates sprite object
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # runs sprite classes initializer
        self.image = pygame.transform.scale(player_img, (60, 48)) # size of ship
        self.image.set_colorkey(BLACK) # keys out colour black
        self.rect = self.image.get_rect() # defines rectangle
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0 
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]: # if arrow keys (left or right) are pressed, move left or right
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx #moving using speedx
        if self.rect.right > WIDTH: # prevents going off screen
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        

class Mob(pygame.sprite.Sprite): # adds mob object
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-2000, -60) # where they spawn
        self.rect.y =  random.randrange(0, HEIGHT/3) 
        self.speedy = 5 # speed of mob
        
    def update(self): # update
        self.rect.x += self.speedy
        if self.rect.right > WIDTH + 60: # if hit ends of screen spawns more
            self.rect.x = random.randrange(-2000,-60)
            self.rect.y = random.randrange(0, HEIGHT/3)
            self.speedy = 5 # speed
            
            
class Bullet(pygame.sprite.Sprite): # adds bullet sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 40)) # scaling bullet img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
            
            
class Explosion(pygame.sprite.Sprite): # explosionnnnn
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0] 
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
# =================== functions =======================

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
                
# =================================================== #
#                       MAIN
# =================================================== #

# Loading all game graphics
background = pygame.image.load(path.join(img_dir, 'bg.jpg')).convert()
background_rect = background.get_rect()
background_scaled = pygame.transform.scale(background, (WIDTH,HEIGHT))
player_img = pygame.image.load(path.join(img_dir, 'ship5.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laser1.png")).convert()

explosion_anim = [] #list of explosion tiles/sprites
for i in range(9):
    filename = 'tile00{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim.append(img) # adds every explosion img into list

    
# Grouping Sprites
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player) # adds player sprite
num_of_mobs = 5    # num of mobs
for i in range(num_of_mobs): # will add all mobs 
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
    
# ================= game loop ================ #

running = True
while running:
    clock.tick(FPS) # keep loop running at the right speed
    
    for event in pygame.event.get(): # checks for all events using for loop
        if event.type == pygame.QUIT: # check for closing window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # shooting with space
                player.shoot()
    
    # update
    all_sprites.update()
    
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits: # loops thru so every mob shot, another is spawned
        expl = Explosion(hit.rect.center) # explosion played
        all_sprites.add(expl)
        newmob() 
        
# draw / render
    screen.fill(BLACK)
    screen.blit(background_scaled, background_rect) # draws bg onto screen
    all_sprites.draw(screen) # draws all sprites
    pygame.display.flip() # draws ^everything^ then shows it
        
pygame.quit() 