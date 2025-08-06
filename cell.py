import pygame

class Cell:
    def __init__(self, value, row, col, screen, is_user_input=False):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.is_user_input = is_user_input

    def set_cell_value(self, value):
        self.value = value
        self.is_user_input = True

    def set_sketched_value(self, value):
        self.sketched_value = value

    def clear(self):
        self.value = 0
        self.sketched_value = 0
        self.is_user_input = False

    def draw(self, width, height):
        x_pos = self.col * width
        y_pos = self.row * height

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x_pos, y_pos, width, height), 3)

        font = pygame.font.Font(None, 40)

        if self.value != 0:
            color = (0, 0, 255) if self.is_user_input else (0, 0, 0)
            text = font.render(str(self.value), True, color)
            text_rect = text.get_rect(center=(x_pos + width / 2, y_pos + height / 2))
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, (0, 0, 255))
            text_rect = text.get_rect(center=(x_pos + width / 2, y_pos + height / 2))
            self.screen.blit(text, text_rect)

