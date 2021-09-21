from objects.text import Text
from objects.game import Game
from pygame import Rect, image
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
        self.sprite = None
        self.idle = False
        self.faceUp = False
        self.faceDown = False
        self.faceLeft = False
        self.faceRight = False
        self.moveSprite = []
        self.idleSprite = []
        self.kills = 0
        super().__init__()

    @staticmethod
    def collission_test(rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile.Rect) == 1 and not isinstance(tile, Empty)]

    @staticmethod
    def hit_test(rect, explosions):
        return [fire for fire in explosions if rect.colliderect(fire.Rect) == 1]

    def move(self):
        if Game.framerate > 0:
            self.speed = self.__speed * Game.settings["game.tileSize"] / Game.framerate
        else:
            self.speed = 0
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
        self.tile_x = round((self.x-self.x_offset)/Game.settings["game.tileSize"])
        self.tile_y = round((self.y-self.y_offset)/Game.settings["game.tileSize"])



class InanimateEntity(Game):
    sprite = None
    tile_size = Game.settings["game.tileSize"]

    def __init__(self, tileX, tileY, offsetX, offsetY):
        self.tileX = tileX
        self.tileY = tileY
        self.x, self.y = (tileX * InanimateEntity.tile_size) + offsetX, (tileY * InanimateEntity.tile_size) + offsetY
        self.Rect = Rect(self.x, self.y, Game.settings["game.tileSize"], Game.settings["game.tileSize"])
        super().__init__()


class Empty(InanimateEntity):
    def __str__(self):
        return "Empty<{}({}),{}({})>".format(self.x, self.tileX, self.y, self.tileY)


class Box(InanimateEntity):
    sprite = scale(image.load("assets/images/box.png").convert(),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))

    def __str__(self):
        return "Box<{}({}),{}({})>".format(self.x, self.tileX, self.y, self.tileY)


class Wall(InanimateEntity):
    sprite = scale(image.load("assets/images/wall.png").convert(),
                   (InanimateEntity.tile_size, InanimateEntity.tile_size))

    def __str__(self):
        return "Wall<{}({}),{}({})>".format(self.x, self.tileX, self.y, self.tileY)


