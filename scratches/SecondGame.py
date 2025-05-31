import sys

import pygame
import random

from pygame.sprite import collide_mask

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

bg_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/space2.png")

bg_image = pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))

options_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/options.jpg")
options_image = pygame.transform.scale(options_image,(SCREEN_WIDTH,SCREEN_HEIGHT))

#  set game icon
gameIcon = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/icon.jpg")
pygame.display.set_icon(gameIcon)

PLAYER_WIDTH = 50


# load game sounds
missile_sfx = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/missile.wav")
missile_sfx.set_volume(0)

laser_sfx = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/laser.mp3")
laser_sfx.set_volume(0.4)

damage = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/explosion2.mp3")
game_over_sfx = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/gameover.mp3")
gun = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/raygun.wav")
explosion_sound = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/explosion.mp3")
explosion2_sound = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/gameover.mp3")

# create clock object
clock = pygame.time.Clock()

#  load player image
player_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/icon.jpg")

enemy_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/enemy.png")
enemy_image = pygame.transform.scale(enemy_image,(100,100))
enemy_image = pygame.transform.rotate(enemy_image,180)

bullet_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/storm_shadow.png")

spritesheet = pygame.image.load('C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/enemy.png').convert_alpha()

spritesheet = pygame.transform.scale(spritesheet,(400,100))

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


#  writing main game code

class Background():

    def __init__(self,image,speed):
        self.image = image
        self.speed = speed
        self.position = 0
        self.screen_height = SCREEN_HEIGHT


    def draw(self):
        screen.blit(self.image,(0,self.position))
        screen.blit(self.image,(0,-self.screen_height + self.position))

        self.position += self.speed

        if self.position > self.screen_height:
           self.position = 0


class Spaceship(pygame.sprite.Sprite):

    def __init__(self,x,y,health): # constructor method
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = pygame.transform.scale(player_image,(50,50))
        self.rect = self.image.get_rect()  #  Creates a rectangle from the image
        self.rect.topleft = (x,y) # Specifies lcoation of rectangle
        self.velocity = 7 # specifies
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
        pygame.draw.rect(screen,'red',pygame.Rect(self.rect.x,self.rect.y + 50,self.rect.width,10,))
        if self.health_remaining >0:
            pygame.draw.rect(screen, 'green', pygame.Rect(self.rect.x, self.rect.y + 50,
                                                        int(self.rect.width *(self.health_remaining/self.health_start)),10))
        current_time = pygame.time.get_ticks()
        cooldown = 500

        if key[pygame.K_SPACE] and current_time - self.previous_time > cooldown and self.ammo >0:
            gun.play(maxtime=350)
            self.ammo -= 1
            bullet1 = Bullets(self.rect.centerx - 5, self.rect.centery,bullet_image)

            bullet_group.add(bullet1)
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
player_health = 5
#  create spaceship object
spaceship = Spaceship(SCREEN_WIDTH/2,SCREEN_HEIGHT - (PLAYER_WIDTH*2),player_health) # create spaceship object of spaceship class
player_group.add(spaceship) #  add spaceship object to spaceship sprite group


alien_image = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/killer.png")

alien_laser = pygame.image.load("C:/Users/jobat/OneDrive/Desktop/GAME/Sprite images/laser.png")
alien_laser = pygame.transform.scale(alien_laser,(25,25))
alien_laser = pygame.transform.rotate(alien_laser,90)

moving = True
aggression_start = pygame.time.get_ticks()


