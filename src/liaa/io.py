import os, sys, json, pygame, pickle
from os.path import join as merge

global cache
cache = {}  

# conf.json check
if not os.path.exists('conf.json'):
    open('conf.json', 'x')    
    defaultConf = '''{
    "resolution": [256, 144],
    "size": 1,
    "path": "gameData",
    "font": null
    "fontSize": 10
}
    '''
    with open('conf.json', 'w') as f:
        f.write(defaultConf)


CONF = json.load(open('conf.json'))

RES = CONF['resolution']
SIZE = CONF['size']
PATH = CONF['path']
FONT_SIZE = CONF['fontSize']

pygame.font.init()
if CONF['font']:
    font = pygame.font.SysFont(CONF['font'], FONT_SIZE*SIZE)
else:
    font = pygame.font.SysFont(pygame.font.get_default_font(), 10*SIZE)

#
# GET ASSETS
#


def getSound(name):
    global cache
    path = merge(PATH, 'resources', 'sounds', f'{name}.mp3')
    if os.path.exists(path):
        if path in cache:
            return cache[path]
        else:
            sound = pygame.mixer.Sound(path)
            cache[path] = sound
            return sound
    else:
        return None

def getRes():
    return (RES[0] * SIZE, RES [1] * SIZE)

def getPicture(name):
    path = merge(PATH, 'resources', 'textures', f'{name}.png')
    if os.path.exists(path):
        return path
    else:
        return merge(PATH, 'resources', 'textures', 'missing.png')

def getPygameSurface(path):
    i = pygame.image.load(path)
    i = pygame.transform.scale(i, (i.get_rect().width*SIZE, i.get_rect().height*SIZE))
    return i

def getTexture(name):
    filePath = merge(PATH, 'resources', 'animations', f'{name}.json')
    if not os.path.exists(filePath):
        # Animation not found
        if os.path.exists(merge(PATH, 'resources', 'textures', f'{name}.png')):
            # It's just a plain texture
            return ((getPygameSurface(getPicture(name)), (0, 0)),)
        else:
            # Dev is stupid and called for a nonexistant texture
            return ((getPygameSurface(getPicture('missing')), (0, 0)), (getPygameSurface(getPicture('error')), (0, 0)))
    

    try:
        with open(filePath, 'r') as f:
            js = json.load(f)
            for i in range(len(js)):
                js[i - 1][0] = getPygameSurface(getPicture(js[i - 1][0]))
            return js

    except:
        # Error animation
        return ((getPygameSurface(getPicture('missing')), (0, 0)), (getPygameSurface(getPicture('error')), (0, 0)))

#
# SAVE AND LOAD GAME
#

def saveScene(name, path):
    path = merge(PATH, 'scenes', f'{path}.bin')
    # Very bad way to do this, but it works.
    try:
        open(path, 'x')
    except:
        pass
    pickle.dump(scene, open(path, 'wb'))

def loadScene(path):
    path = merge(PATH, 'scenes', f'{path}.bin')
    return pickle.load(open(path, 'rb'))