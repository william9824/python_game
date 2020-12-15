import pygame
import os
pygame.font.init()
import random
import time

# Window setting
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load image
RED_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Load laser
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background & Scaling (OS_PATH , SCALE DIMENSION)
BKG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),(WIDTH,HEIGHT))


# Blueprint of ship; attribute (POS, HP, IMG, LASER , CD)
class Ship:
    COOLDOWN = 15

    def __init__(self, x, y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        # pygame.draw.rect(window,(255,0,0),(self.x, self.y, 50, 50))  * RED BOX FOR TEST *
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            # Write sth here #

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.laser.append(laser) # add to list
            self.cool_down_counter = 1

    def get_height(self): # Get ship grid  * edge position *
        return self.ship_img.get_height()

    def get_width(self): # Get ship grid * edge position *
        return self.ship_img.get_width()


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window): # Update frame
        window.blit(self.img, (self.x, self.y))

    def move(self, vel): # Go down side
        self.y += vel

    def off_screen(self, height):
        return self.y < height and self.y >= 0

    def collision(self, obj):
        return collide(obj, self)

class Enemy(Ship):
    COLOR_MAPPING = { # Create a mapping list
        "RED": (RED_SHIP, RED_LASER),
        "GREEN": (GREEN_SHIP, GREEN_LASER),
        "BLUE" : (BLUE_SHIP, BLUE_LASER),
    }

    def __init__(self,x,y,color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAPPING[color] # Match the mapping list | e.g. * COLOR_MAPPING[RED] *
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel # Go down


# Player Ship
class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x, y, health) # Super
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # hit box 
        self.max_health = health


def collide(obj1, obj2): # Overlap for offset: obj1's coordinate - obj2's coordinate
    offset_x = obj1.x - obj2.x
    offset_y = obj1.y - obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None # if not overlaping -> None | if overlapping -> (x,y)

# Control flow - main function
def main():
    run = True  # start
    main_font = pygame.font.SysFont("comicsans", 45)
    lost_font = pygame.font.SysFont("comicsans", 50)
    lost = False
    lost_count = 0
    level = 0
    lives = 5
    FPS = 60 # FPS, Game Speed



    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5 # Velocity

    player = Player(300,650)

    clock = pygame.time.Clock()

    # redraw Window
    def redraw_window(): # Rendering procession
        WIN.blit(BKG,(0,0))  # Coordinate Stuff : From left-top to right-bottom
        # draw text
        lifes_label = main_font.render(f"lives: {lives}", 1, (255,255,255)) # F-string
        level_label = main_font.render(f"level: {level}", 1, (255,255,255)) # F-string

        WIN.blit(lifes_label,(10,10)) # POS( x+10, y+10 ) : Top-left
        WIN.blit(level_label,(WIDTH - level_label.get_width() - 10, 10)) # POS( TOP_RIGHT - 10 , 10 ) : Top-right

        for enemy in enemies: # Enemy class inherits "Ship.draw()"
            enemy.draw(WIN)

        if lost:
            lost_label = lost_font.render("Lost", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2 , HEIGHT/2)) # Put it Center : Window Center - Label's Center

        player.draw(WIN)

        pygame.display.update()



    while run:  # start
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0: # Are you lost?
            lost = True
            lost_count += 1

        if lost:
           if lost_count > FPS * 5: # Frame Per Second: 1Sec = 60 Frame | FPS * n = nSec : Timer
               run = False
           else:
                continue # Go back to beginning of while loop -> "while run"

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length): # Spawn Randomly instead of coming down at the same time
                enemy = Enemy(random.randrange(80, WIDTH-100), random.randrange(-1500, - 100), random.choice(["RED", "GREEN", "BLUE"]) ) # x,y { 80 ~ WIDTH (WIDTH -100), (-1200 ~ -120 ) }
                enemies.append(enemy) # add to list


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Quit Game while pressing "X"

        # Player Movement control && Stay in the grid(Window) :  * Coordinate system starts from LEFT-TOP corner *
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0 : # Go left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH : # Go right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0 : # Go up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT : # Go down
            player.y += player_vel
        if keys[pygame.K_s]:
            player.shoot()

        for enemy in enemies[:]: # Copy Enemy list, So it doesnt affect "list: enemies" -- Not necessary but safer --
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT: # Enemies go outside the window
                lives -= 1
                enemies.remove(enemy) # Destroy object


main()
