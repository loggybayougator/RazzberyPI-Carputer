import pygame
from pygame.locals import *
import math
import time
import obd
from obd import OBDStatus
from time import sleep
from picamera import PiCamera

pygame.init()

#########
pygame.mouse.set_visible(False)
camera = PiCamera()
camera.start_preview()
camera.preview.alpha = 0

fule = 100
background = (53, 44, 109)
#########

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_w = screen.get_width()
screen_h = screen.get_height()
time_radian = 50
circle_y = screen_h / 2
circle_y2 = int((screen_h / 4) * 2.9)
circle1_x = screen_w * .25
circle2_x = screen_w * .5
circle3_x = screen_w * .75
circle4_x = int(screen_w * .3745318352)
circle_rad = (circle2_x - circle1_x) / 2

circle5_x = int(screen_w * .6254681648)

rpm_text_x = screen_w * .25
rpm_text_y = screen_h * .25
speed_text_x = screen_w * .5
speed_text_y = screen_h * .25
load_text_x = screen_w * .75
load_text_y = screen_h * .25
headerFont = pygame.font.SysFont('Tahoma', 50)
digitFont = pygame.font.SysFont('Tahoma', 45)
numberFont = pygame.font.SysFont('Tahoma', 10)
timeFont = pygame.font.SysFont('Tahoma', 20)
white = (255, 255, 255)
offwhite = (200,200,200)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
vcolor = green
grey = (112, 128, 144)
red = (255, 0, 0)
blue = (0, 0, 255)
speed = 0
rpm = 0
load = 0
angle = 5.4
posit = []
#pie is exactly 3
raspberry = 3.141592653

for s in range (0,60):
    pos = [int(math.cos(math.radians(s*6+270))*time_radian+circle4_x),int(math.sin(math.radians(s*6+270))*time_radian+circle_y2)]
    posit.append(pos)

def getHour():
    curHour = time.strftime('%I') 
    return curHour
def getMin():
    curMin = time.strftime('%M')
    return curMin
def getSec():
    curSec = time.strftime('%S')
    return curSec

def draw_hud():
    screen.fill(background)
    pygame.draw.circle(screen, black, (int(circle4_x), int(circle_y2)), (int(time_radian)+4), 5)


    if fule > 50:
        pygame.draw.circle(screen, green, (int(circle5_x), int(circle_y2)), 50)
    elif fule > 25:
        pygame.draw.circle(screen, yellow, (int(circle5_x), int(circle_y2)), 50)
    elif fule < 25:
        pygame.draw.circle(screen, red, (int(circle5_x), int(circle_y2)), 50)
    pygame.draw.circle(screen, black, (int(circle5_x), int(circle_y2)), (int(time_radian)+4), 5)
    

    
    pygame.draw.circle(screen, black, (int(circle1_x), int(circle_y)), int(circle_rad), 5)

    for step in range(0,9000,500):
        vcolor = white
        if step >= 4500:
            vcolor = yellow
        if step >= 6000:
            vcolor = red
        angle2 = (angle - ((step / 1.9) / 1000))
        line_x = (circle_rad - 8) * math.sin(angle2) + circle1_x
        line_y = (circle_rad - 8) * math.cos(angle2) + circle_y
        number_text = numberFont.render(str(step), True, vcolor)
        number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
        screen.blit(number_text, number_text_loc)
        pygame.draw.circle(screen, vcolor, [int(line_x), int(line_y)], 2)

    pygame.draw.circle(screen, black, (int(circle2_x), int(circle_y)), int(circle_rad), 5)

    for step in range(0,150,10):
        angle1 = (angle - ((step / .031) / 1000))
        line_x = (circle_rad - 8) * math.sin(angle1) + circle2_x
        line_y = (circle_rad - 8) * math.cos(angle1) + circle_y
        pygame.draw.circle(screen, white, [int(line_x), int(line_y)], 2)
        number_text = numberFont.render(str(step), True, white)
        number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
        screen.blit(number_text, number_text_loc)

    pygame.draw.circle(screen, black, (int(circle3_x), int(circle_y)), int(circle_rad), 5)

    for step in range(0,110,10):
        angle3 = (angle - ((step / .022) / 1000))
        line_x = (circle_rad - 8) * math.sin(angle3) + circle3_x
        line_y = (circle_rad - 8) * math.cos(angle3) + circle_y
        number_text = numberFont.render(str(step), True, white)
        number_text_loc = number_text.get_rect(center=(line_x, line_y+8))
        screen.blit(number_text, number_text_loc)
        pygame.draw.circle(screen, white, [int(line_x), int(line_y)], 2)

    speed_text = headerFont.render('SPEED', True, black)
    rpm_text = headerFont.render('RPM', True, black)
    load_text = headerFont.render('LOAD', True, black)
    speed_text_loc = speed_text.get_rect(center=(speed_text_x, speed_text_y))
    rpm_text_loc = rpm_text.get_rect(center=(rpm_text_x, rpm_text_y))
    load_text_loc = load_text.get_rect(center=(load_text_x, load_text_y))
    screen.blit(speed_text, speed_text_loc)
    screen.blit(rpm_text, rpm_text_loc)
    screen.blit(load_text, load_text_loc)

    if int(getHour())==12:
        hourX = posit[0*5 + int(int(getMin())/12)][0]
        hourY = posit[0*5 + int(int(getMin())/12)][1]
    else:
        hourX = posit[int(getHour())*5 + int(int(getMin())/12)][0]
        hourY = posit[int(getHour())*5 + int(int(getMin())/12)][1]

    minX = posit[int(getMin())][0]
    minY = posit[int(getMin())][1]
    secX = posit[int(getSec())][0]
    secY = posit[int(getSec())][1]

    pygame.draw.line(screen,white,(circle4_x,circle_y2),(hourX,hourY),8)
    pygame.draw.line(screen,offwhite,(circle4_x,circle_y2),(minX,minY),4)
    pygame.draw.circle(screen,red,(circle4_x,circle_y2),7,0)
    pygame.draw.line(screen,red,(circle4_x,circle_y2),(secX,secY),1)
    pygame.draw.circle(screen, black, (int(circle4_x), int(circle_y2)), (int(time_radian)+4), 5)

    time_text = timeFont.render(getHour()+':'+getMin()+':'+getSec(), True, white)
    time_text_loc = time_text.get_rect(center=(circle4_x, circle_y2 + 63))
    screen.blit(time_text, time_text_loc)


    #pygame.draw.circle(screen, blue, (int(circle1_x-3), int(circle_y2+50)), 25)

    
