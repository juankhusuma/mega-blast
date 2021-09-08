from objects.game import Game
from pygame import image
from pygame.transform import scale


class AnimateEntity(Game):
    def __init__(self, x, y, speed):
        # Speed will be in tile per second
        self.x = x
        self.y = y
        self.__speed = speed
        self.speed = 0
        self.__updateSpeed()
        self.sprite = None
        self.idle = False
        self.faceUp = False
        self.faceDown = False
        self.faceLeft = False
        self.faceRight = False
        self.moveSprite = []
        self.idleSprite = []
        super().__init__()

    def __updateSpeed(self):
        if Game.framerate > 0:
            self.speed = self.__speed * Game.settings["game.tileSize"] / Game.framerate
        else:
            self.speed = 0

    def move(self):
        self.__updateSpeed()
        if self.faceUp:
            self.y -= self.speed
        if self.faceDown:
            self.y += self.speed
        if self.faceLeft:
            self.x -= self.speed
        if self.faceRight:
            self.x += self.speed


class InanimateEntity(Game):
    sprite = None
    tile_size = Game.settings["game.tileSize"]

    def __init__(self, tileX, tileY):
        self.x, self.y = tileX * InanimateEntity.tile_size, tileY * InanimateEntity.tile_size
        super().__init__()


class Empty(InanimateEntity):
    pass


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


class Mimic(InanimateEntity):
    sprite_idle = scale(image.load("assets/images/enemies/mimic/1.png"),
                        (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite_aggrovated = scale(image.load("assets/images/enemies/mimic/2.png"),
                              (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite = sprite_idle
