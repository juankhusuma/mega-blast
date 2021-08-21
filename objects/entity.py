from objects.game import Game
from pygame import image
from pygame.transform import scale


class AnimateEntity(Game):
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        super().__init__()

    def moveX(self):
        self.x += self.speed

    def moveY(self):
        self.y += self.speed


class InanimateEntity(Game):
    def __init__(self, tileX, tileY):
        self.x, self.y = tileX * self.tile_size, tileY * self.tile_size
        super().__init__()


class Box(InanimateEntity):
    sprite = scale(image.load("assets/images/box.png"), (24, 24))

    def __init__(self, tileX, tileY):
        self.tile_size = Box.sprite.get_width()
        super().__init__(tileX, tileY)


class Wall(InanimateEntity):
    sprite = scale(image.load("assets/images/wall.png"), (24, 24))

    def __init__(self, tileX, tileY):
        self.tile_size = Wall.sprite.get_width()
        super().__init__(tileX, tileY)
