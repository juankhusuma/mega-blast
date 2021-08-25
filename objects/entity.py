from objects.game import Game
from pygame import image
from pygame.transform import scale


class AnimateEntity(Game):
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.sprite = None
        self.moveSprite = []
        self.idleSprite = []
        super().__init__()

    def moveX(self):
        self.x += self.speed

    def moveY(self):
        self.y += self.speed


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


class Player(AnimateEntity):
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed)
        moveSpritePath = "assets/images/player{}/move".format(id)
        idleSpritePath = "assets/images/player{}/idle".format(id)
        moveImage1 = image.load(moveSpritePath+"/move1.png")
        moveImage2 = image.load(moveSpritePath+"/move2.png")
        [self.moveSprite.append(moveImage1) for _ in range(3)]
        [self.moveSprite.append(moveImage2) for _ in range(3)]
        idleImage1 = image.load(idleSpritePath+"/idle/idle1.png")
        idleImage2 = image.load(idleSpritePath+"/idle/idle2.png")
        [self.idleSprite.append(idleImage1) for _ in range(5)]
        self.idleSprite.append(idleImage2)


class Mimic(InanimateEntity):
    sprite_idle = scale(image.load("assets/images/enemies/mimic/1.png"),
                        (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite_aggrovated = scale(image.load("assets/images/enemies/mimic/2.png"),
                              (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite = sprite_idle
