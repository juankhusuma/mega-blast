from typing import Text
from pygame import Rect, Surface, mouse
from objects.game import Game

class Cursor(Game):
    position = mouse.get_pos()
    x, y = position
    def __init__(self):
        super().__init__()
        Cursor.x, Cursor.y = mouse.get_pos()

    @classmethod
    def hovered_text(klass, other):
        klass.x, klass.y = mouse.get_pos()
        other = Rect(other.x, other.y, other.text.get_width(), other.text.get_height())
        return Rect(klass.x, klass.y, 10, 10).colliderect(other)

    def __str__(self):
        return "Cursor<{},{}>".format(Cursor.x, Cursor.y)