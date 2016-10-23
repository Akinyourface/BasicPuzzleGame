import pygame
from pygame.locals import *
from random import randint


""" This file was mainly used to test collision detection using pygame sprites, and to figure out how to load a map using arrays. Later on I might use tiled but 
    I just wanted to make sure that I had a grasp on what to do with normal text files.
 
   **TODO**
    * Fiqure out how to read arrays from a text file
    * Fiqure out a leveling switching system

    * Maybe learn a few math equation to have blocks rotate around a pivot point which the player will have to advoid
    * Add scoring functionality and score 'blocks' you could say
"""






BLACK = (0, 0, 0)
WHITE = (255,255,255)

BLUE = (0, 0, 255)

SCREEN_WIDTH = 1920

SCREEN_HEIGHT = 1080



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([16,16])
        self.imageSurf = pygame.image.load("player.png")
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.timesDied = 0
        self.image.blit(self.imageSurf, (self.rect.x - 64 + 14, self.rect.y - 64 + 14))
        self.dir = 3 # 1 left, 2 right, 3 up, 4 down
        self.dirWS = 0
        self.xvelocity = 0
        self.yvelocity = 0
        self.health = 100

    def update_pos(self, x, y):
        self.xvelocity += x
        self.yvelocity += y

    def update(self):
        self.rect.x += self.xvelocity
        
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        exit_hit_list = pygame.sprite.spritecollide(self, self.Exit, False)
        lava_hit_list = pygame.sprite.spritecollide(self, self.lava, False)
        crate_hit_list = pygame.sprite.spritecollide(self, self.crate, False)
        second_crate_hit_list = pygame.sprite.spritecollide(self, self.sec_crate, False)

        for col in crate_hit_list:
            if self.rect.left <= col.rect.left and self.rect.left <= col.rect.right and col.rect.left and self.dir == 1:
                self.rect.right = col.rect.left
                col.rect.x += 1
                
            if self.rect.right >= col.rect.left and self.rect.right >= col.rect.right and col.rect.left and self.dir == 2:
                self.rect.left = col.rect.right
                col.rect.x -= 1
                
            if self.rect.top <= col.rect.top and self.rect.top <= col.rect.bottom and col.rect.top and self.dirWS == 4:
                self.rect.bottom = col.rect.top
                col.rect.y += 1
                
            if self.rect.bottom >= col.rect.top and self.rect.bottom >= col.rect.bottom and col.rect.top and self.dirWS == 3:
                self.rect.top = col.rect.bottom
                col.rect.y += -1


                
        for col in second_crate_hit_list:
            if self.rect.left <= col.rect.left and self.rect.left <= col.rect.right and col.rect.left and self.dir == 1:
                self.rect.right = col.rect.left
                col.rect.x += 1
                
            if self.rect.right >= col.rect.left and self.rect.right >= col.rect.right and col.rect.left and self.dir == 2:
                self.rect.left = col.rect.right
                col.rect.x -= 1
                
            if self.rect.top <= col.rect.top and self.rect.top <= col.rect.bottom and col.rect.top and self.dirWS == 4:
                self.rect.bottom = col.rect.top
                col.rect.y += 1
                
            if self.rect.bottom >= col.rect.top and self.rect.bottom >= col.rect.bottom and col.rect.top and self.dirWS == 3:
                self.rect.top = col.rect.bottom
                col.rect.y -= 1

        for col in lava_hit_list:
            self.rect.y = 50
            self.rect.x = 0
            self.timesDied += 1
        
        for col in exit_hit_list:
            self.rect.x = 50
            self.rect.y = 50
            self.timesDied += 1
            
            
        for block in block_hit_list:
            if self.xvelocity > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.yvelocity

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.yvelocity > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
    def draw_image(self):
        pass
        #self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 16, height = 16, color = BLUE):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.imageSurf = pygame.image.load("border.png")
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))
        self.rect.y = y
        self.rect.x = x

                
