#  ___________________________________________________________________________
# / Programer: Kyler. V            Platform                  Date: 2023-01-13 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |   This class is used to create a platform that the character stands on.   |
# |                                                                           |
# \___________________________________________________________________________/

import pygame

class Platform ():
    STEP = 1

    def __init__ (self, x: int, y: int, image: pygame.Surface):
        self.pos = [x, y]
        self.image = pygame.transform.scale(
            image,
            (image.get_width () + 240, image.get_height () + 60)
        )
        self.width = self.image.get_width ()
        self.height = self.image.get_height ()


    # /////////////////////
    #   Public Functions.
    # /////////////////////

    def draw (self, win: pygame.Surface) -> None:
        """
        Generate the image onto the screen.

        Args:
            win (pygame.Surface): The pygame window.
        """
        win.blit (
            self.image,
            self.pos
        )
      
    def set_pos (self, pos: "list[int]") -> None:
        """
        Set the position of the platform.

        Args:
            pos (list[int]): Position.
        """
        self.pos = pos
    
    def get_mask (self) -> pygame.mask.Mask:
        """
        Get the mask of the platform.

        Returns:
            pygame.mask.Mask: The mask of the platform.
        """
        return pygame.mask.from_surface (self.image)
  
    def move(self, offset:  "list[int]"):
        """
        Move the platform an amount.

        Args:
            offset (list[int]): The offset in pixels to move it.
        """
        self.pos[0] += self.STEP * offset[0]
        self.pos[1] += self.STEP * offset[1]

    def get_pos (self) -> "list[int]":
        """
        Get the position of the platform.

        Returns:
            list[int]: The position of the platform.
        """
        return self.pos

    def get_width (self) -> int:
        """
        Get the width of the image.

        Returns:
            int: Image width.
        """
        return self.width