def get_speed(s):
    global speed
    if not s.is_null():
	#metric or standard speeds which do you require?
        speed = int(s.value.magnitude) #for kph metric
        #speed = int(s.value.magnitude * .060934) #for mph standard
def get_rpm(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.mangitude)
def get_load(l):
    global load
    if not l.is_null():
        load = int(l.value.mangitude)

def get_fule(f):
    global fule
    if not f.is_null():
        fule = int(f.value.mangitude)


    






#connection.watch(obd.commands.SPEED, callback=get_speed)
#connection.watch(obd.commands.RPM, callback=get_rpm)
#connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
#connection.watch(obd.commands.ETHANOL_PERCENT, callback=get_fule)
#connection.start()
check = 0		
running = True
while running:



    ###########
    keycheack1 = pygame.mouse.get_pressed()
    if(keycheack1[0] == 1 and check == 0):
        camera.preview.alpha = 255
        sleep(.1)
        check = 1
    ###########
    elif(keycheack1[0] == 1 and check == 1):
        camera.preview.alpha = 0
        sleep(.1)
        check = 0



        
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                #connection.stop()
		#connection.close()
            elif event.type == QUIT:
                running = False
                #connection.stop()
                #connection.close()
                
    draw_hud()
	
    speedDisplay = digitFont.render(str(int(speed)), 3, white)
    angle1 = (angle - ((speed / .031) / 1000))
    line_x = (circle_rad - 10) * math.sin(angle1) + circle2_x
    line_y = (circle_rad - 10) * math.cos(angle1) + circle_y
    pygame.draw.line(screen, blue, [circle2_x, circle_y], [line_x, line_y], 4)
	
    rpmDisplay = digitFont.render(str(rpm), 3, white)
    if rpm >= 4500:
        vcolor = yellow
    if rpm >= 6000:
            vcolor = red
    angle2 = (angle - ((rpm / 1.9) / 1000))
    line_x = (circle_rad - 10) * math.sin(angle2) + circle1_x
    line_y = (circle_rad - 10) * math.cos(angle2) + circle_y
    pygame.draw.line(screen, vcolor, [circle1_x, circle_y], [line_x, line_y], 2)
	
    loadDisplay = digitFont.render(" " + str(int(load)) + '%', 3, white)
    angle3 = (angle - ((load / .022) / 1000))
    line_x = (circle_rad - 10) * math.sin(angle3) + circle3_x
    line_y = (circle_rad - 10) * math.cos(angle3) + circle_y
    pygame.draw.line(screen, red, [circle3_x, circle_y], [line_x, line_y], 6)

    fule_text = timeFont.render(" " + str(int(fule)) + '%', True, white)
    fule_text_loc = fule_text.get_rect(center=(circle5_x, circle_y2 + 63))
    screen.blit(fule_text, fule_text_loc)
	
    screen.blit(loadDisplay, (circle3_x -((circle3_x / 8) - 40), circle_y + 60))
    screen.blit(rpmDisplay, (circle1_x - (circle2_x / 8) + 10, circle_y + 60))
    screen.blit(speedDisplay,(circle2_x -(circle1_x / 8) + 10, circle_y + 60))
    pygame.display.update()
    pygame.display.flip()
    
    #use to test the display
    rpm += 5
    if rpm >= 8505:
        rpm = 0
    speed += .05
    if speed >= 140:
        speed = 0
    load += .05
    if load >= 101:
        load = 0
    
    fule -= .1
    if fule <= 0:
        fule = 100
        
pygame.quit()
