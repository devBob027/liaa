import pygame, multiprocessing, sys
from liaa import render, io

class Event:
    def __init__(self, t, data):
        self.type = t
        self.data = data

class SaveObject:
    def __init__(self, obj, **data):
        self.data = data
        self.load = obj

class GameObject:
    def __init__(self):

        self.renderObjects = []
        self.id = None
        self.layer = 1
        self.load()

    def save(self):
        pass

    def load(self):
        pass

    def tick(self, events):
        pass

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.display = pygame.display.set_mode(io.getRes())
        self.clock = pygame.time.Clock()
        self.gameObjects = []
        self.eventQueue = []
        self.renderer = render.Render(self.clock, self.display)
        self.runBuiltInEvents = True
        self.renderLayers = 1

    def addObject(self, obj):
        self.gameObjects.append(obj)
        self.gameObjects[len(self.gameObjects) - 1].id = len(self.gameObjects) - 1
        return len(self.gameObjects) - 1

    def tick(self):  
        for e in pygame.event.get():
            self.eventQueue.append(e)

        newEvents = []
        for obj in self.gameObjects:
            i = obj.tick(self.eventQueue)
            if i:
                for e in i:
                    newEvents.append(e)

        if self.runBuiltInEvents:
            self._events()
        self.customEventsTick()
        self.renderer.renderFrame(self.gameObjects, self.renderLayers)
        self.eventQueue = newEvents.copy()
    
    def _events(self):
        for event in self.eventQueue:
            match event.type:
                case pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                case 'offsetCamera':
                    self.renderer.offset = (self.renderer.offset[0] + event.data[0], self.renderer.offset[1] + event.data[1])
                case 'setCameraOffset':
                    # I'm not sure if lists need to be copied, so I'm doing it the long way
                    self.renderer.offset = (event.data[0], event.data[1])
                case 'saveScene':
                    # TODO: add function
                    pass
                case 'loadScene':
                    # TODO: add function
                    pass

    def customEventsTick(self):
        # This is for the developer to determine
        pass

    def saveScene(self):
        scene = []
        for obj in self.gameObjects:
            scene.append(obj.save)
        return scene

    def loadScene(self, scene):
        self.gameObjects = []
        self.renderer.offset = (0, 0)
        for obj in scene:
            i = self.addObject(obj.load())
            self.gameObjects[i].load(obj.data)