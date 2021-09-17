from objects.stopwatch import Stopwatch
from objects.game import Game
from objects.entity import AnimateEntity, BombActive, BombItem, Explosion
from objects.text import Text
from pygame import Rect, image

class Player(AnimateEntity, Game):
    animations = {
        1: {
            "move": [* [image.load("assets/images/player1/move/move1.png").convert() for _ in range(10)], * [image.load("assets/images/player1/move/move2.png").convert() for _ in range(5)]],
            "idle": [* [image.load("assets/images/player1/idle/idle1.png").convert() for _ in range(20)], * [image.load("assets/images/player1/idle/idle6.png").convert() for _ in range(10)]]
        },
        2: {
            "move": [* [image.load("assets/images/player2/move/move1.png").convert() for _ in range(10)], * [image.load("assets/images/player2/move/move2.png").convert() for _ in range(5)]],
            "idle": [* [image.load("assets/images/player2/idle/idle1.png").convert() for _ in range(20)], * [image.load("assets/images/player2/idle/idle6.png").convert() for _ in range(10)]]
        },
        3: {
            "move": [* [image.load("assets/images/player3/move/move1.png").convert() for _ in range(10)], * [image.load("assets/images/player3/move/move2.png").convert() for _ in range(5)]],
            "idle": [* [image.load("assets/images/player3/idle/idle1.png").convert() for _ in range(20)], * [image.load("assets/images/player3/idle/idle6.png").convert() for _ in range(10)]]
        },
        4: {
            "move": [* [image.load("assets/images/player4/move/move1.png").convert() for _ in range(10)], * [image.load("assets/images/player4/move/move2.png").convert() for _ in range(5)]],
            "idle": [* [image.load("assets/images/player4/idle/idle1.png").convert() for _ in range(20)], * [image.load("assets/images/player4/idle/idle6.png").convert() for _ in range(10)]]
        },
    }
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed)

        self.id = id
        self.frame = 0
        self.bomb_count = 3

        self.idle = True
        self.facingUp = False
        self.facingDown = False
        self.facingLeft = False
        self.facingRight = False
        self.timer = Stopwatch()
        self.superBomb = True
        self.is_bot = False
        self.idleAnimation = Player.animations[id]["idle"]
        self.moveAnimation = Player.animations[id]["move"]

        self.sprite = self.idleAnimation[0]
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
            if self.frame < len(self.idleAnimation) - 1:
                self.frame += 1
            else:
                self.frame = 0
            self.sprite = self.idleAnimation[self.frame]
        else:
            if self.frame < len(self.moveAnimation) - 1:
                self.frame += 1
            else:
                self.frame = 0 
            self.sprite = self.moveAnimation[self.frame]
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