from pygame.transform import scale
from objects.entity import BombActive, Empty
from pygame.constants import K_RSHIFT, KEYDOWN, KEYUP, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_q, K_r, K_s, K_t, K_u, K_w
from objects.player import Player
from objects.game import Game
from objects.cursor import Cursor
from objects.map import MapFactory, MapRenderer
from objects.text import Text
from pygame import image, init, display, event, QUIT, math, mixer, mouse, quit, time, draw, mixer
import sys
import math
import time as TIME
mapFactory = MapFactory()
init()
mixer.init()

display.set_caption("Mega Blast")
clock = time.Clock()
mapRenderer = MapRenderer()

start = False
open_option = False
open_quit_option = False
open_option_input_prompt  = False

player_count_options = [x + 1 for x in range(4)]
bot_count_options = [x for x in range(4)]
win_limit_options = [x + 1 for x in range(9)]
player_count_selected = Game.gameConf["game.player.count"]
bot_count_selected = Game.gameConf["game.bot.count"]
win_limit_selected = Game.gameConf["game.win.limit"]

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
    global open_option, open_option_input_prompt, mapFactory, player_count_selected, bot_count_selected, win_limit_selected
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
            Game.modifyGameData("game-conf", { "game.player.count": player_count_selected, "game.bot.count": bot_count_selected, "game.win.limit": win_limit_selected })
            mapFactory = MapFactory()
            mapRenderer.start()
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

def options_menu():  # sourcery no-metrics
    global open_option_input_prompt, open_option, player_count_options, bot_count_options, win_limit_options, player_count_selected, bot_count_selected, win_limit_selected
    title = Text("Mega Blast!", size="xl", fg="white", bg="black", align="top-center")
    back = Text("Return to Main Menu", size="m", fg="red", bg="black", align="top-center", display=False)
    back.y += title.text.get_height() + 20
    if cursor.hovered_text(back):
        back = Text("Return to Main Menu", size="m", fg=[50, 0, 0], bg="black", align="top-center", display=False)
        back.y += title.text.get_height() + 20
        if mouse.get_pressed()[0]:
            open_option = False
            TIME.sleep(0.3)

    player_count = Text("Player Amount", size="m", fg="white", bg="black", align="top-center", display=False)
    player_count.y += title.text.get_height() + back.text.get_height() + 40

    for i, j in enumerate(player_count_options):
        text = Text(str(j), size="m", fg=[200, 200, 200], bg="black", align="top-center", display=False)
        text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + 60
        text.x = text.x + (i - 2)*45
        if cursor.hovered_text(text):
            text = Text(str(j), size="m", fg=[150, 150, 150], bg="black", align="top-center", display=False)
            text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + 60
            text.x = text.x + (i - 2)*45
            if mouse.get_pressed()[0]:
                player_count_selected = j
                TIME.sleep(0.3)
        Game.surface.blit(text.text, (text.x, text.y))
        if j == player_count_selected:
            draw.rect(Game.surface, (0, 250, 0), (text.x - 4, text.y - 4, text.text.get_width() + 6, text.text.get_height() + 6), 5)

    bot_count = Text("Bot Amount", size="m", fg="white", bg="black", align="top-center", display=False)
    bot_count.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + 80

    __text_height = text.text.get_height()

    for i, j in enumerate(bot_count_options):
        text = Text(str(j), size="m", fg=[200, 200, 200], bg="black", align="top-center", display=False)
        text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + bot_count.text.get_height() + 100
        text.x = text.x + (j - 2)*45
        if cursor.hovered_text(text):
            text = Text(str(j), size="m", fg=[150, 150, 150], bg="black", align="top-center", display=False)
            text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + bot_count.text.get_height() + 100
            text.x = text.x + (j - 2)*45
            if mouse.get_pressed()[0]:
                bot_count_selected = j
                TIME.sleep(0.3)
        Game.surface.blit(text.text, (text.x, text.y))
        if j == bot_count_selected:
            draw.rect(Game.surface, (0, 250, 0), (text.x - 4, text.y - 4, text.text.get_width() + 6, text.text.get_height() + 6), 5)

    win_limit = Text("Win Limit", size="m", fg="white", bg="black", align="top-center", display=False)
    win_limit.y +=  title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + bot_count.text.get_height() + __text_height + 120

    for i, j in enumerate(win_limit_options):
        text = Text(str(j), size="m", fg=[200, 200, 200], bg="black", align="top-center", display=False)
        text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + __text_height + win_limit.text.get_height() + bot_count.text.get_height() + 140
        text.x = text.x + (j - 5)*45
        if cursor.hovered_text(text):
            text = Text(str(j), size="m", fg=[150, 150, 150], bg="black", align="top-center", display=False)
            text.y += title.text.get_height() + back.text.get_height() + player_count.text.get_height() + text.text.get_height() + __text_height + win_limit.text.get_height() + bot_count.text.get_height() + 140
            text.x = text.x + (j - 5)*45
            if mouse.get_pressed()[0]:
                win_limit_selected = j
                TIME.sleep(0.3)
        Game.surface.blit(text.text, (text.x, text.y))
        if j == win_limit_selected:
            draw.rect(Game.surface, (0, 250, 0), (text.x - 4, text.y - 4, text.text.get_width() + 6, text.text.get_height() + 6), 5)

    save = Text("Save Settings", size="m", fg="green", bg="black", align="bottom-center")
    if cursor.hovered_text(save):
        save = Text("Save Settings", size="m", fg=[0, 50, 0], bg="black", align="bottom-center")
        if mouse.get_pressed()[0]:
            open_option_input_prompt = True

    Game.surface.blit(back.text, (back.x, back.y))
    Game.surface.blit(player_count.text, (player_count.x, player_count.y))
    Game.surface.blit(bot_count.text, (bot_count.x, bot_count.y))
    Game.surface.blit(win_limit.text, (win_limit.x, win_limit.y))

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

