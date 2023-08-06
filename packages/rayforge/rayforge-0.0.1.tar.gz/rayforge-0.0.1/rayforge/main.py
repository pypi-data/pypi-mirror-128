from pyray import *

import os

from rayforge.color import Color
from rayforge.vec2 import Vec2

class RayForge:
    def __init__(self, width = 1200, height = 600, fps = 60, background_color = Color(20, 20, 20)):
        self.fps = fps
        self.width = width
        self.height = height
        self.background_color = background_color

        init_window(self.width, self.height, "Forge")
        set_target_fps(self.fps)

        self.path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(self.path, "./assets/icon/icon.png")
        icon = load_image(icon)
        set_window_icon(icon)

        self.update_handlers = []
        self.draw_handlers = []

        print("INFO: RAYFORGE: Initialized successfully")

    def _update(self):
        for i in self.update_handlers:
            i()

    def _draw(self):
        for i in self.draw_handlers:
            i()

    def run(self):
        while not window_should_close():
            self._update()
            begin_drawing()
            clear_background(self.background_color.get_tuple())
            self._draw()
            end_drawing()

        close_window()

    def update(self, func):
        self.update_handlers.append(func)

    def draw(self, func):
        self.draw_handlers.append(func)

    def set_background_color(self, color):
        self.background_color = color

    def set_fps(self, fps):
        self.fps = fps
        set_target_fps(self.fps)

    def get_fps(self):
        return get_fps() / 1

    def set_window_pos(self, x, y):
        set_window_position(x, y)

    def get_window_pos(self):
        return Vec2(get_window_position().x, get_window_position().y)

    def set_window_size(self, width, height):
        set_window_size(width, height)

    def get_window_size(self):
        return get_screen_width(), get_screen_height()

    def set_window_width(self, width):
        set_window_size(width, get_screen_height())

    def set_window_height(self, height):
        set_window_size(get_screen_width(), height)

    def get_window_width(self):
        return get_screen_width()

    def get_window_height(self):
        return get_screen_height()