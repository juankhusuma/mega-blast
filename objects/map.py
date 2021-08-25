from objects.game import Game
from objects.entity import Box, Wall
import random
import sys


class MapFactory(Game):
    def __init__(self):
        super().__init__()
        size = self.gameConf["game.mapSize"]
        self.width, self.height = size, size
        self.EMPTY = 'e'
        self.WALL = 'w'
        self.AGENT = 'p'
        self.GOAL = 'x'
        self.BOX = 'b'
        self.maze = {}
        self.spaceCells = set()
        self.connected = set()
        self.walls = set()
        Game.modifyGameData("map", map=self.__generateMaze())

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

    def __populate(self):
        TL = (1, 1)
        BR = (self.height-2, self.width-2)
        if self.height % 2 == 0:
            BR = (BR[0]-1, BR[1])
        if self.width % 2 == 0:
            BR = (BR[0], BR[1]-1)
        self.maze[TL] = self.AGENT
        self.maze[BR] = self.GOAL

    def __generateMaze(self):
        print("Generating Maze...")
        self.width += 2
        self.height += 2
        self.__initialize()
        self.__borderFill()
        self.__primAlg()
        # self.__populate()
        _map = [''.join(self.maze[(i, j)] for j in range(self.width))
                for i in range(self.height)]
        if len(_map) % 5 != 0:
            _map.pop()
            for i, j in enumerate(_map):
                _map[i] = j[:-1]
        return _map


class MapRenderer(Game):
    def __init__(self):
        print("Map renderer initialized...")
        super().__init__()
        self.map_item = []
        self.__start()

    def __start(self):
        for i, column in enumerate(Game.map["map"]):
            for j, item in enumerate(column):
                if item == "b":
                    self.map_item.append(Box(i, j))
                elif item == "w":
                    self.map_item.append(Wall(i, j))
                # print(self.map_item[-1])

    def render(self):
        for item in self.map_item:
            if isinstance(item, Wall):
                Game.surface.blit(Wall.sprite, (item.x, item.y))
            elif isinstance(item, Box):
                Game.surface.blit(Box.sprite, (item.x, item.y))
