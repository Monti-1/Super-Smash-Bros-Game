#  ___________________________________________________________________________
# / Programer: Ashwin .J        Captain_Falcon               Date: 2022-12-23 \
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |              This class is used to control Captain Falcon                 |
# |                                                                           |
# | Functions:                                                                |
# |     __init__:                                                             |
# |         - Initializes Captain Falcon.                                     |
# |                                                                           |
# |     attack_1:                                                             |
# |         - The first attack that Captain Falcon can use.                   |
# |                                                                           |
# |     attack_2:                                                             |
# |         - The second attack that Captain Falcon can use.                  |
# |                                                                           |
# |     draw:                                                                 |
# |         - Used for a custom draw function.                                |
# |                                                                           |
# \___________________________________________________________________________/

from Character import *
import os

class Captain_Falcon(Character):

    def __init__(self, images_path: str, pos: "list[int]", text_pos: int):
        """
        Initialize Captain Falcon.

        Args:
            images_path (str): Path to all images
        """
        character_images_path = os.path.join (images_path, "Captain Falcon")

        # ------------------------
        #   Attacking variables.
        # ------------------------

        self.attack_counter = 0
        self.attack_1_damage = 10
        self.attack_2_damage = 30

        # ---------------------------------------------
        #   Run the initializer for the parent class.
        # ---------------------------------------------
        super ().__init__(
            character_images_path,
            [self.attack_1_damage, self.attack_2_damage], 
            [self.attack_1, self.attack_2],
            [[0, 0], [0, 0]],
            position=pos,
            knockback=[[5, .2], [7, .3]],
            name="Captain falcon",
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
        self.step_modifier_x = 3

    def attack_2 (self) -> None:
        """
        Activate attack 2.
        """
        self.attacking = 2
    
    def draw (self, window: pygame.Surface) -> None:
        """
        Draws the sprite to the screen

        Args:
            window (pygame.Surface): The main pygame window
        """
        if (not self.dead):
            if (self.moving):
                if (self.walking):
                    self.walk_modifier = 2
                    max_counter = len (self.sprites["WALK"]) * self.DISPLAY_TIME

                    # -----------------------------
                    #   Reset our index if we are
                    #       at the end of the
                    #          animation.
                    # -----------------------------
                    if (self.counters[0] + 1 >= max_counter):
                        self.counters[0] = 0
                        self.walking = False
                        self.running = True

                    index = self.counters[0] // self.DISPLAY_TIME

                    # ---------------------------
                    #   Get the image and apply
                    #   proper transformations
                    #         if needed.
                    # ---------------------------
                    sprite = self.sprites["WALK"][index]
                    if (not self.facing_right):
                        sprite = pygame.transform.flip (sprite, True, False)

                    self.counters[0] += 1

                elif (self.running):
                    self.walk_modifier = 6
                    max_counter = len (self.sprites["RUN"]) * self.DISPLAY_TIME

                    # -----------------------------
                    #   Reset our index if we are
                    #       at the end of the
                    #          animation.
                    # -----------------------------
                    if (self.counters[1] + 1 >= max_counter):
                        self.counters[1] = 0

                    index = self.counters[1] // self.DISPLAY_TIME
                    sprite = self.sprites["RUN"][index]
                    if (not self.facing_right):
                        sprite = pygame.transform.flip (sprite, True, False)

                    self.counters[1] += 1

                self.attacking = 0

            elif (self.attacking != 0):
                attack_index = "ATTACK_" + str (self.attacking)
                max_counter = len (self.sprites[attack_index]) * self.DISPLAY_TIME

                # -----------------------------
                #   Reset our index if we are
                #       at the end of the
                #          animation.
                # -----------------------------
                if (self.counters[2] + 1 >= max_counter):
                    self.counters[2] = 0
                    self.attacking = 0

                index = self.counters[2] // self.DISPLAY_TIME
                sprite = self.sprites[attack_index][index]
                if (not self.facing_right):
                    sprite = pygame.transform.flip (sprite, True, False)

                self.counters[2] += 1


            else:
                sprite = self.sprites["WALK"][0]
                if (not self.facing_right):
                    sprite = pygame.transform.flip (sprite, True, False)

            if (not self.moving):
                if (not self.walking):
                    self.counters[0] = 0
                elif (not self.running):
                    self.counters[1] = 0

            self.current_surface = sprite
            window.blit (
                sprite,
                self.pos
            )

        # --------------------------------
        #   Draw the health information.
        # --------------------------------
        self._draw_health_info (window)




if (__name__ == "__main__"):
    player_1 = Captain_Falcon (os.path.join (os.getcwd (), "IMGS"))