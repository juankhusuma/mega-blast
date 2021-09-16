from objects.stopwatch import Stopwatch
from objects.game import Game
from objects.entity import AnimateEntity, BombActive, BombItem, Explosion
from objects.text import Text
from pygame import Rect, image

class Player(AnimateEntity, Game):
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed)

        self.id = id
        self.frame = 0
        self.bomb_count = 3
        moveSpritePath = "assets/images/player{}/move".format(id)
        idleSpritePath = "assets/images/player{}/idle".format(id)
        moveImage1 = image.load(moveSpritePath+"/move1.png")
        moveImage2 = image.load(moveSpritePath+"/move2.png")
        idleImage1 = image.load(idleSpritePath+"/idle1.png")
        idleImage2 = image.load(idleSpritePath+"/idle6.png")
        self.idle = True
        self.facingUp = False
        self.facingDown = False
        self.facingLeft = False
        self.facingRight = False
        self.timer = Stopwatch()
        self.superBomb = True
        self.is_bot = False

        [self.moveSprite.append(moveImage1) for _ in range(10)]
        [self.moveSprite.append(moveImage2) for _ in range(5)]
        [self.idleSprite.append(idleImage1) for _ in range(20)]
        [self.idleSprite.append(idleImage2) for _ in range(10)]

        self.sprite = idleImage1
        self.Rect = Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        self.has_bomb = True

    def renderIdTag(self):
        id_label = Text(str(self.id), size="xs", fg="white", bg="black", align=[self.x + self.sprite.get_width()/2, self.y], display=False)
        id_label.y -= id_label.text.get_height() + 5
        id_label.x -= id_label.text.get_width()/2
        Game.surface.blit(id_label.text, (id_label.x, id_label.y))

    def placeBomb(self):
        if self.has_bomb:
            self.has_bomb = False
            self.timer.reset()
            Game.bomb_items.append(BombActive(
                self.tile_x,
                self.tile_y,
                self.x_offset,
                self.y_offset,
                self
            ))

    def animate(self):
        if self.timer.time_elapsed() > 1_000:
            self.has_bomb = True
        if self.idle:
            if self.frame < len(self.idleSprite) - 1:
                self.frame += 1
            else:
                self.frame = 0
            self.sprite = self.idleSprite[self.frame]
        else:
            if self.frame < len(self.moveSprite) - 1:
                self.frame += 1
            else:
                self.frame = 0 
            self.sprite = self.moveSprite[self.frame]
        Game.surface.blit(self.sprite, (self.Rect.x, self.Rect.y))
        self.renderIdTag()
        item = BombItem(
            (self.x-self.x_offset)/Game.settings["game.tileSize"], 
            (self.y-self.y_offset)/Game.settings["game.tileSize"],
            self.x_offset,
            self.y_offset)
        if self.has_bomb:
            Game.surface.blit(BombItem.sprite, (item.x, item.y))

        for i in self.hit_test(self.Rect, Game.explosions):
            if i.player != self:
                if not self.is_bot:
                    Game.players.remove(self)
                else:
                    Game.bots.remove(self)
                i.player.kills += 1

class Bot(Player):
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed, id)
        self.is_bot = True

    def renderIdTag(self):
        id_label = Text(str(self.id), size="xs", fg="red", bg="black", align=[self.x + self.sprite.get_width()/2, self.y], display=False)
        id_label.y -= id_label.text.get_height() + 5
        id_label.x -= id_label.text.get_width()/2
        Game.surface.blit(id_label.text, (id_label.x, id_label.y))