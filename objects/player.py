from objects.entity import AnimateEntity
from pygame import image

class Player(AnimateEntity):
    def __init__(self, x, y, speed, id):
        super().__init__(x, y, speed)
        moveSpritePath = "assets/images/player{}/move".format(id)
        idleSpritePath = "assets/images/player{}/idle".format(id)
        moveImage1 = image.load(moveSpritePath+"/move1.png")
        moveImage2 = image.load(moveSpritePath+"/move2.png")
        idleImage1 = image.load(idleSpritePath+"/idle1.png")
        idleImage2 = image.load(idleSpritePath+"/idle2.png")
        self.idle = True
        self.facingUp = False
        self.facingDown = False
        self.facingLeft = False
        self.facingRight = False

        [self.moveSprite.append(moveImage1) for _ in range(3)]
        [self.moveSprite.append(moveImage2) for _ in range(3)]
        [self.idleSprite.append(idleImage1) for _ in range(5)]
        self.idleSprite.append(idleImage2)

        self.sprite = self.idleSprite[0]

    def move(self):
        if not self.idle:
            if self.facingUp: 
                self.moveUp()
            if self.facingDown: 
                self.moveDown()
            if self.facingLeft: 
                self.moveLeft()
            if self.facingRight: 
                self.moveRight()