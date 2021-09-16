from objects.text import Text
from pygame import image, draw
from objects.game import Game
from objects.entity import BombActive, BombItem, Box, Empty, Mimic, Wall
from objects.player import Bot, Player
import random
import sys


class MapFactory(Game):
    test = 0
    def __init__(self):
        MapFactory.test += 1
        self.test = MapFactory.test
        super().__init__()
        size = self.settings["game.mapSize"]
        self.width, self.height = size, size
        self.EMPTY = 'e'
        self.WALL = 'w'
        self.BOX = 'b'
        self.maze = {}
        self.spaceCells = set()
        self.connected = set()
        self.walls = set()
        self._map = self.__generateMaze()
        print("Generating new map")
        Game.modifyGameData("map", {"map": self._map})

    @staticmethod
    def adjacent(cell):
        i, j = cell
        for (y, x) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            yield (i+y, j+x), (i+2*y, j+2*x)

    def __initialize(self):
        for i in range(self.height):
            for j in range(self.width):
                self.maze[(i, j)] = self.EMPTY if (
                    (i % 2 == 1) and (j % 2 == 1)
                ) else self.WALL

    def __borderFill(self):
        for i in range(self.height):
            self.maze[(i, 0)] = self.WALL
            self.maze[(i, self.width-1)] = self.WALL
        for j in range(self.width):
            self.maze[(0, j)] = self.WALL
            self.maze[(self.height-1, j)] = self.WALL
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[(i, j)] == self.EMPTY:
                    self.spaceCells.add((i, j))
                if self.maze[(i, j)] == self.WALL:
                    self.walls.add((i, j))

    def __primAlg(self, verbose=True):
        originalSize = len(self.spaceCells)
        self.connected.add((1, 1))
        while len(self.connected) < len(self.spaceCells):
            doA, doB = None, None
            cns = list(self.connected)
            random.shuffle(cns)
            for (i, j) in cns:
                if doA is not None:
                    break
                for A, B in self.adjacent((i, j)):
                    if A not in self.walls:
                        continue
                    if (B not in self.spaceCells) or (B in self.connected):
                        continue
                    doA, doB = A, B
                    break
            A, B = doA, doB
            self.maze[A] = self.BOX if random.randrange(
                1, 5) == 4 else self.EMPTY
            self.maze[B] = self.BOX if random.randrange(
                1, 5) == 4 else self.EMPTY
            self.walls.remove(A)
            self.spaceCells.add(A)
            self.connected.add(A)
            self.connected.add(B)
            if verbose:
                cs, ss = len(self.connected), len(self.spaceCells)
                cs += (originalSize - ss)
                ss += (originalSize - ss)
                if cs % 10 == 1:
                    print('%s/%s cells self.connected ...' %
                          (cs, ss), file=sys.stderr)

    def __generateMaze(self):
        print("Generating Maze...")
        self.width += 2
        self.height += 2
        self.__initialize()
        self.__borderFill()
        self.__primAlg(False)
        _map = [''.join(self.maze[(i, j)] for j in range(self.width))
                for i in range(self.height)]
        for i, row in enumerate(_map):
            _map[i] = list(row)
        for c, a in enumerate(_map):
            for d, b in enumerate(a):
                if c > 0 and c < len(_map) - 1 and d > 0 and d < len(a) - 1:
                    if random.randrange(1, 40) == 4 and b == "w":
                        _map[c][d] = "m"
                    if random.randrange(1, 5) == 3 and b == "w":
                        _map[c][d] = "e"

        return _map


class MapRenderer(Game):
    bomb = image.load("assets/images/regular_bomb.png")
    def __init__(self):
        print("Map renderer initialized...")
        super().__init__()
        self.start()

    def start(self):
        Game.map_item = []
        Game.players = []
        Game.bots = []
        player_count = Game.gameConf["game.player.count"]
        bot_count = Game.gameConf["game.bot.count"]
        space = 10
        for i, column in enumerate(Game.map["map"]):
            for j, item in enumerate(column):
                if item == "b":
                    Game.map_item.append(Box(i, j, Game.x_offset, Game.y_offset))
                elif item == "w":
                    Game.map_item.append(Wall(i, j, Game.x_offset, Game.y_offset))
                elif item == "m":
                    Game.map_item.append(Mimic(i, j, Game.x_offset, Game.y_offset))
                elif item == "e":
                    Game.map_item.append(Empty(i, j, Game.x_offset, Game.y_offset))
                    if space > 0:
                        space -= 1
                    else:
                        space = 50
                        if player_count > 0:
                            Game.players.append(Player((i*Game.settings["game.tileSize"] + self.x_offset), ((j*Game.settings["game.tileSize"]) + self.y_offset), 5, player_count))
                            player_count -= 1
                            continue
                        if bot_count > 0 and player_count == 0:
                            Game.bots.append(Bot(i*Game.settings["game.tileSize"] + self.x_offset, ((j*Game.settings["game.tileSize"]) + self.y_offset), 5, bot_count))
                            bot_count -= 1

    @staticmethod
    def render():
        for item in Game.map_item:
            if isinstance(item, Wall):
                Game.surface.blit(Wall.sprite, (item.x, item.y))
            elif isinstance(item, Box):
                Game.surface.blit(Box.sprite, (item.x, item.y))
            elif isinstance(item, Mimic):
                # for player in Game.players:
                #     if item.withinVicinity((player.x, player.y)):
                #         Mimic.sprite = Mimic.sprite_aggrovated
                #     else:
                #         Mimic.sprite = Mimic.sprite_idle
                Game.surface.blit(item.sprite, (item.x, item.y))

        for bomb in Game.bomb_items:
            if isinstance(bomb, BombItem):
                Game.surface.blit(BombItem.sprite, (bomb.x, bomb.y))
            elif isinstance(bomb, BombActive):
                bomb.update()

        for player in Game.players:
            for entity in Game.map_item:
                if isinstance(entity, Mimic):
                    if entity.withinVicinity((player.x, player.y)):
                        entity.sprite = Mimic.sprite_aggrovated
                    else:
                        entity.sprite = Mimic.sprite_idle
            player.animate()
            player.move()
            draw.rect(Game.surface, "green", player.Rect, 1)

        for bot in Game.bots:
            bot.animate()
            bot.move()
            draw.rect(Game.surface, "red", bot.Rect, 1)