class Mimic(InanimateEntity):
    sprite_idle = scale(image.load("assets/images/enemies/mimic/1.png").convert(),
                        (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite_aggrovated = scale(image.load("assets/images/enemies/mimic/2.png").convert(),
                              (InanimateEntity.tile_size, InanimateEntity.tile_size))
    sprite = sprite_idle

    def withinVicinity(self, pos):
        [x, y] = pos
        return math.sqrt((self.x - x)**2 + (self.y-y)**2 )<= 50

    def __str__(self):
        return "Mimic<{}({}),{}({})>".format(self.x, self.tileX, self.y, self.tileY)

class BombItem(InanimateEntity):
    sprite = scale(image.load("assets/images/regular_bomb.png").convert(), (int(InanimateEntity.tile_size * 0.5), int(InanimateEntity.tile_size * 0.5)))
    sprite.set_colorkey((0, 0, 0, 0))
    def __init__(self, tileX, tileY, offsetX, offsetY):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.x += (self.tile_size - BombItem.sprite.get_width())/2 
        self.x += (self.tile_size - BombItem.sprite.get_height())/2 
        self.player = None

class Explosion(InanimateEntity):
    animations = []
    animations += [scale(image.load("assets/images/explosions/explosion{}.png".format(j + 1)).convert(), (InanimateEntity.tile_size, InanimateEntity.tile_size)) for j in range(6)]
    def __init__(self, tileX, tileY, offsetX, offsetY, placed_by):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.timer = Stopwatch()
        self.timer.reset()
        self.player = placed_by
        self.animations = []
        self.frame = 0
        
        Explosion.sprite = Explosion.animations[0]

    def animate(self):
        if self.frame < len(Explosion.animations) - 1:
            self.frame += 1
        else:
            self.frame = 0
        Explosion.sprite = Explosion.animations[self.frame]
        Game.surface.blit(Explosion.sprite, (self.x, self.y))
        if self.timer.time_elapsed() > 200:
            Game.entites.pop(0)


class BombActive(InanimateEntity):
    sprite = scale(image.load("assets/images/regular_bomb.png").convert(), (InanimateEntity.tile_size, InanimateEntity.tile_size))
    animations = []
    animations += [scale(image.load("assets/images/regular_bomb.png").convert(), (InanimateEntity.tile_size, InanimateEntity.tile_size)) for _ in range(10)]
    animations += [scale(image.load("assets/images/ignited_bomb.png").convert(), (InanimateEntity.tile_size, InanimateEntity.tile_size)) for _ in range(10)]

    def __init__(self, tileX, tileY, offsetX, offsetY, placed_by):
        super().__init__(tileX, tileY, offsetX, offsetY)
        self.player = placed_by
        self.timer = Stopwatch()
        self.timer.reset()
        self.text = Text(str(self.player.id), size="xs", fg="white", bg="black", align=[self.player.x, self.player.y], display=False)
        self.text.x += (BombActive.sprite.get_width() - self.text.text.get_width())/2
        self.text.y += (BombActive.sprite.get_height() - self.text.text.get_height())/2
        self.frame = 0
        self.stop_propagation = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,
        }

    def __add_explosion_up(self, i):
        item = Game.map_item[Game.change2Dto1DIndex(self.tileX, self.tileY - i)]
        if isinstance(item, Wall):
            self.stop_propagation["UP"] = True
        else:
            Game.map_item[Game.change2Dto1DIndex(self.tileX, self.tileY - i)] = Empty(self.tileX, self.tileY - i, self.x_offset, self.y_offset)
            Game.entites.append(Explosion(self.tileX, self.tileY - i, self.x_offset, self.y_offset, self.player)) # Up

    def __add_explosion_down(self, i):
        item = Game.map_item[Game.change2Dto1DIndex(self.tileX, self.tileY + i)]
        if isinstance(item, Wall):
            self.stop_propagation["DOWN"] = True
        else:
            Game.map_item[Game.change2Dto1DIndex(self.tileX, self.tileY + i)] = Empty(self.tileX, self.tileY + i, self.x_offset, self.y_offset)
            Game.entites.append(Explosion(self.tileX, self.tileY + i, self.x_offset, self.y_offset, self.player)) # Down

    def __add_explosion_left(self, i):
        item = Game.map_item[Game.change2Dto1DIndex(self.tileX - i, self.tileY)]
        if isinstance(item, Wall):
            self.stop_propagation["LEFT"] = True
        else:
            Game.map_item[Game.change2Dto1DIndex(self.tileX - i, self.tileY)] = Empty(self.tileX - i, self.tileY, self.x_offset, self.y_offset)
            Game.entites.append(Explosion(self.tileX - i, self.tileY, self.x_offset, self.y_offset, self.player)) # Left

    def __add_explosion_right(self, i):
        item = Game.map_item[Game.change2Dto1DIndex(self.tileX + i, self.tileY)]
        if isinstance(item, Wall):
            self.stop_propagation["RIGHT"] = True
        else:
            Game.map_item[Game.change2Dto1DIndex(self.tileX + i, self.tileY)] = Empty(self.tileX + i, self.tileY, self.x_offset, self.y_offset)
            Game.entites.append(Explosion(self.tileX + i, self.tileY, self.x_offset, self.y_offset, self.player)) # Right

    def explode(self):
        Game.entites.append(Explosion(self.tileX, self.tileY, self.x_offset, self.y_offset, self.player))
        if not self.player.superBomb:
            for i in range(1, 3):
                if not self.stop_propagation["UP"]:
                    self.__add_explosion_up(i)
                if not self.stop_propagation["DOWN"]:
                    self.__add_explosion_down(i)
                if not self.stop_propagation["LEFT"]:
                    self.__add_explosion_left(i)
                if not self.stop_propagation["RIGHT"]:
                    self.__add_explosion_right(i)
        else:
            for i in range(1, 5):              
                if not self.stop_propagation["UP"]:
                    self.__add_explosion_up(i)
                if not self.stop_propagation["DOWN"]:
                    self.__add_explosion_down(i)
                if not self.stop_propagation["LEFT"]:
                    self.__add_explosion_left(i)
                if not self.stop_propagation["RIGHT"]:
                    self.__add_explosion_right(i)
        Game.entites.pop(0)
        self.stop_propagation["UP"] = False
        self.stop_propagation["DOWN"] = False
        self.stop_propagation["LEFT"] = False
        self.stop_propagation["RIGHT"] = False

    def animate(self):
        if self.frame < len(BombActive.animations) - 1:
            self.frame += 1
        else:
            self.frame = 0
        BombActive.sprite = BombActive.animations[self.frame]
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

