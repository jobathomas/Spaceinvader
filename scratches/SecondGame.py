import sys
import pygame
import random

# initialise pygame objects
pygame.init()

#  specify screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#  create pygame screen

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# set game caption
pygame.display.set_caption('Space invaders')

# load background images
menu_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/space2.png")
menu_image = pygame.transform.scale(menu_image,(SCREEN_WIDTH,SCREEN_HEIGHT))


bg_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/space2.png")

bg_image = pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))


#  set game icon
gameIcon = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/icon.jpg")
pygame.display.set_icon(gameIcon)

PLAYER_WIDTH = 50


# load game sounds
missile_sfx = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/missile.wav")
missile_sfx.set_volume(0.2)
damage = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/explosion2.mp3")
game_over = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/gameover.mp3")
gun = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/raygun.wav")
explosion_sound = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/explosion.mp3")
explosion2_sound = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/gameover.mp3")

# create clock object
clock = pygame.time.Clock()


#  load player image
player_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/icon.jpg")

enemy_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/enemy.png")
enemy_image = pygame.transform.scale(enemy_image,(50,50))

bullet_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/storm_shadow.png")

# load ammo image

ammo_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/ammo.png")
ammo_image= pygame.transform.scale(ammo_image,(50,50))

ammo_sfx_load = pygame.mixer.music.load("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/reload.mp3")

#  load pause screen image
pause_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/space.jpg")
pause_image = pygame.transform.scale(pause_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
# UI sfx
click = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/click.mp3")
loading_music = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/loading.mp3")
scroll_sfx = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/scroll.mp3")

#  define colours

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

position = 0

#  writing main game code
def background(speed):
    global position
    screen.blit(bg_image,(0,position))
    screen.blit(bg_image,(0,-SCREEN_HEIGHT + position))

    position += speed

    if position > SCREEN_HEIGHT:
       position = 0





class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = pygame.transform.scale(player_image,(50,50))
        self.rect = self.image.get_rect()  #  Creates a rectangle from the image
        self.rect.topleft = (x,y) # Specifies lcoation of rectangle
        self.velocity = 7
        self.health_start = health
        self.health_remaining = health
        self.previous_time = pygame.time.get_ticks()  # when an instance of Spaceship is created, the time is recorded here
        self.score_font = pygame.font.SysFont('ebrima', 40) # create font object
        self.score = 0
        self.ammo_font = pygame.font.SysFont('arial',40) # create font object
        self.ammo = 10


    #  overriding "update" method in Sprite class

    def update(self):


        #  get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x-= self.velocity
        if key[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x+= self.velocity





        #  draw health bar
        pygame.draw.rect(screen,red,pygame.Rect(self.rect.x,self.rect.y + 50,self.rect.width,10,))
        if self.health_remaining >0:
            pygame.draw.rect(screen, green, pygame.Rect(self.rect.x, self.rect.y + 50,
                                                        int(self.rect.width *(self.health_remaining/self.health_start)),10))
        current_time = pygame.time.get_ticks()
        cooldown = 500

        if key[pygame.K_SPACE] and current_time - self.previous_time > cooldown and self.ammo >0:
            self.ammo -= 1
            bullet1 = Bullets(spaceship.rect.centerx - 5, spaceship.rect.centery)
            bullet_group.add(bullet1)
            gun.play(maxtime=350)
            # record current time
            self.previous_time = current_time # timer reset

        if self.health_remaining <=0:
            self.kill()




        # update mask - in update function so mask moves as spaceship moves from left to right
        self.mask = pygame.mask.from_surface(self.image)
        self.player_score()
        self.ammo_update()

    def player_score(self):
        #  add score text to screen
        self.text = self.score_font.render(f'Score:{self.score}', True, 'white')  # create text surface object
        self.textRect = self.text.get_rect(topleft=(10, 10))  # create rectangle from text surface object
        screen.blit(self.text, self.textRect)  # copy surface onto screen surface

    def ammo_update(self):
        self.ammo_text = self.ammo_font.render(f'Missiles: {self.ammo}', True,'white')
        self.ammo_rect = self.ammo_text.get_rect(topleft = (SCREEN_WIDTH - 200,10))
        screen.blit(self.ammo_text,self.ammo_rect)


#  create sprite group
player_group = pygame.sprite.Group()
#  create spaceship object
spaceship = Spaceship(SCREEN_WIDTH/2,SCREEN_HEIGHT - (PLAYER_WIDTH*2),5) # create spaceship object of spaceship class
player_group.add(spaceship) #  add spaceship object to spaceship sprite group

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(enemy_image,180)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velocity = 7
        self.active = True

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = -5
            self.velocity += 0.2
            self.active = True
        if self.rect.y <=20:
            missile_sfx.play(0,350)
        self.check_collision()
        if self.velocity > 16:
            self.velocity = 16



    def check_collision(self):
        if pygame.sprite.spritecollide(self,player_group,False, pygame.sprite.collide_mask) and self.active: # pygame collision check is
                                                                                             # rectangular by default
            # checks whether the rect of one sprite intersects with the rect of another sprite
            damage.play(maxtime=260)
            spaceship.health_remaining-=1
            self.active = False  # deactivates missile to prevent duplicate collisions





# create enemy sprite group
enemy_group = pygame.sprite.Group()
# create missile object
for i in range(8):
    missile = Enemy(random.randint(0,SCREEN_WIDTH),0)
    enemy_group.add(missile) # add 8 missiles to enemy sprite group

class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y,):
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = bullet_image
        self.rect = self.image.get_rect()  #  Assigns image to rectangle
        self.rect.topleft = (x,y) # Specifies lcoation of rectangle


    def update(self):
        self.rect.y-=5
        if self.rect.bottom < 0:
            self.kill()
        self.check_collision()


    def check_collision(self):
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            explosion = Explosion(self.rect.centerx,self.rect.centery,2)
            explosion_group.add(explosion)
            explosion_sound.play()
            spaceship.score +=1


bullet_group = pygame.sprite.Group()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/exp{num}.png")
            if size == 1:
                pygame.transform.scale(img,(20,20))
            if size == 2:
                pygame.transform.scale(img,(40,40))
            if size == 3:
                pygame.transform.scale(img,(40,40))
            # add image to list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation - (explosion_speed - self.counter is interval between images)
        self.counter += 1

        # condition prevents from list index being out of range - self.index must be less than 5-1 (4), which represents
        # the final image in self.images
        # if counter is greater than explosion_speed, move onto next image in list
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if animation complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()

def enemy_replenish():


    if len(enemy_group) < 2:
        explosion2_sound.play()
        for i in range(10):
            missile = Enemy(random.randint(0, SCREEN_WIDTH), -20)
            enemy_group.add(missile)  # add 8 missiles to enemy sprite group
            missile.velocity += 2.25


class Ammo(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ammo_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velocity = 12


    def update(self):

        self.rect.y += self.velocity



        if self.rect.y > SCREEN_HEIGHT :
            self.kill()

        self.collision()


    def collision(self):
       if pygame.sprite.spritecollide(self,player_group, False,pygame.sprite.collide_mask):
            pygame.mixer_music.play()
            spaceship.ammo +=3
            self.kill()




ammo_group = pygame.sprite.Group()
ammo = Ammo(random.randint(50,SCREEN_WIDTH),0)
ammo_group.add(ammo)


previous_time = pygame.time.get_ticks()
cooldown = 15000 # 15 seconds

def ammo_replenish():
    global previous_time
    current_time = pygame.time.get_ticks()
    if current_time - previous_time >= cooldown:
        ammo2 = Ammo(random.randint(50, SCREEN_WIDTH), 0)
        ammo_group.add(ammo2)
        previous_time = current_time




# writing screen UI code


#  creating button class
class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.font = pygame.font.SysFont('arial',30)  # creates a font object loaded from system fonts
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center =(self.x_pos,self.y_pos)) #  creating rect from image
        self.text_input = text_input
        self.text = self.font.render(self.text_input,True,'white')
        self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))


    def draw(self):
        screen.blit(self.image,(self.rect))  # blit image onto screen in the location of self.rect
        screen.blit(self.text,self.text_rect) # blit text onto screen in location of text_rect

    def check_for_input(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True











    def change_colour(self, position):
        global button_width, button_height

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, 'red')

        else:
            self.text = self.font.render(self.text_input, True, 'white')







