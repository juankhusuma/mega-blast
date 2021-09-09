from objects.game import Game
from pygame import Rect, image
from pygame.transform import scale


class AnimateEntity(Game):
    def __init__(self, x, y, speed):
        # Speed will be in tile per second
        self.x = x
        self.y = y
        self.__speed = speed
        self.Rect = Rect(0, 0, 0, 0)
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
        self.collision_types = {
            "top": False,
            "left": False,
            "bottom": False,
            "right": False
        }
        super().__init__()

    def __updateSpeed(self):
        if Game.framerate > 0:
            self.speed = self.__speed * Game.settings["game.tileSize"] / Game.framerate
        else:
            self.speed = 0

    @staticmethod
    def collission_test(rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile.Rect) == 1 and not isinstance(tile, Empty)]

    def move(self):
        self.__updateSpeed()
        if self.faceUp:
            self.y -= self.speed
        if self.faceDown:
            self.y += self.speed
        self.Rect.y = self.y 
        hit_list = self.collission_test(self.Rect, Game.map_item)
        for tile in hit_list:
            if self.faceUp:
                self.Rect.top  = tile.Rect.bottom
            if self.faceDown:
                self.Rect.bottom = tile.Rect.top

        if self.faceLeft:
            self.x -= self.speed
        if self.faceRight:
            self.x += self.speed
        self.Rect.x = self.x
        hit_list = self.collission_test(self.Rect, Game.map_item)
        for tile in hit_list:
            if self.faceLeft:
                self.Rect.left = tile.Rect.right
            if self.faceRight:
                self.Rect.right = tile.Rect.left

        self.x = self.Rect.x
        self.y = self.Rect.y


class InanimateEntity(Game):
    sprite = None
    tile_size = Game.settings["game.tileSize"]

    def __init__(self, tileX, tileY, offsetX, offsetY):
        self.x, self.y = (tileX * InanimateEntity.tile_size) + offsetX, (tileY * InanimateEntity.tile_size) + offsetY
        self.Rect = Rect(self.x, self.y, Game.settings["game.tileSize"], Game.settings["game.tileSize"])
        super().__init__()


class Empty(InanimateEntity):
    def __str__(self):
        return "Empty<{},{}>".format(self.x, self.y)


class Box(InanimateEntity):
    sprite = scale(image.load("assets/images/box.png"),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))

    def __str__(self):
        return "Box<{},{}>".format(self.x, self.y)


class Wall(InanimateEntity):
    sprite = scale(image.load("assets/images/wall.png"),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))

    def __str__(self):
        return "Wall<{},{}>".format(self.x, self.y)


class Mimic(InanimateEntity):
    sprite_idle = scale(image.load("assets/images/enemies/mimic/1.png"),
                        (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite_aggrovated = scale(image.load("assets/images/enemies/mimic/2.png"),
                              (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite = sprite_idle

    def withinVicinity(self, pos):
        [x, y] = pos
        return (self.x - x)**2 + (self.y-y)**y <= 5

    def __str__(self):
        return "Mimic<{},{}>".format(self.x, self.y)