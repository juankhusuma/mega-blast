from pygame.constants import KEYDOWN, K_ESCAPE
from objects.entity import Player
from objects.game import Game
from objects.cursor import Cursor
from objects.map import MapFactory, MapRenderer
from objects.text import Text
from pygame import image, init, display, event, QUIT, mouse, quit, time, draw
import sys
MapFactory()
init()

display.set_caption("Mega Blast")
clock = time.Clock()
mapRenderer = MapRenderer()

start = False
open_option = False


def main():
    global start
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                start = False
        Game.surface.fill("black")
        if start:
            mapRenderer.render()
            Text(str(int(clock.get_fps())), size="xl", fg="white", bg="black", align="top-right")
        else:
            Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
            play_txt = Text("Play", size="l", fg="white", bg="black", align="mid-center", display=False)
            play_txt.y -= 60
            if Cursor().hovered_text(play_txt):
                play_txt = Text("Play", size="l", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
                play_txt.y -= 60
                if mouse.get_pressed()[0]:
                    start = True
            Game.surface.blit(play_txt.text, (play_txt.x, play_txt.y))

            option_txt = Text("Options", size="l", fg="white", bg="black", align="mid-center")
            if Cursor().hovered_text(option_txt):
                option_txt = Text("Options", size="l", fg=[150, 150, 150], bg="black", align="mid-center")

            quit_txt = Text("Quit", size="l", fg="white", bg="black", align="mid-center", display=False)
            quit_txt.y += 60
            if Cursor().hovered_text(quit_txt):
                quit_txt = Text("Quit", size="l", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
                quit_txt.y += 60
                if mouse.get_pressed()[0]:
                    quit()
                    sys.exit()
            Game.surface.blit(quit_txt.text, (quit_txt.x, quit_txt.y))

        display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

