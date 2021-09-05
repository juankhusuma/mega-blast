from pygame.constants import KEYDOWN, K_ESCAPE, K_a, K_d, K_s, K_w
from objects.player import Player
from objects.game import Game
from objects.cursor import Cursor
from objects.map import MapFactory, MapRenderer
from objects.text import Text
from pygame import cursors, image, init, display, event, QUIT, mouse, quit, time, draw
import sys
import time as TIME
mapFactory = MapFactory()
init()

display.set_caption("Mega Blast")
clock = time.Clock()
mapRenderer = MapRenderer()

start = False
open_option = False
open_quit_option = False
open_option_input_prompt  = False

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
            TIME.sleep(0.3)
    Game.surface.blit(play_txt.text, (play_txt.x, play_txt.y))

    option_txt = Text("Options", size="l", fg="white", bg="black", align="mid-center")
    if cursor.hovered_text(option_txt):
        option_txt = Text("Options", size="l", fg=[150, 150, 150], bg="black", align="mid-center")
        if mouse.get_pressed()[0]:
            open_option = True
            TIME.sleep(0.3)

    quit_txt = Text("Quit", size="l", fg="white", bg="black", align="mid-center", display=False)
    quit_txt.y += 60
    if cursor.hovered_text(quit_txt):
        quit_txt = Text("Quit", size="l", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        quit_txt.y += 60
        if mouse.get_pressed()[0]:
            open_quit_option = True
            TIME.sleep(0.3)
    Game.surface.blit(quit_txt.text, (quit_txt.x, quit_txt.y))

def option_form_prompt():
    global open_option, open_option_input_prompt, mapFactory
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
        if mouse.get_pressed()[0]:
            open_option = False
            open_option_input_prompt = False
            mapFactory = MapFactory()
            TIME.sleep(0.3)
    if cursor.hovered_text(no):
        no = Text("No", size="s", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        no.y += warning1.text.get_height() * 2 + 40
        no.x += 50
        if mouse.get_pressed()[0]:
            open_option_input_prompt = False
            TIME.sleep(0.3)

    Game.surface.blit(yes.text, (yes.x, yes.y))
    Game.surface.blit(no.text, (no.x, no.y))

def options_menu():
    global open_option_input_prompt, open_option
    title = Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    back = Text("Return to Main Menu", size="m", fg="red", bg="black", align="top-center", display=False)
    back.y += title.text.get_height() + 20
    if cursor.hovered_text(back):
        back = Text("Return to Main Menu", size="m", fg=[50, 0, 0], bg="black", align="top-center", display=False)
        back.y += title.text.get_height() + 20
        if mouse.get_pressed()[0]:
            open_option = False
            TIME.sleep(0.3)

    player_count = Text("Player Count", size="m", fg="white", bg="black", align="top-center", display=False)
    player_count.y += title.text.get_height() + 20 + back.text.get_height() + 20

    player_count_options = [x + 1 for x in range(4)]
    map(player_count_options, lambda x: print(x))

    save = Text("Save Settings", size="m", fg="green", bg="black", align="bottom-center")
    if cursor.hovered_text(save):
        save = Text("Save Settings", size="m", fg=[0, 50, 0], bg="black", align="bottom-center")
        if mouse.get_pressed()[0]:
            open_option_input_prompt = True

    Game.surface.blit(back.text, (back.x, back.y))
    Game.surface.blit(player_count.text, (player_count.x, player_count.y))

def quit_option_menu():
    global open_quit_option
    Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    warning1 = Text("Are you sure you want to quit?", size="m", fg="white", bg="black", align="mid-center", display=False)
    Game.surface.blit(warning1.text, (warning1.x, warning1.y))
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
        if mouse.get_pressed()[0]:
            quit()
            sys.exit()
    if cursor.hovered_text(no):
        no = Text("No", size="s", fg=[150, 150, 150], bg="black", align="mid-center", display=False)
        no.y += warning1.text.get_height() * 2 + 40
        no.x += 50
        if mouse.get_pressed()[0]:
            open_quit_option = False
            TIME.sleep(0.3)
    Game.surface.blit(yes.text, (yes.x, yes.y))
    Game.surface.blit(no.text, (no.x, no.y))


def main():
    global start, open_option, cursor, open_quit_option, open_option_input_prompt
    player1 = Player(0, 0, 5, 1)
    while True:
        cursor = Cursor()
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                start = False
                open_option = False
                open_quit_option = False
                open_option_input_prompt = False
            if e.type == KEYDOWN:
                if e.key == K_w: # Up
                    pass
                if e.key == K_a: # Left
                    pass
                if e.key == K_s: # Down
                    pass
                if e.key == K_d: # Right
                    pass
                
        Game.surface.fill("black")

        if start:
            mapRenderer.render()
            Game.framerate = int(clock.get_fps())
            Text(str(Game.framerate), size="xl", fg="white", bg="black", align="top-right")
            back_txt = Text("Back", size="m", fg="white", bg="black", align="top-left")
            if Cursor().hovered_text(back_txt):
                back_txt = Text("Back", size="m", fg=[150, 150, 150], bg="black", align="top-left")
                if mouse.get_pressed()[0]:
                    start = False
                    TIME.sleep(0.3)

        elif open_option_input_prompt:
            option_form_prompt()

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

