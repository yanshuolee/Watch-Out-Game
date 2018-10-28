#!/usr/bin/env python

# set pygame window position
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,70)

# Import library
import random
import pygame
from pygame.locals import *
import cv2
import dlib

# Window set-up
pygame.init()
pygame.mixer.init()
width, height = 480, 640
screen = pygame.display.set_mode((width, height)) # set up window
pygame.display.set_caption('Watch out!')

# Load images
player = pygame.image.load("resources/images/main_char.png")
bkgd = pygame.image.load("resources/images/background.png").convert()
main_menu_bkgd = pygame.image.load("resources/images/main_menu.png").convert()
arrow = pygame.image.load("resources/images/b_1.png")
person_1 = pygame.image.load("resources/images/person_1.png")
person_2 = pygame.image.load("resources/images/person_2.png")
person_3 = pygame.image.load("resources/images/person_3.png")
person_4 = pygame.image.load("resources/images/person_4.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/win.png")

# Load audio
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/background_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Text rendering function
def message_to_screen(message, size, color):
    my_font = pygame.font.Font(None, size)
    my_message = my_font.render(message, 0, color)
    return my_message

# Main menu
def main_menu():
    menu = True # used by while-loop
    selected = "start"
    while menu:
        # choose to start / quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # drawing background
        screen.blit(main_menu_bkgd, (0, 0))

        if selected == "start":
            play = message_to_screen("START", 75, (0,0,0))
        else:
            play = message_to_screen("START", 75, (255,255,255))
        if selected == "quit":
            game_quit = message_to_screen("QUIT", 75, (0,0,0))
        else:
            game_quit = message_to_screen("QUIT", 75, (255,255,255))
	
        # drawing text
        screen.blit(play, (width//2-80,height-100))
        screen.blit(game_quit, (width//2-60,height-50))

        # update the scrren
        pygame.display.update()
    
    start_game()

def start_game():
    # Initialize the game and camera
    playerpos = [100, 450]
    arrows = []
    shootingSpeed = 10 # wait how many loops then shoot
    shootingDelay = shootingSpeed
    badtimer = 100 # frequency of drawing enemies
    badtimer1 = 0
    enemy_1 = []
    enemy_2 = []
    enemy_3 = []
    enemy_4 = []
    healthvalue = 194
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    tracker = dlib.correlation_tracker()
    trackingFace = 0
    running = 1
    exitcode = 0
    background_y = 0    


    # Looping the game
    while running:
        # clear the screen before drawing it again
        screen.fill(0)

        # Draw background
        rel_y = background_y % bkgd.get_rect().height
        screen.blit(bkgd,(0,rel_y - bkgd.get_rect().height))
        if rel_y < height:
            screen.blit(bkgd , (0 , rel_y)) 
        background_y +=3
        
        # Draw player position
        playerposForPlot = (playerpos[0], playerpos[1])
        screen.blit(player , playerposForPlot)
        
        # Draw bullets
        for bullet in arrows:
            index = 0
            bullet[1] -= 5
            if bullet[0]< 0 or bullet[0]> 480 or bullet[1]< 230 or bullet[1]> 640:
                arrows.pop(index)
            index += 1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 90)
                screen.blit(arrow1, (projectile[0], projectile[1]))
        
        # Draw enemies
        if badtimer == 0:
            # add badguy position into list
            badguyRandom = random.randint(0,6)
            if badguyRandom == 0 and enemy_1 == []:
                enemy_1 = [random.randint(50, 400), 0]
            elif badguyRandom == 2 and enemy_2 == []:
                enemy_2 = [random.randint(50, 400), 0]
            elif badguyRandom == 4 and enemy_3 == []:
                enemy_3 = [random.randint(50, 400), 0]
            elif badguyRandom == 6 and enemy_4 == []:
                enemy_4 = [random.randint(50, 400), 0]
            
            badtimer = 100 - (badtimer1 * 2)
            if badtimer1 >= 35:
                badtimer1 = 35
            else:
                badtimer1 += 5
        
        # check if enemies is out of range
        if enemy_1 != [] and enemy_1[1] > 620:
            healthvalue -= random.randint(5,20)
            enemy_1 = []
        if enemy_2 != [] and enemy_2[1] > 620:
            healthvalue -= random.randint(5,20)
            enemy_2 = [] 
        if enemy_3 != [] and enemy_3[1] > 620:
            healthvalue -= random.randint(5,20)
            enemy_3 = []
        if enemy_4 != [] and enemy_4[1] > 620:
            healthvalue -= random.randint(5,20)
            enemy_4 = []
        
        # if not empty, draw it on the screen and move it
        if enemy_1 != []:
            enemy_1[1] += 7
            screen.blit(person_1, enemy_1)
        if enemy_2 != []:
            enemy_2[1] += 7
            screen.blit(person_2, enemy_2)
        if enemy_3 != []:
            enemy_3[1] += 7
            screen.blit(person_3, enemy_3)
        if enemy_4 != []:
            enemy_4[1] += 7
            screen.blit(person_4, enemy_4)
        

        # Attack enemy
        if enemy_1 != []:
            badrect = pygame.Rect(person_1.get_rect())
            badrect.top = enemy_1[1]
            badrect.left = enemy_1[0]

            # Check for collisions
            bulletIndex = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[0]
                bullrect.top = bullet[1]
                if badrect.colliderect(bullrect):
                    enemy_1 = []
                    arrows.pop(bulletIndex)
                bulletIndex += 1
        if enemy_2 != []:
            badrect = pygame.Rect(person_2.get_rect())
            badrect.top = enemy_2[1]
            badrect.left = enemy_2[0]

            # Check for collisions
            bulletIndex = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[0]
                bullrect.top = bullet[1]
                if badrect.colliderect(bullrect):
                    enemy_2 = []
                    arrows.pop(bulletIndex)
                bulletIndex += 1
        if enemy_3 != []:
            badrect = pygame.Rect(person_3.get_rect())
            badrect.top = enemy_3[1]
            badrect.left = enemy_3[0]

            # Check for collisions
            bulletIndex = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[0]
                bullrect.top = bullet[1]
                if badrect.colliderect(bullrect):
                    enemy_3 = []
                    arrows.pop(bulletIndex)
                bulletIndex += 1
        if enemy_4 != []:
            badrect = pygame.Rect(person_4.get_rect())
            badrect.top = enemy_4[1]
            badrect.left = enemy_4[0]

            # Check for collisions
            bulletIndex = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[0]
                bullrect.top = bullet[1]
                if badrect.colliderect(bullrect):
                    enemy_4 = []
                    arrows.pop(bulletIndex)
                bulletIndex += 1

        badtimer-=10

        # Draw clock
        font = pygame.font.Font(None, 40)
        survivedtext = font.render( str((90000-pygame.time.get_ticks())//60000) + ":" + str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright = [470, 5]
        screen.blit(survivedtext, textRect)
        
        # Draw health bar
        screen.blit(healthbar, (5, 5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1 + 8, 8))
        
        # update the screen
        pygame.display.update()

        # check if window closed
        for event in pygame.event.get():
            if event.type == QUIT:
                # if closed, close the window
                pygame.quit()
                exit(0)
        
        # make shooting
        if shootingDelay == shootingSpeed:
            shootingDelay = 0
            shoot.play()
            arrows.append([playerposForPlot[0]+63 , playerposForPlot[1]-40])
        shootingDelay += 1

        # Move player using camera
        ret,frame = cap.read()
        frame = cv2.flip(frame,1)
        if not trackingFace:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            maxArea = 0
            x = 0
            y = 0
            w = 0
            h = 0
            for (_x,_y,_w,_h) in faces:
                if  _w*_h > maxArea:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)
                    maxArea = w*h

            if maxArea > 0 :
                #Initialize the tracker
                tracker.start_track(frame,dlib.rectangle(x-10,y-20,x+w+10,y+h+20))
                #Set the indicator variable such that we know the
                #tracker is tracking a region in the image
                trackingFace = 1
        
        if trackingFace:
            trackingQuality = tracker.update(frame)
            if trackingQuality >= 8.5:
                tracked_position =  tracker.get_position()
                t_x = int(tracked_position.left())
                t_y = int(tracked_position.top())
                t_w = int(tracked_position.width())
                t_h = int(tracked_position.height())
                cv2.rectangle(frame, (t_x, t_y),(t_x + t_w , t_y + t_h),(0,255,0) ,2)
                playerpos[0] = t_x
                    
            else:
                trackingFace = 0
        cv2.imshow('Camera Output',frame)
        cv2.moveWindow('Camera Output',600,150) # set window to wanted position
        

        # Win/Lose check
        if pygame.time.get_ticks() >= 90000:
            running = 0
            exitcode = 1
        if healthvalue <= 0:
            running = 0
            exitcode = 0

    # Win/lose display
    if exitcode == 0:
        pygame.mixer.music.stop()
        cap.release()
        cv2.destroyAllWindows()
        screen.blit(gameover, (0, 0))
    else:
        pygame.mixer.music.stop()
        cap.release()
        cv2.destroyAllWindows()
        screen.blit(youwin, (0, 0))

    # Don't close window until I close it
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                exit(0)
        pygame.display.update()

main_menu()