mixer.music.load(Game.menu_music_path)
mixer.music.set_volume(0.7)
mixer.music.play()

def main():  # sourcery no-metrics
    global start, open_option, cursor, open_quit_option, open_option_input_prompt
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
            for player in mapRenderer.players:
                if isinstance(player, Player):
                    if e.type == KEYDOWN:
                        # UP
                        if e.key == K_w and player.id == 1:
                            player.faceUp = True
                            player.faceDown = False
                            player.idle = False
                            player.frame = 0

                        if e.key == K_t and player.id == 2:
                            player.faceDown = False
                            player.faceUp = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_i and player.id == 3:
                            player.faceDown = False
                            player.faceUp = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_UP and player.id == 4:
                            player.faceDown = False
                            player.idle = False
                            player.faceUp = True
                            player.frame = 0

                        # LEFT
                        if e.key == K_a and player.id == 1:
                            player.faceLeft = True
                            player.faceRight = False
                            player.idle = False
                            player.frame = 0

                        if e.key == K_f and player.id == 2:
                            player.faceRight = False
                            player.faceLeft = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_j and player.id == 3:
                            player.faceRight = False
                            player.faceLeft = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_LEFT and player.id == 4:
                            player.faceRight = False
                            player.idle = False
                            player.faceLeft = True
                            player.frame = 0

                        # DOWN
                        if e.key == K_s and player.id == 1:
                            player.faceUp = False
                            player.faceDown = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_g and player.id == 2:
                            player.faceUp = False
                            player.faceDown = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_k and player.id == 3:
                            player.faceUp = False
                            player.faceDown = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_DOWN and player.id == 4:
                            player.faceUp = False
                            player.idle = False
                            player.faceDown = True
                            player.frame = 0

                        # RIGHT
                        if e.key == K_d and player.id == 1:
                            player.faceLeft = False
                            player.faceRight = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_h and player.id == 2:
                            player.faceLeft = False
                            player.faceRight = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_l and player.id == 3:
                            player.faceLeft = False
                            player.faceRight = True
                            player.idle = False
                            player.frame = 0

                        if e.key == K_RIGHT and player.id == 4:
                            player.faceLeft = False
                            player.idle = False
                            player.faceRight = True
                            player.frame = 0

                        if e.key == K_q and player.id == 1:
                            player.placeBomb()

                        if e.key == K_r and player.id == 2:
                            player.placeBomb()

                        if e.key == K_u and player.id == 3:
                            player.placeBomb()

                        if e.key == K_RSHIFT and player.id == 4:
                            player.placeBomb()
                                

                    if e.type == KEYUP:
                        # UP
                        if e.key == K_w and player.id == 1:
                            player.faceUp = False
                        if e.key == K_t and player.id == 2:
                            player.faceUp = False
                        if e.key == K_i and player.id == 3:
                            player.faceUp = False
                        if e.key == K_UP and player.id == 4:
                            player.faceUp = False

                        # LEFT
                        if e.key == K_a and player.id == 1:
                            player.faceLeft = False
                        if e.key == K_f and player.id == 2:
                            player.faceLeft = False
                        if e.key == K_j and player.id == 3:
                            player.faceLeft = False
                        if e.key == K_LEFT and player.id == 4:
                            player.faceLeft = False

                        # DOWN
                        if e.key == K_s and player.id == 1:
                            player.faceDown = False
                        if e.key == K_g and player.id == 2:
                            player.faceDown = False
                        if e.key == K_k and player.id == 3:
                            player.faceDown = False
                        if e.key == K_DOWN and player.id == 4:
                            player.faceDown = False

                        # RIGHT
                        if e.key == K_d and player.id == 1:
                            player.faceRight = False
                        if e.key == K_h and player.id == 2:
                            player.faceRight = False
                        if e.key == K_l and player.id == 3:
                            player.faceRight = False
                        if e.key == K_RIGHT and player.id == 4:
                            player.faceRight = False

                        # STOPPING ANIMATION
                        if (
                            player.id == 1
                            and not player.faceUp
                            and not player.faceDown
                            and not player.faceLeft
                            and not player.faceRight
                        ):
                            player.idle = True
                        if (
                            player.id == 2
                            and not player.faceUp
                            and not player.faceDown
                            and not player.faceLeft
                            and not player.faceRight
                        ):
                            player.idle = True
                        if (
                            player.id == 3
                            and not player.faceUp
                            and not player.faceDown
                            and not player.faceLeft
                            and not player.faceRight
                        ):
                            player.idle = True
                        if (
                            player.id == 4
                            and not player.faceUp
                            and not player.faceDown
                            and not player.faceLeft
                            and not player.faceRight
                        ):
                            player.idle = True

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

