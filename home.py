import os
import pygame
from datetime import datetime
from buttons import Buttons


''' Set the screen '''
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the alarm window on desktop's window
screen_dimensions = (600,600)
pygame.display.set_caption('My-Alarm')
surface = pygame.display.set_mode(screen_dimensions)

''' Fonts '''
pygame.font.init()
font0 = pygame.font.SysFont(name='Comic Sans MS', size=70)
font1 = pygame.font.SysFont(name='Comic Sans MS', size=40)
font2 = pygame.font.SysFont(name='Comic Sans MS', size=20)

''' BG Color '''
bg_color = (0,0,0)
alarm_window_color = (255, 0, 0)
timer_window_color = (0, 0, 255)

buttons = Buttons(pygame, font2, font0)

running = True
btn = None
while running:
    ''' Check for events on window'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Reset alarm if user presses 'r' / 'R'
            if event.key == pygame.K_r:  
                #reset
                ...
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # if left mouse button clicked
                pos = pygame.mouse.get_pos()

                # only check if previously any of the buttons haven't been pressed!!
                if btn == None:
                    btn = buttons.get_mouse_click(pos[0], pos[1])
                elif btn == 0:
                    buttons.alarm_button_clicked(pos[0], pos[1])
    if btn != None:
        if btn == 0: # alarm window
            pygame.display.set_caption('My-Alarm-Window')
            surface.fill(alarm_window_color)

            # if alarm hasn't been set, draw buttons with them in active state
            if buttons.is_alarm_set == False:
                buttons.get_alarm_click(pygame, surface)
                ...
            # if alarm has been set, display timer or maybe the day and time for which it has been set
            else:
                msg = "Your alarm has been set on"
                time = str(buttons.selected_time[0])+" : "+ str(buttons.selected_time[1])+" "+str(buttons.selected_time[2]).upper()
                msg_surface1 = font1.render(msg, True, (0,10,0))
                msg_surface2 = font2.render(time, True, (0,10,0))

    # screen.fill(color, button_rect) 
                rect_pos = (250,300)
                button_rect = pygame.Rect(rect_pos[0], rect_pos[1], 110, 50) 
                surface.fill((255,255,255), button_rect)

                surface.blit(msg_surface1, (50, 240))
                surface.blit(msg_surface2, (rect_pos[0]+10, 310))
            # buttons.draw_alarm_buttons( pygame, surface)
        elif btn == 1:
            pygame.display.set_caption('My-Timer-Window')
            surface.fill(timer_window_color)
    else:
        surface.fill(bg_color)
        buttons.create_buttons(surface, font2)
    pygame.display.flip()

pygame.quit()

# now = datetime.now()
# c_hour = now.hour
# c_min = now.minute
# c_sec = now.second
# c_ms = now.microsecond

# print(now)
# print(f"{c_hour} : {c_min} : {c_sec}")

# time = input('Enter time in HH:MM format: ')
# hour = int(time[:2])
# min = int(time[3:])

# print(hour, min)

# duration = hour*min*60
# while hour!=0 and min !=0