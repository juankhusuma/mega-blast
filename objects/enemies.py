from objects.entity import AnimateEntity
from pygame import image 
from pygame.transform import scale
from objects.game import Game
import math

class Harpies(AnimateEntity):
    animations = [
        scale(
            image.load("assets/images/enemies/harpies/{}.png".format(x+1)),
            (Game.settings["game.tileSize"],
            Game.settings["game.tileSize"])
        ) for x in range(3)
    ]
    sprite = animations[0]

    def get_nearest_player(self):
        return min([math.sqrt((player.x-self.x)**2+(player.y-self.y)**2), (player.x, player.y)] for player in Game.players)

    def __move(self, to):
        [x, y] = to
        if self.x > x:
            self.x -= self.speed
        if self.x < x:
            self.x += self.speed
        if self.y > y:
            self.y -= self.speed
        if self.y < y:
            self.y += self.speed


    def animate(self):
        self.__move(self.get_nearest_player()[1])
        if self.frame < len(Harpies.animations) - 1:
            self.frame += 1
            Harpies.sprite = Harpies.animations[self.frame]
        else:
            self.frame = 0
        Game.surface.blit(Harpies.sprite, (self.x, self.y))

class Hunter(AnimateEntity):
    sprite = scale(
        image.load("assets/images/enemies/hunter/1.png"), 
        (Game.settings["game.tileSize"], 
        Game.settings["game.tileSize"])
    )

    def get_nearest_player(self):
        return min([math.sqrt((player.x-self.x)**2+(player.y-self.y)**2), (player.x, player.y)] for player in Game.players)

    def __move(self, to):
        [x, y] = to
        if self.x > x:
            self.x -= self.speed
        if self.x < x:
            self.x += self.speed
        if self.y > y:
            self.y -= self.speed
        if self.y < y:
            self.y += self.speed

    def animate(self):
        self.__move(self.get_nearest_player()[1])
        Game.surface.blit(Hunter.sprite, (self.x, self.y))
