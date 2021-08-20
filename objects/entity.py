from objects.game import Game


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
    def __init__(self, tileX, tileY, tilesize):
        self.x, self.y = tileX * tilesize, tileY * tilesize
        super().__init__()


class Box(InanimateEntity):
    def __init__(self, tileX, tileY, tilesize, spritePath):
        super().__init__(tileX, tileY, tilesize)
