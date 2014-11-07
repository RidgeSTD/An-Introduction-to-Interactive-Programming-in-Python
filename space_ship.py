#coding:utf-8

# http://www.codeskulptor.org/#user38_xE2LOCfokU_8.py
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
acceleration = 0.3
rotate_speed = 0.1
retard_ratio = 0.04
friction_ratio = 0.02
missile_speed = 10

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# ship thrusting
ship_trust_info = ImageInfo([135, 45], [90, 90], 35)

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    # print('get cos='+str(math.cos(ang))+' sin='+str(math.sin(ang)))
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.retard = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.info = info
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def update(self):
        global acceleration
        global rotate_speed
        global friction_ratio
        global retard_ratio
        global WIDTH
        global HEIGHT
        global ship_trust_info
        ship_thrust_sound

        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] = (1-friction_ratio)*self.vel[0] + acceleration*forward[0]
            self.vel[1] = (1-friction_ratio)*self.vel[1] + acceleration*forward[1]
            self.image_center = ship_trust_info.get_center()
            self.image_size = ship_trust_info.get_size()
        elif self.retard:
            self.vel[0] = self.vel[0]*(1-friction_ratio-retard_ratio)
            self.vel[1] = self.vel[1]*(1-friction_ratio-retard_ratio)
            self.image_center = self.info.get_center()
            self.image_size = self.info.get_size()
        else:
            self.vel[0] = self.vel[0]*(1-friction_ratio)
            self.vel[1] = self.vel[1]*(1-friction_ratio)
            self.image_center = self.info.get_center()
            self.image_size = self.info.get_size()

        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0]+self.vel[0]+WIDTH)%WIDTH
        self.pos[1] = (self.pos[1]+self.vel[1]+HEIGHT)%HEIGHT

    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        # if sound:
        #     sound.rewind()
        #     sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0]+self.vel[0]+WIDTH)%WIDTH
        self.pos[1] = (self.pos[1]+self.vel[1]+WIDTH)%WIDTH

           
def draw(canvas):
    global time
    global lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('LIFE:'+str(lives), [30,60], 25, 'white')
    canvas.draw_text('SCORE:'+str(score), [600,60], 25, 'white')

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    x = random.randint(0,WIDTH+1)
    y = random.randint(0,HEIGHT+1)
    a_rock.pos = [x,y]
    a_rock.angle_vel = random.random()*0.4-0.2
    a_rock.vel[0] = random.random()*3-1.5
    a_rock.vel[1] = random.random()*3-1.5


def keydown_handler(key):
    global missile_speed
    if chr(key)=='&':
        #up
        if not my_ship.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        my_ship.thrust = True
    elif chr(key)=='(':
        #down
        my_ship.retard = True
    elif chr(key)=='%':
        #left
        my_ship.angle_vel = -0.1
    elif chr(key)=='\'':
        #right
        my_ship.angle_vel = 0.1
    elif chr(key)==' ':
        #space
        forward = angle_to_vector(my_ship.angle)
        a_missile.pos[0] = my_ship.pos[0]+45*forward[0]
        a_missile.pos[1] = my_ship.pos[1]+45*forward[1]
        a_missile.vel[0] = my_ship.vel[0]+missile_speed*forward[0]
        a_missile.vel[1] = my_ship.vel[1]+missile_speed*forward[1]
        missile_sound.rewind()
        missile_sound.play()
    else:
        pass
    
def keyup_handler(key):
    if chr(key)=='&':
        #up
        if my_ship.thrust:
            ship_thrust_sound.pause()
        my_ship.thrust = False
    elif chr(key)=='(':
        #down
        my_ship.retard = False
    elif chr(key)=='%':
        #left
        my_ship.angle_vel=0
    elif chr(key)=='\'':
        #right
        my_ship.angle_vel = 0
    elif chr(key)==' ':
        #space TODO
        pass
    else:
        pass
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([-1,-1], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
