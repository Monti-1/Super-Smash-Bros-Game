#  ___________________________________________________________________________
# / Programer: Muntasir Munir        Images                  Date: 2023-01-12 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |        Program that is used to draw images for the characters             |
# |                  and backgrounds in the start menu                        |
# \___________________________________________________________________________/


# ------------
#   Imports.
# ------------
import pygame
import os

class Images ():
    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int, 
        image: str="", 
        sub_image_path: str="", 
    ):
        self.pos = [x, y]
        self.width = width
        self.height = height
        img_path = "IMGS"
        self.sub_image_path = sub_image_path

        self.surface = pygame.Surface ((self.width, self.height))

        main_images_path = os.path.join (
            os.getcwd (),
            img_path, 
            "Menu", 
            sub_image_path
        )
        image_path = os.path.join (main_images_path, image + ".png")
        self.image = pygame.transform.scale (
            pygame.image.load (image_path),
            (self.width, self.height)
        )



    def draw(self, window: pygame.Surface):

        """
        Draws image onto the screen

        Args:
            window: screen that image will be drawn on
        """
        window.blit (
            self.image,
            self.pos
        )

