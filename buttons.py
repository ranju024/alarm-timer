
# def get_mouse_click(mouse_x, mouse_y):
class Buttons:
    def __init__(self, pygame, font, fontl):
        self.pygame = pygame
        self.btn_font = font
        self.fontl = fontl

        self.selected_alarm_button = None

        self.color_selected = (0,255,0)
        self.color_normal = (255,0,0)
 
        self.btn_color = (0,0,0)
        self.rect_color_selected = (0, 255, 0)
        self.text_color_normal = (0, 0, 0)
        self.text_color_selected = (0, 244, 20)

        self.is_alarm_set = False
        self.is_timer_set = False

        self.btn_w = 120
        self.btn_h = 40
        self.btn_positions = [
            (150, 250),
            (350, 250)
        ]

        self.alarm_btn_positions = [
            (50, 150),
            (300, 150),
            (450, 150),
            (200, 500)
        ]
        self.timer_btn_positions = [
            (50, 150),
            (300, 150),
            (450, 150),
            (200, 500)
        ]

        self.selected_time = [0, 0, 'am']
        self.selected_timer = [0, 0, 0]
        self.alarm_btns_state = [False, False, False, False]
        self.timer_btns_state = [False, False, False, False]

        self.text = ""

    def get_alarm_time(self):
        alarm_time_str = f"{self.selected_time[0]:02}:{self.selected_time[1]:02} {self.selected_time[2].upper()}"
        return alarm_time_str

    def reset_timer(self):
        self.is_timer_set = False
        self.timer_btns_state = [False, False, False, False]
        self.selected_timer = [0, 0, 0]

    def reset_alarm(self):
        self.is_alarm_set = False
        self.alarm_btns_state = [False, False, False, False]
        self.selected_time = [0, 0, 'am']

    def create_buttons(self, surface, font):
        for index, pos in enumerate(self.btn_positions):

            if self.button_hover(pos): color = self.color_selected 
            else: color = self.color_normal

            # draw rectangular border
            self.pygame.draw.rect(surface, color, [pos[0], pos[1], self.btn_w, self.btn_h], width=5, border_radius=7)

            if index == 0: text = "Set Alarm" 
            elif index == 1: text = "Set Timer"
            text_surface = font.render(text, True, color) # render text into image
            surface.blit(text_surface, (pos[0]+10, pos[1]+5))  #blit rendered text onto surface(screen)


    # # def draw_alarm_buttons(self, pygame, surface):
    #     for index, pos in enumerate(self.alarm_btn_positions):
    #         mpos = self.get_mouse_positions()
    #         if index == 3:
    #             w, h = 200, 80
    #             font = self.fontl
    #             text = 'Activate'
    #         else: 
    #             w, h = self.btn_w, self.btn_h
    #             font = self.btn_font
    #             if index == 0: 
    #                 text = 'Hour'
    #             elif index == 1:
    #                 text = 'Minutes'
    #             elif index == 2:
    #                 text = 'AM/PM'
    #         self.pygame.draw.rect(surface, self.rect_color, [pos[0], pos[1], w,h], width=2, border_radius=5)

    #         # checking for mouse hover
    #         if self.button_hover(pos):
    #             self.pygame.draw.rect(surface, self.rect_color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
    #             text_surface = font.render(text, True, self.text_color_selected)
    #         else:
    #             text_surface = font.render(text, True, self.text_color_normal)

    #         surface.blit(text_surface, (pos[0] + 13, pos[1]))
  
    def get_mouse_positions(self):
        mouse_pos = self.pygame.mouse.get_pos()
        return mouse_pos
    
    def get_mouse_click(self, x, y) -> int|None:
        return self.button_clicked(x, y)

    def finalize_time_input(self, index, wdow):
        """Finalizes the hour and minute input (for alarm) and hour, minute and seconds input (for timer) when Enter is pressed."""
        try:
            value = int(self.text)
            if index == 0:  # Hour
                if 1 <= value <= 12:
                    if wdow == 0:
                        self.selected_time[index] = value 
                    elif wdow == 1:
                        self.selected_timer[index] = value
            elif index == 1:  # Minutes
                if 0 <= value < 60:
                    if wdow == 0:
                        self.selected_time[index] = value 
                    elif wdow == 1:
                        self.selected_timer[index] = value
            elif index == 2 and wdow == 1:  # seconds for timer
                if 0 <= value < 60:
                    self.selected_timer[index] = value
        except ValueError:
            # Handle cases where input is not a valid number
            print(f"{self.selected_time[index]} is not a valid number")
            if wdow == 0:
                self.selected_time[index] = 0
            elif wdow == 1:
                self.selected_timer[index] = 0
        self.text = "" # Clear input box text after submission


    def handle_time_input(self, surface, event, pygame, index, wdow):
        if wdow == 0:
            pos = self.alarm_btn_positions[index]
            """Handles digit input, backspace, and rendering for text fields."""
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and len(self.text) < 2:
                self.text += event.unicode
            
            # Update the text surface immediately after changing the text
            txt_surface = self.btn_font.render(str(self.text), True, (255,255,255))
            # Now blit the text
            surface.blit(txt_surface, pos)
            pygame.display.update()
        
        elif wdow == 1: # timer window
            pos = self.timer_btn_positions[index]
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and len(self.text) < 2:
                self.text += event.unicode
            
            txt_surface = self.btn_font.render(str(self.text), True, (255,255,255))
            surface.blit(txt_surface, pos)
            pygame.display.update()


    def get_alarm_click(self, pygame, screen):
        for index, pos in enumerate(self.alarm_btn_positions):
            # before blitting the text, define the rect for the button
            print(pos)
            button_rect = pygame.Rect(pos[0], pos[1], self.btn_w, self.btn_h) 
            color = self.btn_color
            text_color = (255,255,255)

            if self.button_hover(pos) or self.alarm_btns_state[index] == True:
                color = (0,255,255)
                text_color = (0,0,0)

            # Clear the area with a background color
            screen.fill(color, button_rect) 
            
            # if user presses on 'Activate' button, show the activated window
            if index == 3:
                prompt = 'Activate'
            else:
                prompt = self.selected_time[index]
            prompt_surface = self.btn_font.render(str(prompt), True, text_color)
            screen.blit(prompt_surface, pos)
    
    def get_timer_click(self, pygame, screen):
        for index, pos in enumerate(self.timer_btn_positions):
            # before blitting the text, define the rect for the button
            button_rect = pygame.Rect(pos[0], pos[1], self.btn_w, self.btn_h) 
            color = self.btn_color
            text_color = (255,255,255)

            if self.button_hover(pos) or self.timer_btns_state[index] == True:
                color = (0,255,255)
                text_color = (0,0,0)

            # Clear the area with a background color
            screen.fill(color, button_rect) 
            
            # if user presses on 'Activate' button, show the activated window
            if index == 3:
                prompt = 'Set Timer'
            else:
                prompt = self.selected_timer[index]
            prompt_surface = self.btn_font.render(str(prompt), True, text_color)
            screen.blit(prompt_surface, pos)

    # Toggle am or pm
    def toggle_ampm(self):
        if self.selected_time[2] == 'am':
            self.selected_time[2] = 'pm'
        else:
            self.selected_time[2] = 'am'


    # return index when button pressed
    def button_clicked(self, mouse_x, mouse_y):
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                return index
        return None

    # set btn state to True when any button pressed
    def alarm_button_clicked(self, mouse_x, mouse_y):
        for index, pos in enumerate(self.alarm_btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.alarm_btns_state[index] = True
                if index == 3:
                    self.is_alarm_set = True
                return index
            elif index != 3:
                self.alarm_btns_state[index] = False

    def timer_button_clicked(self, mouse_x, mouse_y):
        for index, pos in enumerate(self.timer_btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.timer_btns_state[index] = True
                if index == 3:
                    self.is_timer_set = True
                return index
            elif index != 3:
                self.timer_btns_state[index] = False

    # is button currently being hovered?
    def button_hover(self, pos):
        mouse_pos = self.get_mouse_positions()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    # is the cursor currently on a button?    
    def on_button(self, mouse_x, mouse_y, pos):
        return (pos[0] < mouse_x < (pos[0] + self.btn_w)) and \
                (pos[1] < mouse_y < (pos[1] + self.btn_h))
