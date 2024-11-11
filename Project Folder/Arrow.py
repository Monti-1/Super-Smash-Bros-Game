#  ___________________________________________________________________________
# / Programmer: Muntasir. M          Arrow                   Date: 2022-12-22 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |                  This class is used to control an Arrow.                  |
# |                                                                           |
# \___________________________________________________________________________/

from random import randint
import pygame

class Arrow():
    ARROW_SPEED = 6
    RANGE = 100

    def __init__(
        self,
        pos: "list[int]",
        damage: int,
        image: pygame.Surface,
        direction: bool,
        identifier: int,
        attack_number: int
    ):
        # ---------------------
        #   Unseen variables.
        # ---------------------
        self.direction = direction
        self.damage = damage
        self.image = image
        self.identifier = identifier
        self.num = attack_number
        self.attack_identifier = randint (0, 100000000000000000000000000000000)

        # -------------
        #   Movement.
        # -------------
        self.character_pos = [pos[0] + 1, pos[1] + 1]
        self.pos = pos
        self.height = self.image.get_height ()
        self.pos[1] += self.height // 3

        # -------------------------------
        #   Set the range of the arrow.
        # -------------------------------
        self.min_value = self.character_pos[0] - self.RANGE
        self.max_value = self.character_pos[0] + self.RANGE
        
        # -----------------------------------
        #   Set the direction of the arrow.
        # -----------------------------------
        if (self.direction):
            self.pos[0] += self.image.get_width () // 4
        
        elif (not self.direction):
            self.pos[0] -= self.image.get_width () // 4
            self.image = pygame.transform.flip (image, True, False)
        


    # /////////////////////
    #   Public functions.
    # /////////////////////


    def draw (self, window: pygame.surface.Surface) -> bool:
        """
        Draw the arrow on the screen.

        Args:
            window (pygame.surface.Surface): Main window to draw arrow on.

        Returns:
            bool: Delete this object or not.
        """

        if (self.direction):
            value = self.ARROW_SPEED

        else:
            value = -self.ARROW_SPEED

        if (self.min_value <= self.pos[0] + value <= self.max_value):
            self.pos[0] += value
            window.blit (
                self.image,
                self.pos
            )
            return True

        return False

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
        return pygame.mask.from_surface (self.image)
    
    def get_pos (self) -> "list[int]":
        """
        Get the position of the arrow.

        Returns:
            list[int]: The x, y pos of the arrow.
        """
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
        return self.image.get_width ()



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