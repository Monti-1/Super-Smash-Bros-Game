#  ___________________________________________________________________________
# / Programer: Muntasir Munir       Button                   Date: 2023-01-10 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |   This class is used to make a Button menu for choosing the characters    |
# |                     and backgrounds for the players                       |
# \___________________________________________________________________________/



# ------------
#   Imports.
# ------------
import sys
import pygame
from Images import *
import os

# ------------------------------
#   Configuration for testing.
# ------------------------------
pygame.init ()
fps = 60
fpsClock = pygame.time.Clock ()
width, height = 800, 800
screen = pygame.display.set_mode ((width, height))

font = pygame.font.SysFont ('Times New Roman', 30, True)

objects = []

class Button ():

    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int, 
        buttonText: str='Button', 
        onclickFunction=None,
        index: int=0
    ):
        """
        Initialize the Button class.

        Args:
            x (int): X pos.
            y (int): Y pos.
            width (int): Width of button.
            height (int): Height of button.
            buttonText (str, optional): Button text. Defaults to 'Button'.
            onclickFunction (_type_, optional): 
                Function with an int argument. Defaults to None.
            index (int, optional): 
                Index of player. Defaults to 0.
        """
        self.pos = [x, y]
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.buttonText = buttonText
        self.index = index
        

        self.fillColors = {
            'normal': '#ff0000',
            'hover': '#d53737',
            'pressed': '#700000',
        }

        self.buttonSurface = pygame.Surface ((self.width, self.height))
        self.buttonRect = pygame.Rect (self.pos[0], self.pos[1], self.width, self.height)

        self.buttonSurf = font.render (self.buttonText, True, (20, 20, 20))
        self.alreadyPressed = False     

        objects.append (self)

    def update_color (self) -> None:
        """
        Fills button with color for hovering and clicking.
        Also decides if the button has been pressed or not.
        """

        mousePos = pygame.mouse.get_pos ()

        if (self.buttonRect.collidepoint (mousePos)):
            self.buttonSurface.fill (self.fillColors['hover'])

            if (pygame.mouse.get_pressed (num_buttons = 3)[0]):
                self.buttonSurface.fill (self.fillColors['pressed'])

        else:
            self.buttonSurface.fill (self.fillColors['normal'])
        
    def draw (self, window) -> None:
        """
        Draws the button onto the screen

        Args:
            window: screen that the button will be drawn on
        """

        self.buttonSurface.blit (self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect ().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect ().height / 2
        ])
        window.blit (self.buttonSurface, self.buttonRect)

    def clicked (self) -> None or list:
        """
        If the button is clicked run the function.

        Returns:
            None or list: Data to be returned.
        """
        mousePos = pygame.mouse.get_pos ()
        if (self.onclickFunction != None):
            if (self.buttonRect.collidepoint (mousePos)):
                return self.onclickFunction (self.index)
        return None



if (__name__ == "__main__"):

    counter = 0
    widths = [50, 300, 550]
    plyr_names = ["Link", "Pikachu", "Captain Falcon"]
    bg_names = ["Haunted forest", "Peachy meadow", "Interstellar"]

    def test (index):
        global counter
        if (counter < 2):
            plyr (index)

    def bg (index):
        global objects
        print (plyr_names[index])
        objects = [
            Button (
                widths[num] - 10,
                650, 
                220, 
                100, 
                bg_names[num], 
                test,
                num
            ) for num in range (3)  
        ]
        objects += [
            Images (
                widths[num],
                100, 
                200, 
                500, 
                bg_names[num],
                "Bg" 
            ) for num in range (3)
        ]       

    def plyr (index):
        global counter
        global objects
        objects = [
            Button (
                widths[num],
                100, 
                200, 
                100, 
                plyr_names[num], 
                bg,
                num
            ) for num in range (3)
        ]
        
        objects += [
            Images (
                widths[num],
                250, 
                200, 
                400, 
                plyr_names[num],
                "Char" 
            ) for num in range (3)
        ]
        counter += 1

    def Buttoning ():
        global objects
        objects = [Button (200, 600, 300, 100, 'Button', plyr)]
        

    # Game loop.
    Buttoning()

    while True:
        screen.fill ((255, 255, 255))
        for event in pygame.event.get ():
            if (event.type == pygame.QUIT):
                pygame.quit ()
                sys.exit ()

        for object in objects:
            if (isinstance (object, Button)):
                object.fill ()
            object.draw (screen)
        
        pygame.display.flip ()
        fpsClock.tick (fps)