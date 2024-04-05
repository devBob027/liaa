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

# Cache operations

def cacheObjects(name):
    newCache = {}
    for i in name:
        newCache[i] = getAsset(i)
    global cache
    cache = newCache.copy()

# Asset stuff

def getAsset(name):
    global cache
    if name in cache:
        return cache[name]
    else:
        match name.split('.')[1][:4]:
            case 'mp3':
                return getSound(name.split('.')[0])
            case 'png':
                return getPicture(name.split('.')[0])
            case 'png/':
                return getPicture(name)

def getSound(name):
    global cache
    if f'{name}.mp3' in cache:
        return cache[f'{name}.mp3']
    path = merge(PATH, 'resources', 'sounds', f'{name}.mp3')
    if os.path.exists(path):
        sound = pygame.mixer.Sound(path)
        cache[f'{name}.mp3'] = sound
        return sound
    else:
        return None

def getRes():
    return (RES[0] * SIZE, RES [1] * SIZE)

def getPicture(name):
    path = ''
    if '.' in name:
        # Sprite sheet logic goes here
        # TODO: Add sprite sheet logic
        pass
    else:
        path = merge(PATH, 'resources', 'textures', f'{name}.png')
    global cache
    if path in cache:
        return cache[path]
    elif not os.path.exists(path):
        path = merge(PATH, 'resources', 'textures', 'missing.png')
    i = pygame.image.load(path)
    cache[path] = i
    return i

def _getPygameSurface(path):
    i = getPicture(path)
    i = pygame.transform.scale(i, (i.get_rect().width*SIZE, i.get_rect().height*SIZE))
    return i

def getTexture(name):
    filePath = merge(PATH, 'resources', 'animations', f'{name}.json')
    if not os.path.exists(filePath):
        # Animation not found
        if os.path.exists(merge(PATH, 'resources', 'textures', f'{name}.png')):
            # It's just a plain texture
            return ((_getPygameSurface(name), (0, 0)),)
        else:
            # Dev is stupid and called for a nonexistant texture
            return ((_getPygameSurface('missing'), (0, 0)), (_getPygameSurface('error'), (0, 0)))
    

    try:
        with open(filePath, 'r') as f:
            js = json.load(f)
            for i in range(len(js)):
                js[i - 1][0] = getPygameSurface(getPicture(js[i - 1][0]))
            return js

    except:
        # Error animation
        return ((_getPygameSurface('missing'), (0, 0)), (_getPygameSurface('error'), (0, 0)))

#
# Save and load
#

def saveScene(name, path, saveCache = True):
    path = merge(PATH, 'scenes', f'{path}.bin')
    # Very bad way to do this, but it works.
    try:
        open(path, 'x')
    except:
        pass
    pickle.dump([saveCache*list(cache.keys()), scene], open(path, 'wb'))

def loadScene(path):
    path = merge(PATH, 'scenes', f'{path}.bin')
    c, scene = pickle.load(open(path, 'rb'))
    cacheObjects(c)
    return scene