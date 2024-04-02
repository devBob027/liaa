from liaa import io
import pygame, math

class RenderObject:
    def __init__(self, textures, pos = (0, 0), fpf = 1, loop = False):
        self.texture = []
        for anim in textures:
            self.texture.append(anim)
        
        self.pos = pos
        self.fpf = fpf
        self.setAnimation(0)
        self.loop = loop

    def setAnimation(self, animation):
        self.animation = animation
        self.frame = 0

    def render(self, offset):
        self.frame += 1
        f = math.floor(self.frame / self.fpf)
        if f >= len(self.texture[self.animation]):
            if self.loop:
                self.frame = 0
                f = 0
            else:
                f = len(self.texture[self.animation]) - 1
        return (self.texture[self.animation][f][0], ((self.texture[self.animation][f][1][0] + self.pos [0] + offset[0])*io.SIZE, (self.texture[self.animation][f][1][1] + self.pos [1] + offset[1])*io.SIZE))

class Render:
    def __init__(self, clock, display):
        self.clock = clock
        self.display = display
        self.offset = (0, 0)

    # Gets a list of GameObjects and renders them
    def renderFrame(self, objList, layers):
        self.display.fill((0, 0, 0))
        for i in range(layers + 1):
            for obj in objList:
                if obj.layer == i:
                    r = None

                    # If the GameObject has multiple render objects, render them individually
                    if type(obj.renderObjects) == list:
                        for sobj in obj.renderObjects:
                            r = sobj.render(self.offset)
                            self.display.blit(r[0], r[1])
                        r = None
                    
                    # If it doesn't, just render it.
                    else:
                        r = obj.renderObjects.render(self.offset)
                    if r:
                        self.display.blit(r[0], r[1])
        pygame.display.flip()
        self.clock.tick(30)
            