
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

        self.selected_time = [0, 0, 'am']
        self.alarm_btns_state = [False, False, False, False]

        self.text = ""

    def get_alarm_time(self):
        alarm_time_str = f"{self.selected_time[0]:02}:{self.selected_time[1]:02} {self.selected_time[2].upper()}"
        return alarm_time_str

    def reset(self):
        self.is_alarm_set = False
        self.is_timer_set = False
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


    def draw_alarm_buttons(self, pygame, surface):
        for index, pos in enumerate(self.alarm_btn_positions):
            mpos = self.get_mouse_positions()
            if index == 3:
                w, h = 200, 80
                font = self.fontl
                text = 'Activate'
            else: 
                w, h = self.btn_w, self.btn_h
                font = self.btn_font
                if index == 0: 
                    text = 'Hour'
                elif index == 1:
                    text = 'Minutes'
                elif index == 2:
                    text = 'AM/PM'
            pygame.draw.rect(surface, self.rect_color, [pos[0], pos[1], w,h], width=2, border_radius=5)

            # checking for mouse hover
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.rect_color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
                text_surface = font.render(text, True, self.text_color_selected)
            else:
                text_surface = font.render(text, True, self.text_color_normal)

            # check if a button was clicked, then set its color
            # self.selected_alarm_button = self.alarm_button_clicked(mpos[0], mpos[1])
            # if self.selected_alarm_button == index:
            #     pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
            #     text_surface = font.render(text, True, self.text_color_selected)

            surface.blit(text_surface, (pos[0] + 13, pos[1]))

    def get_mouse_positions(self):
        mouse_pos = self.pygame.mouse.get_pos()
        return mouse_pos
    
    def get_mouse_click(self, x, y) -> int|None:
        return self.button_clicked(x, y)

    # def get_alarm_click(self, pygame, screen, mx, my):
    #     self.selected_alarm_button = self.alarm_button_clicked(mx, my)
    #     btn = self.selected_alarm_button
    #     text = ''
    #     if btn != None:
    #         done = False
    #         while not done:
    #             for event in pygame.event.get():
    #                 # if event.type == pygame.MOUSEBUTTONDOWN:
    #                 #     # Toggle active state if the user clicks on the input box
    #                 #     if input_box.collidepoint(event.pos):
    #                 #         active = not active
    #                 #     else:
    #                 #         active = False
    #                     # color = color_active if active else color_inactive
    #                 if event.type == pygame.KEYDOWN:
    #                     if event.key == pygame.K_RETURN:
    #                         done = True
    #                     elif event.key == pygame.K_BACKSPACE:
    #                         text = text[:-1]
    #                     # Only append characters that are digits
    #                     elif event.unicode.isdigit(): 
    #                         text += event.unicode

    #             # Render the current input text
    #             prompt_surface = self.fonts.render(str(text), True, (255, 0, 255))
    #             screen.blit(prompt_surface, self.alarm_btn_positions[btn])

    #             pygame.display.update()

    #         try:
    #             if btn == 0:
    #                 hr = int(text)
    #             elif btn == 1:
    #                 min = int(text)
        
    #             return int(text)     # if '.' not in text else float(text)
    #         except ValueError:
    #             return None # Handle cases where input is empty or invalid
    #     # if btn == 0: ask user to input hours
    #     # if btn == 1: ask user to input minutes
    #     # if btn == 2: ask user to input am/pm
    #     # if btn == 3: activate the alarm (current time, final time, ...)

    def finalize_time_input(self, index):
        """Finalizes the hour or minute input when Enter is pressed."""
        try:
            value = int(self.text)
            if index == 0:  # Hour
                if 1 <= value <= 12:
                    self.selected_time[index] = value
            elif index == 1:  # Minutes
                if 0 <= value < 60:
                    self.selected_time[index] = value
        except ValueError:
            # Handle cases where input is not a valid number
            print(f"{self.selected_time[index]} is not a valid number")
            self.selected_time[index] = 0
        self.text = "" # Clear input box text after submission


    def handle_time_input(self, surface, event, pygame, index):
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

        # now handle user inputs (hour, min, toggle am-pm) when user presses the button
        # self.selected_time = [0, 0, 'am']
        # self.alarm_btns_state = [False, False, False, False]
            # if self.alarm_btns_state[index] == True:
            #     if index == 0 or index == 1:
            #         for event in pygame.event.get():
            #             if event.type == pygame.KEYDOWN:
            #                 if event.key == pygame.K_RETURN:  # if user presses 'Enter'
            #                     if index == 0:  # for hour
            #                         # self.selected_time[index] = self.text if self.text <=12  else 0
            #                         self.selected_time[index] = int(self.text) if self.text.isdigit() and int(self.text) <=12  else 0
            #                     elif index == 1:  # for minutes
            #                         self.selected_time[index] = int(self.text) if self.text.isdigit() and int(self.text) < 60  else 0
            #                         # self.selected_time[index] = self.text if self.text <60  else 0
            #                 elif event.key == pygame.K_BACKSPACE:
            #                     self.text = self.text[:-1]
            #                 elif event.unicode.isdigit() and len(self.text) < 2:
            #                     self.text += event.unicode
            #                 txt_surface = self.btn_font.render(str(self.text), True, text_color)
            #                 # Now blit the text
            #                 screen.blit(txt_surface, pos)
            #         # pygame.draw.rect(screen, self.color, self.rect, 2)
            #     elif index == 2:  # for am/pm
            #         self.toggle_ampm()
            #         txt_surface = self.btn_font.render(self.selected_time[2].upper(), True, text_color)
            #         screen.blit(txt_surface, pos)
            
            # if user presses on 'Activate' button, show the activated window
            if index == 3:
                prompt = 'Activate'
            else:
                prompt = self.selected_time[index]
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

        # set btn state tp True when any button pressed
    def alarm_button_clicked(self, mouse_x, mouse_y):
        for index, pos in enumerate(self.alarm_btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.alarm_btns_state[index] = True
                if index == 3:
                    self.is_alarm_set = True
                return index
            elif index != 3:
                self.alarm_btns_state[index] = False

    # is button currently being hovered?
    def button_hover(self, pos):
        mouse_pos = self.get_mouse_positions()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    # is the cursor currently on a button?    
    def on_button(self, mouse_x, mouse_y, pos):
        return (pos[0] < mouse_x < (pos[0] + self.btn_w)) and \
                (pos[1] < mouse_y < (pos[1] + self.btn_h))
