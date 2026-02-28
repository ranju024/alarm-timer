import os
import pygame
from datetime import datetime
from buttons import Buttons


''' Set the screen '''
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the alarm window on desktop's window
screen_dimensions = (600,600)
pygame.display.set_caption('My-Alarm')
surface = pygame.display.set_mode(screen_dimensions)

# Initialize the mixer for sound playback
pygame.mixer.init()
sound_file = "alarm_sound.mp3" 
pygame.mixer.music.load(sound_file)
alarm_triggered = False
alarm_already_playing = False

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
wdow = None
while running:
    ''' Check for events on window'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     # Reset alarm if user presses 'r' / 'R'
        #     if event.key == pygame.K_r:  
                #reset

        # stop playing alarm audio when user presses 's' or 'S'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and alarm_already_playing:
                pygame.mixer.music.stop()
                alarm_already_playing = False
                buttons.reset()
                wdow = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # if left mouse button clicked
                pos = pygame.mouse.get_pos()

                # only check if previously any of the buttons haven't been pressed!!
                if wdow == None:
                    wdow = buttons.get_mouse_click(pos[0], pos[1])
                # alarm window not yet activated
                elif wdow == 0 and buttons.is_alarm_set == False:
                    index = buttons.alarm_button_clicked(pos[0], pos[1])
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

                    if index == 2:  # for am/pm
                        buttons.toggle_ampm()
                        txt_surface = buttons.btn_font.render(buttons.selected_time[2].upper(), True, (255,255,255))
                        surface.blit(txt_surface, pos)

        # handling any keyboard events while user tries to activate the alarm
        # handle user inputs (hour, min, toggle am-pm) when user presses respective button
        if event.type == pygame.KEYDOWN and index is not None:
            if index in (0, 1):
                if event.key == pygame.K_RETURN:  # if user presses 'Enter'
                    buttons.finalize_time_input(index)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
                else:
                    buttons.handle_time_input(surface, event, pygame, index)

               
             # timer button left
       

    if wdow != None:
        if wdow == 0: # alarm window
            pygame.display.set_caption('My-Alarm-Window')
            surface.fill(alarm_window_color)

            # if alarm hasn't been set, draw buttons with them in active state
            if buttons.is_alarm_set == False:
                buttons.get_alarm_click(pygame, surface)
            # if alarm has been set, display timer or maybe the day and time for which it has been set
            else:
                msg = "Your alarm has been set on"
                alarm_msg = "Time to work!"
                time = str(buttons.selected_time[0])+" : "+ str(buttons.selected_time[1])+" "+str(buttons.selected_time[2]).upper()
                alarm_time_str = buttons.get_alarm_time()
                print(alarm_time_str)
                now = datetime.now().strftime("%I:%M %p")  
                print(now)    


                if now >= alarm_time_str and not alarm_triggered:
                    alarm_msg_surface = font1.render(alarm_msg, True, (0, 10, 0))
                    print("Time to wake up!")
                    if not alarm_already_playing:
                        pygame.mixer.music.play(-1)   # Play the music on a loop (-1 means infinite loop)
                        alarm_already_playing = True
                    surface.blit(alarm_msg_surface, (200, 280))

                # Check if the music has stopped (e.g. if the user pressed 's' or it ended naturally)
                elif alarm_triggered and not pygame.mixer.music.get_busy():
                    alarm_triggered = False
                else:
                    msg_surface1 = font1.render(msg, True, (0,10,0))
                    msg_surface2 = font2.render(time, True, (0,10,0))
                    rect_pos = (250,300)
                    button_rect = pygame.Rect(rect_pos[0], rect_pos[1], 110, 50) 
                    surface.fill((255,255,255), button_rect)
                    surface.blit(msg_surface1, (50, 240))
                    surface.blit(msg_surface2, (rect_pos[0]+10, 310))
            # buttons.draw_alarm_buttons( pygame, surface)
        elif wdow == 1:
            pygame.display.set_caption('My-Timer-Window')
            surface.fill(timer_window_color)
    else:
        surface.fill(bg_color)
        buttons.create_buttons(surface, font2)
    pygame.display.flip()

pygame.quit()