class Exits(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 16, height = 16, color = BLUE):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.imageSurf = pygame.image.load("enemy.png")
        self.imageSurf.set_alpha(255)
        self.numofenemies = 0
        self.rect = self.image.get_rect()
        self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))
        self.rect.y = y
        self.rect.x = x
        self.dir = randint(1, 4)
        self.dir2 = 0

    def get_enemies(self):
        return self.numofenemies
    
    def set_enemies(self, num):
        self.numofenemies = num
        
    def update(self):
        wall_hit_list = pygame.sprite.spritecollide(self,self.walls, False)
        lava_hit_list = pygame.sprite.spritecollide(self, self.lavas, False)
        crate_hit_list = pygame.sprite.spritecollide(self, self.crate, False)
        dir_crate_list = pygame.sprite.spritecollide(self, self.dir_crate, False)
        #self_hit_list = pygame.sprite.spritecollide(self, self.self_enemy, False)
        """ 1 = left, 2 = right, 3 = up, 4 = bottom"""


        """for col in self_hit_list:
            if self.dir == 1:
                self.dir = 2
            elif self.dir == 2:
                self.dir = 1

            if self.dir == 3:
                self.dir = 4
            elif self.dir == 4:
                self.dir = 3
        """
        for col in wall_hit_list:
            if self.dir == 1:
                self.dir = 2
            elif self.dir == 2:
                self.dir = 1

            if self.dir == 3:
                self.dir = 4
            elif self.dir == 4:
                self.dir = 3

        for col in crate_hit_list:
            if self.dir == 1:
                self.dir = 2
            elif self.dir == 2:
                self.dir = 1

            if self.dir == 3:
                self.dir = 4
            elif self.dir == 4:
                self.dir = 3

        

        
        if self.dir == 1:
            self.rect.x -= 1
        if self.dir == 2:
            self.rect.x += 1
        if self.dir == 3:
            self.rect.y -= 1
        if self.dir == 4:
            self.rect.y += 1

        


            
        
        

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 24, height = 24, color = (0, 255, 0)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.imageSurf = pygame.image.load("grass.png")
        
        

        self.rect = self.image.get_rect()
        self.draw_image()
        self.rect.y = y
        self.rect.x = x
    def draw_image(self):
        self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))

    
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 24, height = 24, color = (255, 0, 255)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.imageSurf = pygame.image.load("lava.png")
                                           
        #adding image here

        self.rect = self.image.get_rect()
        self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))
        self.rect.x = x
        self.rect.y = y

