from pyray import *

from rayforge.color import Color

class Text:
    def __init__(self, text, x = 0, y = 0, font_size = 24, color = Color(240, 240, 240)):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color

    def draw(self):
        draw_text(self.text, self.x, self.y, self.font_size, self.color.get_tuple())

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_font_size(self, font_size):
        self.font_size = font_size

    def get_font_size(self):
        return self.font_size

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def center(self):
        self.x = int(get_screen_width() / 2) - self.font_size * 6
        self.y = int(get_screen_height() / 2) - int(self.font_size / 2)

    def center_x(self):
        self.x = int(get_screen_width() / 2) - self.font_size * 6

    def center_y(self):
        self.y = int(get_screen_height() / 2) - int(self.font_size / 2)