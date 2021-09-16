from objects.text import Text
from objects.game import Game
from pygame import Rect, display, image, sprite
from pygame.transform import scale
from objects.stopwatch import Stopwatch
import math

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
        return math.sqrt((self.x - x)**2 + (self.y-y)**2 )<= 50

    def __str__(self):
        return "Mimic<{},{}>".format(self.x, self.y)

class BombItem(InanimateEntity):
    sprite = scale(image.load("assets/images/regular_bomb.png"), (int(InanimateEntity.tile_size * 0.5), int(InanimateEntity.tile_size * 0.5)))
    def __init__(self, tileX, tileY, offsetX, offsetY):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.x += (self.tile_size - BombItem.sprite.get_width())/2 
        self.x += (self.tile_size - BombItem.sprite.get_height())/2 
        self.player = None

class Explosion(InanimateEntity):
    def __init__(self, tileX, tileY, offsetX, offsetY, placed_by):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.timer = Stopwatch()
        self.timer.reset()
        self.player = placed_by

    def update(self):
        if self.timer.time_elapsed() > 500:
            Game.explosions.pop(0)


class BombActive(InanimateEntity):
    sprite = scale(image.load("assets/images/regular_bomb.png"), (InanimateEntity.tile_size, InanimateEntity.tile_size))
    def __init__(self, tileX, tileY, offsetX, offsetY, placed_by):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.player = None
        self.player = placed_by
        self.timer = Stopwatch()
        self.timer.reset()
        self.text = Text(str(self.player.id), size="xs", fg="white", bg="black", align=[self.player.x, self.player.y], display=False)
        self.text.x += (BombActive.sprite.get_width() - self.text.text.get_width())/2
        self.text.y += (BombActive.sprite.get_height() - self.text.text.get_height())/2
        self.animations = []
        self.animations += [scale(image.load("assets/images/regular_bomb.png"), (InanimateEntity.tile_size, InanimateEntity.tile_size)) for _ in range(10)]
        self.animations += [scale(image.load("assets/images/ignited_bomb.png"), (InanimateEntity.tile_size, InanimateEntity.tile_size)) for _ in range(10)]
        self.frame = 0

    def explode(self):
        Game.bomb_items.pop(0)

    def update(self):
        if self.frame < len(self.animations) - 1:
            self.frame += 1
        else:
            self.frame = 0
        BombActive.sprite = self.animations[self.frame]
        Game.surface.blit(BombActive.sprite, (self.x, self.y))
        Game.surface.blit(self.text.text, (self.text.x, self.text.y))
        if self.timer.time_elapsed() > 1_000:
            self.explode()

    def __str__(self):
        return "Bomb<time:{}>".format(1_000 - self.timer.time_elapsed())

class PowerUp(InanimateEntity):
    pass

class NoClip(PowerUp):
    pass

class ExtraBlast(PowerUp):
    pass