class Crate(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 24, height = 24, color = (255, 0, 0)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.imageSurf = pygame.image.load("crate.png")
        self.rect = self.image.get_rect()
        self.image.blit(self.imageSurf, (self.rect.x, self.rect.y))
        self.rect.x = x
        self.rect.y = y
        self.isMoveable = True

    def update(self):
        local_crate_list = pygame.sprite.spritecollide(self, self.crate, False)



        for col in local_crate_list:
            self.isMoveable = False
class SecondCrate(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 24, height = 24, color = (0, 0, 255)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class CrateExit(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 24, height = 24, color = (0, 0, 255)):
        super().__init__()
        self.image= pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.exitVar = False
    def update(self):
        self_crate_col = pygame.sprite.spritecollide(self, self.crate, False)

        for col in self_crate_col:
            self.exit_level()


    def exit_level(self):
        hasExit = True
        
pygame.init()
pygame.font.init()
displayFont = pygame.font.SysFont("monospace", 15)

display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)

all_sprite_list = pygame.sprite.Group()
enemy_sprite_list = pygame.sprite.Group()
exit_sprite_list = pygame.sprite.Group()
grass_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
player_sprite_list = pygame.sprite.Group()
lava_sprite_list = pygame.sprite.Group()
crate_sprite_list = pygame.sprite.Group()
second_crate_sprite_list = pygame.sprite.Group()
exit_sprite = pygame.sprite.Group()




"""ARRAYS WHICH HOLD THE VALUE FOR THE LEVEL
   0 = GRASS
   1 = KEY BLOCK
   2 = CRATE
   3 = WALL
   4 = ENEMY
   5 = LAVA
   6 = KEYHOLE
"""
level = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3],
    [3, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3],
    [3, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

level2 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

currentlevel = level
numEnem = 0
hasExit = False

"""**LOADING THE TILEMAP USING THE ARGUMENTS 'LEVEL' FOR THE LEVEL YOU WANT TO LOAD**"""

def tilemap(level):
    currentlevel = level
    numEnemies = 0
    for x in range(len(currentlevel)):
        for y in range(len(currentlevel[x])):

            
            if currentlevel[x][y] == 3:
                wall = Wall(x*24, y*24, 24, 24, (255,255,255))
                wall_list.add(wall)
                all_sprite_list.add(wall)

                
            if currentlevel[x][y] == 4:
                Exit = Exits(x*24, y*24, 24, 24, (255, 0, 255))
                numEnemies = numEnemies + 1
                Exit.set_enemies(numEnemies)
            
                floors = Floor(x*24, y*24, 24, 24)
                exit_sprite_list.add(Exit)
                all_sprite_list.add(Exit)
                grass_sprite_list.add(floors)
                Exit.walls = wall_list
                Exit.lavas = lava_sprite_list
                Exit.crate = crate_sprite_list
                Exit.dir_crate = second_crate_sprite_list
                #Exit.self_enemy = exit_sprite_list
                
            if currentlevel[x][y] == 0:
                floors = Floor(x*24, y*24)
                grass_sprite_list.add(floors)

                
            if currentlevel[x][y] == 5:
                lava = Lava(x*24, y*24, 24, 24)
                lava_sprite_list.add(lava)

                
            if currentlevel[x][y] == 2:
                crate = Crate(x*24, y*24, 24, 24, (210,105,30))
                crate.crate = crate_sprite_list
                crate_sprite_list.add(crate)
                floors = Floor(x*24, y*24, 24, 24)
                grass_sprite_list.add(floors)

                
            if currentlevel[x][y] == 1:
                sec_crate = SecondCrate(x*24, y*24, 24, 24)
                second_crate_sprite_list.add(sec_crate)

            if currentlevel[x][y] == 6:
                keyhole = CrateExit(x*24, y*24, 24, 24, (255, 255, 255))
                exit_sprite.add(keyhole)
                keyhole.crate = exit_sprite





clock = pygame.time.Clock()
isRunning = True
haschanged = False
tilemap(level)
player = Player(50, 50)
isDebug = True
timesDied = displayFont.render(str(player.timesDied), 1, (0, 0, 0))
playerDir = displayFont.render(str(player.dir), 1, (0, 0, 0))



"""**START OF THE GAME LOOP**"""


while isRunning and not hasExit:
    

    
    player.walls = wall_list
    player.Exit = exit_sprite_list
    player.lava = lava_sprite_list
    player.crate = crate_sprite_list
    player.sec_crate = second_crate_sprite_list
    
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        tilemap(level2)
                
    if keys[pygame.K_w]:
        player.dirWS = 3
        player.yvelocity = -5
        
    if not keys[pygame.K_w]:
        player.dirWS = 0
        player.yvelocity = 0
        

    if keys[pygame.K_s]:
        player.yvelocity = 5
        player.dirWS = 4
    if not keys[pygame.K_s] and not keys[pygame.K_w]:
        player.dirWS = 0
        player.yvelocity = 0


    if keys[pygame.K_a]:
        player.dir = 2
        player.xvelocity = -5
    if not keys[pygame.K_a]:
        player.dir = 0
        player.xvelocity = 0

    if keys[pygame.K_d]:
        player.dir = 1
        player.xvelocity = 5
    if not keys[pygame.K_d] and not keys[pygame.K_a]:
        player.dir = 0
        player.xvelocity = 0
        
    


    
    if keys[pygame.K_ESCAPE]:
        isRunning = False

    player_sprite_list.add(player)
    display.fill(BLACK)
    player_sprite_list.update()
    crate_sprite_list.update()    
    all_sprite_list.update()
    second_crate_sprite_list.update()
    exit_sprite.update()

    
    grass_sprite_list.draw(display)
    lava_sprite_list.draw(display)
    crate_sprite_list.draw(display)
    player_sprite_list.draw(display)
    second_crate_sprite_list.draw(display)
    exit_sprite.draw(display)
    all_sprite_list.draw(display)



    if isDebug:        
        display.blit(timesDied, (10, 10))
        display.blit(playerDir, (10, 20))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
        





        
