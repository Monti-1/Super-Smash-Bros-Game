#  ___________________________________________________________________________
# / Programmer: Kyler. v           Lightning                 Date: 2022-12-22 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |              This class is used to control a Lightning strike.            |
# |                                                                           |
# | Functions:                                                                |
# |     __init__:                                                             |
# |         - Initializes all private variables and images.                   |
# |                                                                           |
# |     draw:                                                                 |
# |         - Used to draw the lightning.                                     |
# |                                                                           |
# |     get_attacking:                                                        |
# |         - Get the attacking value. This is always 1.                      |
# |                                                                           |
# |     get_attack_damage:                                                    |
# |         - Get the attack damage that will be dealt if a collision is      |
# |           detected.                                                       |
# |                                                                           |
# |     check_collide:                                                        |
# |         - Check if the lightning collides with any object.                |
# |                                                                           |
# |     get_mask:                                                             |
# |         - Get the mask of the lightning image.                            |
# |                                                                           |
# |     get_pos:                                                              |
# |         - Get the position of the lightning.                              |
# |                                                                           |
# |     _offset:                                                              |
# |         - Get the offset from the lightning to another object.            |
# |                                                                           |
# \___________________________________________________________________________/

from random import randint
import pygame

class Lightning ():
    DISPLAY_TIME = 4

    def __init__(
        self,
        x: int,
        y: int,
        damage: int,
        images: "list[pygame.surface.Surface]",
        width_of_calling_class: int,
        height_of_calling_class: int,
        identifier: int,
        attack_number: int
    ):
        self.identifier = identifier
        self.damage = damage
        self.num = attack_number
        self.images = images
        self.max_index = len (self.images) * self.DISPLAY_TIME
        self.index = 0
        self.player_pos = (x, y)
        self.width_and_height = [
            width_of_calling_class,
            height_of_calling_class
        ]
        self.pos = [x, y]
        self.attack_identifier = randint (0, 100000000000000000000000000000000)



    # /////////////////////
    #   Public functions.
    # /////////////////////


    def draw (self, window: pygame.surface.Surface) -> bool:
        """
        Draw the lightning on the screen.

        Args:
            window (pygame.surface.Surface): Main window to draw lightning on.

        Returns:
            bool: Delete this object or not.
        """
        self.max_index = len (self.images) * self.DISPLAY_TIME

        if (self.index + 1 >= self.max_index):
            self.index = 0
            return False

        index = self.index // self.DISPLAY_TIME
        image = self.images[index]

        width = image.get_width ()
        height = image.get_height ()

        new_width = self.width_and_height[0]
        new_width = new_width // 2
        new_width -= width // 2

        new_x = self.player_pos[0]
        new_x += new_width // 2

        new_y = self.player_pos[1]
        new_y += self.width_and_height[1] - 5
        new_y -= height

        self.pos = [new_x, new_y]
        self.index += 1
        window.blit (
            image,
            [new_x, new_y]
        )

        return True

    def get_attacking (self) -> int:
        """
        Get the attack number

        Returns:
            int: Return the attack number
        """
        return 1

    def get_attack_damage (self) -> int:
        """
        Get the attack damages.

        Returns:
            list[int]:
                Index 0 is the damage this attack does
                index 1 is 0 cause we are just giving
                one attack.
        """
        return self.damage

    def check_collide (self, object) -> bool:
        """
        Checks to see if there is collision between
        this sprite and object's sprite

        Args:
            object (SubClassOf Character): A character sub class.

        Returns:
            bool: If this character and object overlap.
        """
        mask_1 = self.get_mask ()
        mask_2 = object.get_mask ()
        if (mask_1.overlap (mask_2, self._offset (object))):
            return True

        else:
            return False

    def get_mask (self) -> pygame.mask.Mask:
        """
        Gets the mask of the current image on the screen.

        Returns:
            pygame.mask.Mask or None:
                Returns the mask if an image is on the screen.
        """
        return pygame.mask.from_surface (
            self.images[self.index // self.DISPLAY_TIME]
        )

    def get_pos (self) -> "list[int]":
        return self.pos

    def get_attack_identifier (self) -> int:
        """
        Get the attack identifier.

        Returns:
            int: Identifier.
        """
        return self.attack_identifier

    def get_identifier (self) -> int:
        """
        Get the identifier.

        Returns:
            int: Identifier.
        """
        return self.identifier

    def get_width (self) -> int:
        """
        Get the width

        Returns:
            int: Width.
        """
        return self.images



    # //////////////////////
    #   Private functions.
    # //////////////////////


    def _offset (self, object) -> "list[int]":
        """
        Return the offset from this character to the other.

        Args:
            object (Character SubClass):
                A subclass of the character class.

        Returns:
            list[int]:
                Returns a list with the difference in
                x position and y position in a list.
        """
        pos = object.get_pos ()
        return [int (self.pos[0] - pos[0]), int (self.pos[1] - pos[1])]
