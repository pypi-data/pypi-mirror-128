from pyray import *

from rayforge.color import Color
from rayforge.text import Text

class FpsCounter(Text):
    def __init__(self, x = 0, y = 0, font_size = 24, color = Color(240, 240, 240)):
        super().__init__(
            text = "",
            x = x,
            y = y,
            font_size = font_size,
            color = color
        )

    def update(self):
        self.text = str(get_fps() / 1)