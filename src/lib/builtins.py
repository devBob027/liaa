from lib import game, io, render
import pygame, os, sys, math, textwrap

'''
    TODO: add the following presets:
        [X] Textbox
        [ ] SoundPlayer
        [ ] PlayerSizeview
        [ ] GridMap
        [ ] BasicMenu
        [ ] PlayerTopdown
'''

class Textbox(game.GameObject):

    def getTextSize(self):
        x = 1
        while True:
            s = io.font.render('A'*x, False, self.hColor)
            s = s.get_rect()
            if s.w > self.textArea[0]:
                return([x - 2, self.textArea[1]//(s.h)])
            x += 1

    def setText(self, text):
        self.text = textwrap.wrap(text, self.tSize[0])
        self._setTextAnim()

    def _setTextAnim(self, skip = False):

        self.renderObjects = []
        s = pygame.Surface((self.size[0] * io.SIZE, self.size[1] * io.SIZE))
        s.fill(self.hColor)
        pygame.draw.rect(s,self.bColor,pygame.Rect(io.SIZE,io.SIZE,(self.size[0] - 2) * io.SIZE,(self.size[1] - 2) * io.SIZE))
        self.renderObjects.append(render.RenderObject([[[s, self.pos]]]))

        
        textSpeed = math.ceil(self.textSpeed)
        dY = 0
        dT = 0
        line = 0
        for tChunk in self.text:
            if line > self.tSize[1]:
                break
            elif skip:
                self.renderObjects.append(render.RenderObject([[[io.font.render(tChunk, False, self.hColor),[self.pos[0] + 2, self.pos[1] + 2 + dY]]]]))
                dT = 0
            else:
                anim = []
                # Draw nothing for dT frames
                for i in range(dT):
                    anim.append([pygame.Surface((0, 0)),[0, 0]])
                # Draw text and increment dT
                for i in range(0, len(tChunk), textSpeed):
                    anim.append([io.font.render(tChunk[:int(i)], False, self.hColor),[self.pos[0] + 2, self.pos[1] + 2 + dY]])
                    dT += 1

                anim.append([io.font.render(tChunk, False, self.hColor),[self.pos[0] + 2, self.pos[1] + 2 + dY]])
            
                self.renderObjects.append(render.RenderObject([anim],fpf=math.ceil(1/self.textSpeed)))
            dY += io.FONT_SIZE
            line += 1
        self.framesLeft = dT

    def load(self, data = {'text': '', 'textSpeed': 1, 'pos': (1, 103), 'hColor': (255, 255, 255), 'bColor': (0, 0, 0), 'size': (254, 40)}):
        
        self.textSpeed = data['textSpeed']
        self.animate = True
        self.pos = data['pos']
        self.hColor = data['hColor']
        self.bColor = data['bColor']
        self.size = data['size']

        self.textArea = [(self.size[0] - 2) * io.SIZE, (self.size[1] - 2) * io.SIZE]

        self.tSize = self.getTextSize()
        self.text = textwrap.wrap(data['text'], self.tSize[0])
        self._setTextAnim()

    def tick(self, events):

        if self.framesLeft > 0:
            self.framesLeft -= 1
            if self.framesLeft == 0:
                return [game.Event('TextboxTextComplete', [self.id])]
        
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key in [pygame.K_z, pygame.K_x]:
                        if self.framesLeft:
                            self._setTextAnim(True)
                            return [game.Event('TextboxTextComplete', [self.id]), game.Event('TextboxTextSkipped', [self.id])]
