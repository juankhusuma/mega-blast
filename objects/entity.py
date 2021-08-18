class AnimateEntity:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed

    def moveX(self):
        self.x += self.speed

    def moveY(self):
        self.y += self.speed

class InanimateEntity:
    def __init__(self, tileX, tileY, tilesize):
        self.x, self.y = tileX * tilesize, tileY * tilesize

    
    