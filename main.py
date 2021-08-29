from pygame.constants import KEYDOWN, K_ESCAPE
from objects.entity import Player
from objects.game import Game
from objects.cursor import Cursor
from objects.map import MapFactory, MapRenderer
from objects.text import Text
from pygame import cursors, image, init, display, event, QUIT, mouse, quit, time, draw
import sys
import time as TIME
MapFactory()
init()

display.set_caption("Mega Blast")
clock = time.Clock()
mapRenderer = MapRenderer()

start = False
open_option = False
open_quit_option = False

def main_menu():
    global start, open_option, open_quit_option
    Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    play_txt = Text("Play", size="l", fg="white", bg="black", align="mid-center", display=False)
    play_txt.y -= 60
    if cursor.hovered_text(play_txt):
        play_txt = Text("Play", size="l", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        play_txt.y -= 60
        if mouse.get_pressed()[0]:
            start = True
            TIME.sleep(0.1)
    Game.surface.blit(play_txt.text, (play_txt.x, play_txt.y))

    option_txt = Text("Options", size="l", fg="white", bg="black", align="mid-center")
    if cursor.hovered_text(option_txt):
        option_txt = Text("Options", size="l", fg=[150, 150, 150], bg="black", align="mid-center")
        if mouse.get_pressed()[0]:
            open_option = True
            TIME.sleep(0.1)

    quit_txt = Text("Quit", size="l", fg="white", bg="black", align="mid-center", display=False)
    quit_txt.y += 60
    if cursor.hovered_text(quit_txt):
        quit_txt = Text("Quit", size="l", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        quit_txt.y += 60
        if mouse.get_pressed()[0]:
            open_quit_option = True
    Game.surface.blit(quit_txt.text, (quit_txt.x, quit_txt.y))

def options_menu():
    global open_option
    Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    warning1 = Text("Changing any value in the option will override", size="s", fg="white", bg="black", align="mid-center", display=False)
    warning2 = Text("your current game, Proceed?", size="s", fg="white", bg="black", align="mid-center", display=False)
    warning2.y += warning1.text.get_height()
    Game.surface.blit(warning1.text, (warning1.x, warning1.y))
    Game.surface.blit(warning2.text, (warning2.x, warning2.y))
    yes = Text("Yes", size="s", fg="white", bg="black", align="mid-center", display=False)
    no = Text("No", size="s", fg="white", bg="black", align="mid-center", display=False)
    yes.y += warning1.text.get_height() * 2 + 40
    yes.x -= 50
    no.y += warning1.text.get_height() * 2 + 40
    no.x += 50

    if cursor.hovered_text(yes):
        yes = Text("Yes", size="s", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        yes.y += warning1.text.get_height() * 2 + 40
        yes.x -= 50
    if cursor.hovered_text(no):
        no = Text("No", size="s", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        no.y += warning1.text.get_height() * 2 + 40
        no.x += 50
        if mouse.get_pressed()[0]:
            open_option = False
            TIME.sleep(0.1)

    Game.surface.blit(yes.text, (yes.x, yes.y))
    Game.surface.blit(no.text, (no.x, no.y))

def quit_option_menu():
    global open_quit_option
    Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    warning1 = Text("Are you sure you want to quit?", size="m", fg="white", bg="black", align="mid-center", display=False)
    Game.surface.blit(warning1.text, (warning1.x, warning1.y))
    yes = Text("Yes", size="m", fg="white", bg="black", align="mid-center", display=False)
    no = Text("No", size="m", fg="white", bg="black", align="mid-center", display=False)
    yes.y += warning1.text.get_height() * 2 + 40
    yes.x -= 50
    no.y += warning1.text.get_height() * 2 + 40
    no.x += 50

    if cursor.hovered_text(yes):
        yes = Text("Yes", size="m", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        yes.y += warning1.text.get_height() * 2 + 40
        yes.x -= 50
        if mouse.get_pressed()[0]:
            quit()
            sys.exit()
    if cursor.hovered_text(no):
        no = Text("No", size="m", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        no.y += warning1.text.get_height() * 2 + 40
        no.x += 50
        if mouse.get_pressed()[0]:
            open_quit_option = False
            TIME.sleep(0.1)
    Game.surface.blit(yes.text, (yes.x, yes.y))
    Game.surface.blit(no.text, (no.x, no.y))

def main():
    global start, open_option, cursor
    while True:
        cursor = Cursor()
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                start = False
                open_option = False
        Game.surface.fill("black")

        if start:
            mapRenderer.render()
            Text(str(int(clock.get_fps())), size="xl", fg="white", bg="black", align="top-right")
            back_txt = Text("Back", size="m", fg="white", bg="black", align="top-left")
            if Cursor().hovered_text(back_txt):
                back_txt = Text("Back", size="m", fg=[150, 150, 150], bg="black", align="top-left")
                if mouse.get_pressed()[0]:
                    start = False
                    TIME.sleep(0.1)


        elif open_option:
            options_menu()

                
        elif open_quit_option:
            quit_option_menu()

        else:
            main_menu()

        display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

