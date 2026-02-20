from buttons import Buttons

class SelectTime:
    def __init__(self, pygame, fonts, fontl):
        self.pygame = pygame
        self.fonts = fonts
        self.fontl = fontl
        self.btn_w = 100
        self.btn_h = 50

        self.rect_color = (255,255,255)
        self.rect_color_selected = (0, 255, 0)
        self.text_color_normal = (0, 0, 0)
        self.text_color_selected = (0, 244, 20)

        self.btn_positions = [
            (50, 150),
            (300, 150),
            (450, 150),
            (200, 500)
        ]
        self.buttons = Buttons(pygame, fonts)
        self.selected_button = None
        self.selected_hour = 0
        self.selected_min = 0
        self.selected_ampm = ''
    
    def draw_alarm_buttons(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            mx, my = self.get_mouse_positions()
            if index == 3:
                w, h = 150,  70
                font = self.fontl
                text = 'Activate'
            else: 
                w, h = self.btn_w, self.btn_h
                font = self.fonts
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
            self.buttons.button_clicked(mx, my) != None
            if self.selected_button == index:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], w, h], width=2, border_radius=5)
                text_surface = self.mfont.render(text, True, self.text_color_selected)


            surface.blit(text_surface, (pos[0] + 13, pos[1]))

    def get_mouse_positions(self):
        mouse_pos = self.pygame.mouse.get_pos()
        return (mouse_pos[0], mouse_pos[1])

