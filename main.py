from objects.game import Game
from objects.map import MapFactory, MapRenderer
from objects.text import Text
from pygame import init, display, event, QUIT, quit, time
import sys
MapFactory()
init()

display.set_caption("Mega Blast 2")
clock = time.Clock()
mapRenderer = MapRenderer()


def main():
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
        Game.surface.fill("black")
        mapRenderer.render()
        frameRateGauge = Text(str(int(clock.get_fps())), size="xl",
                              fg="white", bg="black", align="top-right")
        display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
