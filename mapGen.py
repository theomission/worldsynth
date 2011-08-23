#!/usr/bin/env python

import random
import pygame.display
from numpy import *
from pygame.locals import *
from library.popup_menu import PopupMenu
from library.midpointDisplacement import MDA
from library.sphere import Planet


class mapGen():
    """Our game object! This is a fairly simple object that handles the
    initialization of pygame and sets up our game to run."""
    
    def __init__(self, width = 512, height = 512):    
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools
        that we will need for more complicated tutorials.""" 
        pygame.init()

        # create our window
        self.height = width
        self.width = height
        self.size = (self.width, self.height)
        self.window = pygame.display.set_mode(self.size)

        # world data
        self.heightmap = empty((self.width,self.height)) 

        # clock for ticking
        self.clock = pygame.time.Clock()

        # set the window title
        pygame.display.set_caption("World Generator - Setup")

        # tell pygame to only pay attention to certain events
        # we want to know if the user hits the X on the window, and we
        # want keys so we can close the window with the esc key
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])
                     
        # make background and blit the background onto the window
        self.background = pygame.Surface(self.window.get_size(), depth=32)
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0,0))
        # update the display so the background is on there
        pygame.display.update()

        # create menues
        self.menu = (
            'Menu',
            (
                'Add',
                'Midpoint Displacment',
                'Spherical Algorithm',
            ),
            (
                'Size',
                'Small',
                'Medium',
                'Large',
            ),
            'Save',
            'Reset',      
            'Quit',
        )    
        

    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""
 
        print 'Starting Event Loop'
 
        running = True
        # run until something tells us to stop
        while running:
 
            # tick pygame clock
            # you can limit the fps by passing the desired frames per seccond to tick()
            self.clock.tick(60)
 
            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()
 
            # update the title bar with our frames per second
            pygame.display.set_caption('World Generator - %d fps' % self.clock.get_fps())
 
            # blit the dirty areas of the screen
            pygame.display.update()
            #pygame.display.flip()

        print 'Closing '


    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""
 
        # poll for pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
 
            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False

            elif event.type == MOUSEBUTTONUP:
                print 'Show menu'
                PopupMenu(self.menu)                               
            
            elif event.type == USEREVENT:
                if event.code == 'MENU':
                    self.handleMenu(event)  
                    
        return True

    def handleMenu(self,e):
        print 'Menu event: %s.%d: %s' % (e.name,e.item_id,e.text)
        if e.name == 'Menu':
            if e.text == 'Quit':
                quit()
            elif e.text == 'Reset':
                self.__init__()
                
        elif e.name == 'Add...':
            if e.text == 'Midpoint Displacment':
                self.mda()
            elif e.text == 'Spherical Algorithm':
                self.sphere()
                
        elif e.name == 'Size...':
            if e.text == 'Small':
                self.__init__(width=256,height=256)
            elif e.text == 'Medium':
                self.__init__(width=512,height=512)
            elif e.text == 'Large':
                self.__init__(width=1024,height=1024)
            
        self.window.blit(self.background, (0,0)) # blit to screen our background    
        pygame.display.update() # update our screen after event


    def mda(self): # our midpoint displacement algorithm
        size = self.width + self.height
        roughness = 8
        c1 = random.random()
        c2 = random.random()
        c3 = random.random()
        c4 = random.random()
        
        heightmap = empty((self.width,self.height))         
        mda = MDA(size, roughness)
        mda.divideRect(heightmap, 0, 0, self.width, self.height, c1, c2, c3, c4)
        heightmap *= 255
        heightmap = heightmap.astype('int')
        self.heightmap = heightmap
        
        background = []
        for x in heightmap:
            for y in x:
                hex = "0x%02x%02x%02x" % (y, y, y)
                background.append(int(hex,0))
        background = array(background).reshape(self.width,self.height)
        
        pygame.surfarray.blit_array(self.background, background)
        
        del mda, heightmap, background
        
    def sphere(self): # our spherical planet algorithm
        sphere = Planet(self.width)
        world = sphere.generatePlanet(sphere.createSphere(), 50)
        self.background = sphere.sphereToPicture(world)
        self.heightmap = array(world.getdata(),
                        uint8).reshape(world.size[1], 
                        world.size[0])
        del world,sphere
            


class Button(pygame.sprite.Sprite):
    """An extremely simple button sprite."""
    def __init__(self, xy, text):
        pygame.sprite.Sprite.__init__(self)
        self.xy = xy
        self.font = pygame.font.Font(None, 25)  # load the default font, size 25
        self.color = (0, 0, 0)         # our font color in rgb
        self.text = text
        self.generateImage() # generate the image
 
    def generateImage(self):
        # draw text with a solid background - about as simple as we can get
        self.image = self.font.render(self.text, True, self.color, (200,200,200))
        self.rect = self.image.get_rect()
        self.rect.center = self.xy

class TextSprite(pygame.sprite.Sprite):
    """An extremely simple text sprite."""
 
    def __init__(self, xy, text=''):
        pygame.sprite.Sprite.__init__(self)
        self.xy = xy    # save xy -- will center our rect on it when we change the text
        self.font = pygame.font.Font(None, 25)  # load the default font, size 25
        self.color = (255, 165, 0)         # our font color in rgb
        self.text = text
        self.generateImage() # generate the image
 
    def setText(self, text):
        self.text = text
        self.generateImage()
 
    def generateImage(self):
        """Updates the text. Renders a new image and re-centers at the initial coordinates."""
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.xy

# runs the program
if __name__ == '__main__':
    world = mapGen()
    world.run()