def play():

    theme = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/backgroundmusic.mp3")
    theme.set_volume(1)
    theme.play(-1)  # music will play indefinitely with -1 arg

    speed = 5

    while True:

        pygame.display.set_caption('Space Invader')

        #  drawing background image onto screen
        background(speed)

        speed +=0.002

        if speed >= 15:
            speed = 15
        if spaceship.health_remaining <=0:

            game_over()

        clock.tick(60)

        enemy_replenish()

        ammo_replenish()


        #  draw sprite groups
        for spritegrp in [player_group,enemy_group,bullet_group,explosion_group,ammo_group]:
            spritegrp.update()
            spritegrp.draw(screen)



        #  Event handler code
        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.mixer.pause()
            pause()









        pygame.display.update()



button_width = 300
button_height = 200

button_surface = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/button1.png")
button_surface = pygame.transform.scale(button_surface,(button_width,button_height))

play_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT/4, 'PLAY')
options_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 'OPTIONS')
quit_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150, 'QUIT')

def pause():

    pygame.display.set_caption('Pause')

    while True:

        screen.blit(pause_image,(0,0))



        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_k]:
            pygame.mixer.unpause()
            play()





        pygame.display.update()


def game_over():

    while True:

        pygame.mixer.stop()

        screen.fill((0,0,0))




        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()


def main_menu():
    pygame.display.set_caption('Menu')
    loading_music.play(-1)


    while True:

        background(0.25)

        for button in [play_button,options_button,quit_button]:
            button.change_colour(pygame.mouse.get_pos())
            button.draw()



        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(pygame.mouse.get_pos()):
                    click.play()
                    loading_music.stop()
                    pygame.time.delay(600)
                    play()
                if options_button.check_for_input(pygame.mouse.get_pos()):
                    pass
                if quit_button.check_for_input(pygame.mouse.get_pos()):
                    sys.exit()



        pygame.display.update()




main_menu()

