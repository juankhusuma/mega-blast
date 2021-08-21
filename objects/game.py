import json
from pygame import display, init
init()


class Game:
    """The game class is used to share settings across all objects in the game"""

    settingsPath = "data/settings.json"
    gameConfPath = "data/game.options.json"
    mapPath = "data/map.json"
    with open(settingsPath, "r") as __f:
        settings = json.load(__f)
    with open(gameConfPath, "r") as __g:
        gameConf = json.load(__g)
    with open(mapPath, "r") as __h:
        map = json.load(__h)
    resolution = settings["game.resolution"]
    if resolution == [0, 0]:
        screenInfo = display.Info()
        resolution = [screenInfo.current_w, screenInfo.current_h]
    surface = display.set_mode(resolution)

    def __init__(self):
        Game.__setJSON()

    @classmethod
    def __setJSON(klass):
        with open(klass.settingsPath, "r") as f:
            klass.settings = json.load(f)
        with open(klass.gameConfPath, "r") as g:
            klass.gameConf = json.load(g)
        with open(klass.mapPath, "r") as h:
            klass.map = json.load(h)

    @classmethod
    def modifyGameData(klass, data_name, **kwargs):
        def __setData(_data, data):
            for key in data:
                _data[key] = data[key]
            return _data
        if data_name == "settings":
            path = klass.settingsPath
            _data = klass.settings
        elif data_name == "game-conf":
            path = klass.gameConfPath
            _data = klass.gameConf
        elif data_name == "map":
            path = klass.mapPath
            _data = klass.map
        with open(path, "w") as f:
            json.dump(__setData(_data, kwargs), f)
        klass.__setJSON()
