#  ___________________________________________________________________________
# / Programmer: Kyler. V            Pikachu                  Date: 2023-01-13 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |                    This class is used to control Pikachu.                 |
# |                                                                           |
# \___________________________________________________________________________/

from Character import Character
from Lightning import Lightning
import pygame
import os

class Pikachu (Character):

    def __init__(self, images_path: str, pos: "list[int]", text_pos: int):
        """
        Initialize Pikachu.

        Args:
            images_path (str): Path to all images
        """
        character_images_path = os.path.join (images_path, "Pikachu")

        # ------------------------
        #   Attacking variables.
        # ------------------------
        self.attack_counter = 0
        self.attack_1_damage = 10
        self.attack_2_damage = 30

        # -------------------------------------------
        #   Get the lightning for pikachu's attacks
        # -------------------------------------------
        lightning_path = os.path.join (character_images_path, "lightning")
        self.lighting = [
            pygame.image.load (
                os.path.join (
                    lightning_path,
                    "lightning_" + "0" + str (x) + ".png"
                )
            ) for x in range (1, 6)
        ]

        # ---------------------------------------------
        #   Run the initializer for the parent class.
        # ---------------------------------------------
        super ().__init__ (
            character_images_path,
            [self.attack_1_damage, self.attack_2_damage],
            [self.attack_1, self.attack_2],
            [[5, 0], [0, 0]],
            position=pos,
            knockback=[[4, .4], [6, .6]],
            name="Pikachu",
            player=text_pos
        )
        

    # /////////////////////
    #   Public functions.
    # /////////////////////

    def attack_1 (self) -> None:
        """
        Activate attack 1.
        """
        self.attacking = 1

    def attack_2 (self) -> Lightning:
        """
        Activate attack 2.

        Returns:
            Lightning: The lighting strike.
        """
        self.attacking = 2
        return Lightning (
            self.pos[0],
            self.pos[1],
            self.attack_2_damage,
            self.lighting,
            self.sprites["ATTACK_2"][0].get_width (),
            self.sprites["ATTACK_2"][0].get_height (),
            self.identifier,
            self.attacking
        )