class Alien(pygame.sprite.Sprite):
    def __init__(self,x,y,health,cooldown):
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = pygame.transform.scale(alien_image,(50,50)) # scale down image
        self.rect = self.image.get_rect()  #  Creates a rectangle with same dimensions as image
        self.rect.topleft = (x,y) # Specifies lcoation of rectangle
        self.health_start = health
        self.health_remaining = health
        self.previous_time = pygame.time.get_ticks()  # when an instance of Spaceship is created, the time is recorded here
        self.moving = True
        self.aggression_start = pygame.time.get_ticks()
        self.start = pygame.time.get_ticks()
        self.cooldown = cooldown



    def update(self):

        # code for moving from left to right


        if self.rect.x <= 0:
            self.moving = False

        elif self.rect.x >= SCREEN_WIDTH - 50:
            self.moving = True

        # health bar code

        pygame.draw.rect(screen, 'red', pygame.Rect(self.rect.x, self.rect.y + 50, self.rect.width, 7, ))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, 'green', pygame.Rect(self.rect.x, self.rect.y + 50,
                                                          int(self.rect.width * (
                                                                      self.health_remaining / self.health_start)), 7))
        if self.moving == True:
            self.rect.x -=5
        else:
            self.rect.x += 5

        if self.health_remaining <=-0:
            self.kill()


        self.movement()
        self.shoot()
        self.collision()



    def movement(self):

        evolution = 5000 # every 5 seconds, move down screen


        self.aggression_current = pygame.time.get_ticks()
        if self.aggression_current - self.aggression_start >= evolution:
            if self.rect.y <= SCREEN_HEIGHT:

                self.rect.y += 10
                self.aggression_start= self.aggression_current


        if self.rect.y >= SCREEN_HEIGHT - 50:
            self.aggression_start = self.aggression_current

    def shoot(self):


        self.current = pygame.time.get_ticks()

        if self.current - self.start >= self.cooldown:
            laser_1 = AlienLaser(self.rect.centerx-5,self.rect.centery-20,alien_laser)
            alien_laser_group.add(laser_1)

            laser_sfx.play()
            self.start = self.current
        if len(enemy_group) <=2:
            self.cooldown = 500
        else:
            self.cooldown = 1000


    def collision(self):

        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.health_remaining -=1
            self.image = pygame.transform.scale(alien_image, (100, 100))
            self.image = pygame.transform.scale(alien_image, (50, 50))
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            explosion_sound.play(maxtime=1000)



class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = image
        self.rect = self.image.get_rect()  # Assigns image to rectangle
        self.rect.topleft = (x, y)  # Specifies lcoation of rectangle

    def update(self):

        self.rect.y +=20
        # eliminate lasers that have left the screen to avoid irrelevant processing
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()

        self.check_collision()

        # code for when player missile collides with meteorites

    def check_collision(self):
        if pygame.sprite.spritecollide(self, player_group, False,pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            explosion_sound.play(maxtime=1000)
            spaceship.health_remaining -=1

alien_laser_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

for i in range(2):
    alien_ship = Alien(random.randint(0,SCREEN_WIDTH),10,10,1000)
    alien_group.add(alien_ship)


# create function for meteor/enemy animation
def get_image(sheet, frame, width, height):

    image = pygame.Surface((width, height)).convert_alpha()  # create image surface
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))  # blit spritesheet image onto image surface
    image.set_colorkey('black') # makes image transparent

    return image


frame_0 = get_image(spritesheet, 0, 50, 100)
frame_1 = get_image(spritesheet, 1, 50, 100)
frame_2 = get_image(spritesheet, 2, 50, 100)
frame_3 = get_image(spritesheet, 3, 50, 100)
frame_4 = get_image(spritesheet, 4, 50, 100)
frame_5 = get_image(spritesheet, 5, 50, 100)
frame_6 = get_image(spritesheet, 6, 50, 100)
frame_7 = get_image(spritesheet, 7, 50, 100)

frames = [frame_0,frame_1, frame_2,frame_3,frame_4,frame_5,frame_6,frame_7]








class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,velocity):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(len(frames)):
            img = frames[i]
            self.animation_list.append(img) # add each frame variable to animation list
        self.image = self.animation_list[self.frame_index] # set self.image to element/frame in list
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velocity = velocity
        self.active = True

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 50

        #check if enough time has passed since last update


        # update image depending on frame
        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


        # if animation has run out then reset back to the start





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
        self.update_animation()
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
for i in range(4):
    missile = Enemy(random.randint(0,SCREEN_WIDTH),0,10)
    enemy_group.add(missile) # add 8 missiles to enemy sprite group

# create 2nd set of missile objects moving at different speed
for i in range(4):
    missile2 = Enemy(random.randint(0, SCREEN_WIDTH), 0, 12)
    enemy_group.add(missile2)  # add 8 missiles to enemy sprite group


