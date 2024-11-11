#  ___________________________________________________________________________
# / Programer: Kyler. V              Text                    Date: 2023-01-13 \                                  |
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |               This class controls text that is displayed.                 |
# |                                                                           |
# \___________________________________________________________________________/


import pygame

class Text ():
    def __init__ (
        self, 
        text: str, 
        pos: "list[int]", 
        text_color: "tuple[int]", 
        font_size:int=18
    ):
        pygame.font.init ()
        self.text = text
        self.pos = pos
        self.text_color = text_color

        self.font = pygame.font.SysFont ("comic sans ms", font_size)
        self._update_image ()


    # /////////////////////////////
    #       Public functions.
    # /////////////////////////////
   
    def set_text_color (self, color: "tuple[int]") -> None:
        """
        Set the text color.

        Args:
            color (tuple[int]): 
                An RGB value for the text to be assigned to.
        """
        self.text_color = color
        self._update_image ()
    
    def draw (self, win: pygame.Surface) -> None:
        """
        Draw the text onto the screen.

        Args:
            win (pygame.Surface): The window on which to draw to.
        """
        win.blit (
            self.image, 
            self.pos
        )
 
    def set_pos (self, pos: "list[int]") -> None:
        """
        Set the position fo the text.

        Args:
            pos (list[int]): (X, Y) coordinates.
        """
        self.pos = pos

    def set_text (self, text: str) -> None:
        """
        Set the text to be something different.

        Args:
            text (str): The text to assign.
        """
        self.text = text
        self._update_image ()

    def get_pos (self) -> "list[int]":
        """
        Get the position of the text.

        Returns:
            list[int]: self.pos
        """
        return self.pos

    def get_height (self) -> int:
        """
        Get the height of the image.

        Returns:
            int: Height.
        """
        return self.image.get_height ()
   
    def get_width (self) -> int:
        """
        Get the width of the text.

        Returns:
            int: Width.
        """
        return self.image.get_width ()


    # //////////////////////////////
    #       Private functions.
    # //////////////////////////////

    def _update_image(self) -> None:
        """
        Update the image variable.
        """
        self.image = self.font.render (self.text, False, self.text_color)



