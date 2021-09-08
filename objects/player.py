from objects.game import Game
from objects.entity import AnimateEntity
from objects.text import Text
from pygame import image

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

        [self.moveSprite.append(moveImage1) for _ in range(10)]
        [self.moveSprite.append(moveImage2) for _ in range(5)]
        [self.idleSprite.append(idleImage1) for _ in range(20)]
        [self.idleSprite.append(idleImage2) for _ in range(10)]

        self.sprite = idleImage1

    def animate(self):
        id_label = Text(str(self.id), size="xs", fg="white", bg="black", align=[self.x + self.sprite.get_width()/2, self.y], display=False)
        id_label.y -= id_label.text.get_height() + 5
        id_label.x -= id_label.text.get_width()/2
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
        Game.surface.blit(self.sprite, (self.x, self.y))
        Game.surface.blit(id_label.text, (id_label.x, id_label.y))



        


class Bot(Player):
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed, id)