class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)  # Call sprite initialiser
        self.image = image
        self.rect = self.image.get_rect()  #  Assigns image to rectangle
        self.rect.topleft = (x,y) # Specifies lcoation of rectangle



    def update(self):


        self.rect.y -=8
        if self.rect.bottom < 0:
            self.kill()

        self.check_collision()


    def check_collision(self):
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            explosion = Explosion(self.rect.centerx,self.rect.centery,2)
            explosion_group.add(explosion)
            explosion_sound.play(maxtime=1000)
            spaceship.score += 1











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

    explosion2_sound.play()
    for i in range(5):
        missile = Enemy(random.randint(0, SCREEN_WIDTH), -20,7)
        enemy_group.add(missile)  # add 8 missiles to enemy sprite group
        missile.velocity +=6
    for i in range(5):
        missile = Enemy(random.randint(0, SCREEN_WIDTH), -20,7)
        enemy_group.add(missile)  # add 8 missiles to enemy sprite group
        missile.velocity +=5



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
            spaceship.ammo +=10
            self.kill()





ammo_group = pygame.sprite.Group()
ammo = Ammo(random.randint(50,SCREEN_WIDTH),0)
ammo_group.add(ammo)


previous_time = pygame.time.get_ticks()
regeneration_time = 15000 # 15 seconds

def ammo_replenish():
    global previous_time
    current_time = pygame.time.get_ticks()
    if current_time - previous_time >= regeneration_time:
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
        #pygame.draw.rect(screen, 'red',self.rect,2)

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






theme = pygame.mixer.Sound("C:/Users/jobat/OneDrive/Desktop/GAME/SFX/backgroundmusic.mp3")
theme.set_volume(0.7)

play_bg = Background(bg_image, 5)


enemy_reload = pygame.time.get_ticks()

def play():

    global return_menu

    theme.play(-1)  # music will play indefinitely with -1 arg


    while True:

        if return_menu:
            return



        play_bg.draw()

        pygame.display.set_caption('Space Invader')

        #  drawing background image onto screen


        play_bg.speed +=0.004


        if play_bg.speed >= 18:
            play_bg.speed = 18
            for x in [missile, missile2]:
                x.velocity +=2

        if spaceship.health_remaining <=0:
            pygame.mixer.stop()
            game_over_sfx.play()
            pygame.time.delay(1400)
            game_over()






        clock.tick(60)

        current_time = pygame.time.get_ticks()
        if len(enemy_group) <=0:
            if current_time - enemy_reload >= 5000:
                print(current_time - enemy_reload)
                enemy_replenish()
                current_time = enemy_reload

        ammo_replenish()


        #  draw sprite groups
        for spritegrp in [player_group,enemy_group,bullet_group,explosion_group,ammo_group,alien_group,alien_laser_group]:
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




def pause():

    pygame.display.set_caption('Pause')

    while True:

        screen.blit(pause_image,(0,0))

        resume_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 'RESUME')
        quit_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 'QUIT')

        for buttons in [resume_button,quit_button]:
            buttons.change_colour(pygame.mouse.get_pos())
            buttons.check_for_input(pygame.mouse.get_pos())
            buttons.draw()



        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.check_for_input(pygame.mouse.get_pos()):
                    scroll_sfx.play()
                    pygame.time.delay(200)
                    pygame.mixer.unpause()
                    return
                elif quit_button.check_for_input(pygame.mouse.get_pos()):
                    scroll_sfx.play()
                    pygame.time.delay(200)
                    sys.exit()

        pygame.display.update()

def options():

    options_bg = Background(options_image,0)
    back_button = Button(button_surface, SCREEN_WIDTH / 2, button_height / 2.5, 'BACK')


    pygame.display.set_caption('Options')

    while True:

        options_bg.draw()

        back_button.draw()
        back_button.change_colour(pygame.mouse.get_pos())



        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    scroll_sfx.play()
                    return # return keyword exits function



        pygame.display.update()


current_state = ''

return_menu = ''

