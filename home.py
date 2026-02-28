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
timer_already_playing = False


''' Fonts '''
pygame.font.init()
font0 = pygame.font.SysFont(name='Comic Sans MS', size=70)
font1 = pygame.font.SysFont(name='Comic Sans MS', size=40)
font2 = pygame.font.SysFont(name='Comic Sans MS', size=20)

''' BG Color '''
bg_color = (0,0,0)
alarm_window_color = (255, 0, 0)
timer_window_color = (0, 0, 255)

clock = pygame.time.Clock()
buttons = Buttons(pygame, font2, font0)

running = True
wdow = None
while running:
    ''' Check for events on window'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # stop playing alarm audio when user presses 's' or 'S'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if alarm_already_playing:
                    pygame.mixer.music.stop()
                    alarm_already_playing = False
                    buttons.reset_alarm()
                    wdow = None
                elif timer_already_playing:
                    pygame.mixer.music.stop()
                    timer_already_playing = False
                    buttons.reset_timer()
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
                # timer window 
                elif wdow == 1: 
                    if buttons.is_timer_set == False:  # not yet activated
                        index = buttons.timer_button_clicked(pos[0], pos[1])
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                        start_time = pygame.time.get_ticks()
                

        # handling any keyboard events while user tries to activate the alarm or set the timer
        # handle user inputs (hour, min, toggle am-pm/seconds) when user presses respective button
        if event.type == pygame.KEYDOWN and index is not None:
            if wdow == 0:
                if index in (0, 1):
                    if event.key == pygame.K_RETURN:  # if user presses 'Enter'
                        buttons.finalize_time_input(index, wdow)
                        
                    else:
                        buttons.handle_time_input(surface, event, pygame, index, wdow)
            if wdow == 1:
                if index in (0, 1, 2):
                    if event.key == pygame.K_RETURN:  # if user presses 'Enter'
                        buttons.finalize_time_input(index, wdow)
                        
                    else:
                        buttons.handle_time_input(surface, event, pygame, index, wdow)


    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
               
    if wdow != None:
        
        if wdow == 0: 
            '''  alarm window '''
            pygame.display.set_caption('My-Alarm-Window')
            surface.fill(alarm_window_color)

            # if alarm hasn't been set, draw buttons with them in active state
            if buttons.is_alarm_set == False:
                buttons.get_alarm_click(pygame, surface)
            # if alarm has been set, display time for which it has been set
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

                # Check if the music has stopped (if the user pressed 's' or it ended naturally)
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
        
        elif wdow == 1:
            ''' timer window '''
            pygame.display.set_caption('My-Timer-Window')
            surface.fill(timer_window_color)

            # if timer hasn't been set, draw buttons with them in active state
            if buttons.is_timer_set == False:
                buttons.get_timer_click(pygame, surface)
            # if timer has been set, display timer 
            else:
                hours = buttons.selected_timer[0]
                minutes = buttons.selected_timer[1]
                seconds = buttons.selected_timer[2]            
                
                total_seconds = hours*60*60 + minutes*60 + seconds  # converted into seconds

                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - start_time) // 1000   # Convert milliseconds to seconds

                if total_seconds - elapsed_time > 0:
                    time_left = total_seconds - elapsed_time
                    # Convert time_left back to H:M:S format
                    minutes, seconds = divmod(time_left, 60)
                    hours, minutes = divmod(minutes, 60)
                    timer_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    
                else:
                    timer_text = "Time Up!"
                    if not timer_already_playing:
                        pygame.mixer.music.play(-1)   # Play the music on a loop (-1 means infinite loop)
                        timer_already_playing = True
                
                text_surface = font0.render(timer_text, True, (255, 255, 255))
                # Center the text
                text_rect = text_surface.get_rect(center=(300, 300))
                surface.blit(text_surface, text_rect)
               
                # Cap the frame rate
                clock.tick(60) # limits FPS to 60

    else:
        surface.fill(bg_color)
        buttons.create_buttons(surface, font2)
    pygame.display.flip()

pygame.quit()

