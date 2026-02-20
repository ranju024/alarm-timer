
# def get_mouse_click(mouse_x, mouse_y):
class Buttons:
    def __init__(self, pygame, font, fontl):
        self.pygame = pygame
        self.btn_font = font
        self.fontl = fontl
        self.color_selected = (0,255,0)
        self.color_normal = (255,0,0)

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
    
    def reset(self):
        self.is_alarm_set = False
        self.is_timer_set = False

    def get_mouse_click(self, x, y) -> int|None:
        return self.button_clicked(x, y)

    # create alarm window
    def alarm_window(self, surface):
        ...
        
    def draw_alarm_buttons(self, pygame, surface):
        for index, pos in enumerate(self.alarm_btn_positions):
            mx, my = self.get_mouse_positions()
            if index == 3:
                w, h = 150,  70
                font = self.fontl
                text = 'Activate'
            else: 
                w, h = self.btn_w, self.btn_h
                font = self.font
                if index == 0: 
                    text = 'Hour'
                elif index == 1:
                    text = 'Minutes'
                elif index == 2:
                    text = 'AM/PM'
            pygame.draw.rect(surface, self.rect_color, [pos[0], pos[1], w,h], width=2, border_radius=5)

            # checking for mouse hover
            if self.buttons.button_hover(pos):
                pygame.draw.rect(surface, self.rect_color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
                text_surface = font.render(text, True, (0, 255, 0))
            else:
                text_surface = font.render(text, True, self.text_color_normal)

            # check if a number was selected, then draw it green
            self.button_clicked(mx, my) != None
            if self.selected_button == index:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
                text_surface = self.mfont.render(text, True, self.text_color_selected)


            surface.blit(text_surface, (pos[0] + 13, pos[1]))

    def get_mouse_positions(self):
        mouse_pos = self.pygame.mouse.get_pos()
        return (mouse_pos[0], mouse_pos[1])


    # do something when button pressed
    def button_clicked(self, mouse_x, mouse_y):
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                return index
        return None

    # is button currently being hovered?
    def button_hover(self, pos):
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    # is the cursor currently on a button?    
    def on_button(self, mouse_x, mouse_y, pos):
        return (pos[0] < mouse_x < (pos[0] + self.btn_w)) and \
                (pos[1] < mouse_y < (pos[1] + self.btn_h))