def game_over():
    global current_state, return_menu, best_score

    current_state = 'GAME OVER'




    quit_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT/2.5, 'QUIT')
    restart_button = Button(button_surface,SCREEN_WIDTH/2,SCREEN_HEIGHT/1.5,'RESTART')
    menu_button = Button(button_surface,SCREEN_WIDTH/2,SCREEN_HEIGHT - 60,'MAIN MENU')

    font = pygame.font.SysFont('ebrima', 40)  # create font object
    text = font.render('GAME OVER', True, 'white')  # create text surface object
    text_rect = text.get_rect(topleft=(SCREEN_WIDTH/2 - 100, 100))  # create rectangle from text surface object


    while True:

        pygame.mixer.stop()

        screen.fill((0,0,0))

        screen.blit(text, text_rect)  # copy surface onto screen surface

        for element in [restart_button, quit_button,menu_button]:
            element.draw()
            element.change_colour(pygame.mouse.get_pos())

        if spaceship.score > best_score: # updating high score
            best_score = spaceship.score



        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(pygame.mouse.get_pos()):
                    scroll_sfx.play()
                    pygame.time.delay(200)
                    sys.exit()
                elif restart_button.check_for_input(pygame.mouse.get_pos()):
                    scroll_sfx.play()
                    pygame.time.delay(200)
                    spaceship.health_remaining = player_health
                    play_bg.speed = 5
                    spaceship.score = 0
                    spaceship.ammo = 10
                    spaceship.rect.x = SCREEN_WIDTH / 2
                    alien_group.empty()
                    enemy_group.empty()
                    for i in range(2):
                        alien_ship = Alien(random.randint(0, SCREEN_WIDTH), 10, 10, 1000)
                        alien_group.add(alien_ship)
                    for i in range(4):
                        missile = Enemy(random.randint(0, SCREEN_WIDTH), 0, 10)
                        enemy_group.add(missile)  # add 8 missiles to enemy sprite group
                    # create 2nd set of missile objects moving at different speed
                    for i in range(4):
                        missile2 = Enemy(random.randint(0, SCREEN_WIDTH), 0, 12)
                        enemy_group.add(missile2)  # add 8 missiles to enemy sprite group
                    theme.play(-1)
                    return
                elif menu_button.check_for_input(pygame.mouse.get_pos()):
                    return_menu = True
                    loading_music.play(-1)
                    spaceship.health_remaining = player_health
                    play_bg.speed = 5
                    spaceship.score = 0
                    spaceship.ammo = 10
                    spaceship.rect.x = SCREEN_WIDTH / 2
                    alien_group.empty()
                    enemy_group.empty()
                    for i in range(2):
                        alien_ship = Alien(random.randint(0, SCREEN_WIDTH), 10, 10, 1000)
                        alien_group.add(alien_ship)
                    for i in range(4):
                        missile = Enemy(random.randint(0, SCREEN_WIDTH), 0, 10)
                        enemy_group.add(missile)  # add 8 missiles to enemy sprite group
                    # create 2nd set of missile objects moving at different speed
                    for i in range(4):
                        missile2 = Enemy(random.randint(0, SCREEN_WIDTH), 0, 12)
                        enemy_group.add(missile2)  # add 8 missiles to enemy sprite group

                    return



        pygame.display.update()


best_score = 0

def high_score_text():

    global best_score
    high_score_font = pygame.font.SysFont('ebrima', 40)  # create font object
    text = high_score_font.render(f'Your high score is: {best_score} kills!', True, 'white')  # create text surface object
    text_rect = text.get_rect(topleft=(10, 10))  # create rectangle from text surface object
    screen.blit(text,text_rect)  # copy/paste surface onto screen surface





def main_menu():
    global current_state, return_menu

    current_state = 'MAIN MENU'     # separating code into game states
    # for some reason main menu code affects game_over code

    pygame.display.set_caption('Menu')
    loading_music.play(-1)
    menu_bg = Background(bg_image,0.25)

    play_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 'PLAY')
    options_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 'OPTIONS')
    quit_button = Button(button_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150, 'QUIT')


    while True:

        if return_menu == True:
            return_menu = False # prevents returning to menu infintely when already returned to menu


        menu_bg.draw()

        current_state = "MAIN MENU"

        high_score_text()



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
                    scroll_sfx.play()
                    options()
                if quit_button.check_for_input(pygame.mouse.get_pos()) and current_state == 'MAIN MENU':
                    scroll_sfx.play()
                    pygame.time.delay(200)
                    sys.exit()




        pygame.display.update()


main_menu()