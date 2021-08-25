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
    tile_size = Game.settings["game.tileSize"]

    def __init__(self, tileX, tileY):
        self.x, self.y = tileX * InanimateEntity.tile_size, tileY * InanimateEntity.tile_size
        super().__init__()


class Box(InanimateEntity):
    sprite = scale(image.load("assets/images/box.png"),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))
    invincible = False

    def __init__(self, tileX, tileY):
        super().__init__(tileX, tileY)

    def __str__(self):
        return "Box<{},{}>".format(self.x, self.y)


class Wall(InanimateEntity):
    sprite = scale(image.load("assets/images/wall.png"),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))
    invincible = True

    def __init__(self, tileX, tileY):
        super().__init__(tileX, tileY)

    def __str__(self):
        return "Wall<{},{}>".format(self.x, self.y)


def Player(AnimateEntity):
    pass
