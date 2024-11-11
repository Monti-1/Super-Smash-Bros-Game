#  ___________________________________________________________________________
# / Programmer: Muntasir. M          Link                    Date: 2022-12-22 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |                    This class is used to control Link.                    |
# |                                                                           |
# | Functions:                                                                |
# |     __init__:                                                             |
# |         - Initializes all private variables and images.                   |
# |                                                                           |
# |     attack_1:                                                             |
# |         - Used to initiate attack 1.                                      |
# |                                                                           |
# |     attack_2:                                                             |
# |         - Used to initiate attack 2.                                      |
# |                                                                           |
# \___________________________________________________________________________/


from Character import Character
from Arrow import Arrow
import pygame
import os

class Link (Character):
    def __init__(self, images_path: str, pos: "list[int]", player_num: int):
        """
        Initialize Pikachu.

        Args:
            images_path (str): Path to all images
        """
        character_images_path = os.path.join (images_path, "Link")

        # ------------------------
        #   Attacking variables.
        # ------------------------

        self.attack_counter = 0
        self.attack_1_damage = 10
        self.attack_2_damage = 30

        # ------------------------------------
        #   Get the arrow for the Link class
        # ------------------------------------
        arrow_path = os.path.join (character_images_path, "arrow_link.png")
        self.arrow_image = pygame.image.load (arrow_path)

        # ---------------------------------------------
        #   Run the initializer for the parent class.
        # ---------------------------------------------
        super ().__init__(
            character_images_path,
            [self.attack_1_damage, self.attack_2_damage],
            [self.attack_1, self.attack_2],
            [[0, 0], [0, 0]],
            position=pos,
            knockback=[[4, .3], [3, .2]],
            name="Link",
            player=player_num
        )
        self.attacks = [self.attack_1, self.attack_2]
        self.DISPLAY_TIME -= 1



    # /////////////////////
    #   Public functions.
    # /////////////////////


    def attack_1 (self) -> None:
        self.attacking = 1

    def attack_2 (self) -> Arrow:
        self.attacking = 2
        return Arrow (
            self.pos.copy (),
            self.attack_2_damage,
            self.arrow_image,
            self.facing_right,
            self.identifier,
            self.attacking
        )
    
