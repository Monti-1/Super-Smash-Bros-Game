#  ___________________________________________________________________________
# / Programmers:                   Character                Date: 2023-01-14  \
# |     - Kyler. V                                                            |
# |     - Muntasir. M                                                         |
# |     - Ashwin. J                                                           |
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |                 This class is used to control a character.                |
# |                                                                           |
# \___________________________________________________________________________/

# =======================
#     Library imports
# =======================
from random import randint
from Text import Text
from time import time
import pygame
import os


class Character ():
    # -----------------------
    #   Constant variables.
    # -----------------------
    INVULNERABLE_TIME = 5 # Seconds
    MAX_HP = 200
    STEP = 1.5 # Pixels
    MAX_JUMPS = 2
    DISPLAY_TIME = 5 # Amount of frames
    MAX_X_SPEED = 30
    MAX_Y_SPEED = 30
    RESISTANCE = 10
    MOVE_X_SPEED = 1
    GRAVITY_EFFECT = 1.5
    JUMP_FORCE = GRAVITY_EFFECT * 10
    BOUNCE_RANGE = 14
    MAX_LIVES = 3

    def __init__ (
        self, images_file: str, damages: "list[int]", attacks: list, 
        movement_on_attacks: list,
        position: "list[int]"=[0, 0],
        knockback: "list[int]"=[[0, 0], [0, 0]],
        name: str="Character",
        player: int=1
    ):
        """
        Initialize the character

        Args:
            images_file (str): The path to the images for this character.
            damages (list[int]): A list of damages for each attack. 
            attacks (list[functions]): The attacks available to us.
            movement_on_attacks (list[list[int]]): 
                The movement that should be applied to the character on certain
                attacks. Form used: [[x diff, y diff], [x diff]]
            position (list[int], optional): Starting pos. Defaults to [0, 0].
            knockback (list[int], optional): Knockback force for each attack. 
                Defaults to [[0, 0], [0, 0]].
            name (str, optional): Used to keep track of who hit each other.
            player (int, optional): Determine where the character is at the beginning.
        """
        # -------------------
        #   Text variables.
        # -------------------
        self.spacing = len (name) * 10
        self.player = player
        self.name = name
        self._create_text ()

        # ---------------------
        #   Unseen variables.
        # ---------------------
        self.identifier = randint (0, 1000000000000000000000000000000000000000)
        self.lives = self.MAX_LIVES
        self.last_adjust = time ()
        self.movement_queue = []
        self.hp = self.MAX_HP
        self.dead = False
        
        # -----------------------
        #   Movement variables.
        # -----------------------
        self.facing_right = False
        self.walk_modifier = 1
        self.jump_counter = 0
        self.can_move = True
        self.jumping = False
        self.walking = False
        self.running = False
        self.pos = position
        self.moving = False
        self.vel = [0, 0]
        
        # ------------------------
        #   Attacking variables.
        # ------------------------
        self.movement_on_attacks = movement_on_attacks
        self.attacks = attacks
        self.counters = [0, 0, 0]
        self.attacking = 0
        self.damages = damages
        self.knockback = knockback
        self.can_take_damage = True

        # -------------------
        #   Image variables
        # -------------------
        self.sprites = self._get_all_animations (images_file)
        self.current_surface = self.sprites["WALK"][0]

        # --------------------
        #   Other variables.
        # --------------------
        self.respawn = [(400 - (self.current_surface.get_width () // 2)), 100]
        self.checks = []



    # /////////////////////////////
    #       Public functions.
    # /////////////////////////////

    # =============================
    #   Attack related functions.
    # =============================

    def get_attack_damages (self) -> "list[int]":
        """
        Get all the attack damages.

        Returns:
            list[int]:
                Return in index 0 the attack damage for
                attack_1 and in index 2 the attack damage
                for attack_2.
        """
        return self.damages

    def set_attacking (self, value: int) -> None:
        """
        Set the attacking value of the character.

        Args:
            value (int): The value that attacking should be.
        """
        self.attacking = value

    def get_knockback (self) -> "list[int]":
        """
        Get the knockback value of each attack

        Returns:
            list[int]: Knockback values.
        """
        return self.knockback

    def get_attacking (self) -> int:
        """
        Get the value of self.attacking.

        Returns:
            int: The value of self.attacking.
        """
        return self.attacking


    # =============================
    #   Health related functions.
    # =============================

    def adjust_health (self, amount: int) -> None:
        """
        Adjust the health of the character by adding an amount.

        Args:
            amount (int):
                The amount to add to self.hp. Amount can be negative.
        """
        if (self.can_take_damage):
            if ((self.hp + amount) <= 0):
                self.adjust_lives (-1)
                self.hp = self.MAX_HP

            else:
                self.hp += amount

    def adjust_lives (self, amount: int) -> None:
        """
        Adust the amount of lives left by adding an amount.

        Args:
            amount (int): 
                The amount to adjust the lives by. Amount can be negotiate.
        """
        if ((self.lives + amount) <= 0):
            self.dead = True
            self.lives = 0
        
        else:
            self.dead = False
            self.lives += amount
        
        self._move_to_respawn ()
        self.last_adjust = time ()

    def get_percentage (self) -> float:
        """
        Get the percentage of health left.

        Returns:
            float: The percent of health left.
        """
        total = self.hp / self.MAX_HP
        total *= 100
        total = round (total, 1)
        return total

    def get_max_health (self) -> int:
        """
        Get the max health of the character.

        Returns:
            int: The max health a character can be.
        """
        return self.MAX_HP

    def get_max_lives (self) -> int:
        """
        Get the max amount of lives that 
        this character can have.

        Returns:
            int: Lives
        """
        return self.MAX_LIVES

    def get_health (self) -> int:
        """
        Get the health of this character.

        Returns:
            int: The remaining hp of the character.
        """
        return self.hp

    def is_alive (self) -> bool:
        """
        Check if the character is dead or not.

        Returns:
            bool: Dead or not.
        """
        if (self.hp <= 0):
            return True
        
        return False

    def get_lives (self) -> int:
        """
        Get the amount of lives left.

        Returns:
            int: Lives left.
        """
        return self.lives

    def is_dead (self) -> bool:
        """
        Is this character dead?

        Returns:
            bool: Dead or not.
        """
        return self.dead


    # ===============================
    #   Movement related functions.
    # ===============================

    def add_to_queue (self, func: str, vars: list) -> None:
        """
        Add an item to the movement queue.

        Args:
            func (str): The type of function to run.
            vars (list): The arguments for the function in a list.
        """
        data = [func]
        data += vars
        self.movement_queue.append (data)

    def set_direction (self, direction: bool) -> None:
        """
        Set the self.facing_right value.

        Args:
            direction (bool): Facing right?
        """
        self.facing_right = direction

    def move (self, difference: "list[int]") -> bool:
        """
        Moves the character a distance.

        Args:
            difference (list[int, int]):
                A difference in speed either > 0, 0, or < 0. In positions x, y.

        Returns:
            bool: If moving the character was successful.
        """
        if (self.can_move):
            if (len (difference) == 2):
                # -----------------------------------------
                #   Check which direction we're going in.
                # -----------------------------------------
                x_vel = 0
                if (difference[0] > 0):
                    value = (self.MOVE_X_SPEED * self.walk_modifier)
                    value *= difference[0]

                elif (difference[0] < 0): 
                    value = (self.MOVE_X_SPEED * self.walk_modifier)
                    value *= difference[0]

                else:
                    value = 0

                x_vel += value

                # ----------------------------------
                #   Check if player wants to jump.
                # ----------------------------------
                if (difference[1] < 0):
                    if (self.jumping is False):
                        self._jump_sequence (-difference[1])
                        self.jumping = True
                
                else:
                    self.jumping = False

                # -------------------------------------
                #   Check for max speed acceleration.
                # -------------------------------------
                if (self.vel[0] > self.MAX_X_SPEED):
                    self.vel[0] = self.MAX_X_SPEED

                if (self.vel[1] > self.MAX_Y_SPEED):
                    self.vel[1] = self.MAX_Y_SPEED

                # -------------------------------------------
                #   Adjust variables to draw the character.
                # -------------------------------------------
                if (x_vel > 0):
                    self.facing_right = True
                    self.moving = True

                elif (x_vel < 0):
                    self.facing_right = False
                    self.moving = True

                else:
                    self.moving = False
                    self.walking = True

                # --------------------------------------------
                #   Deal with if the character is attacking.
                # --------------------------------------------
                if (self.attacking != 0):
                    x_move = self.movement_on_attacks[self.attacking - 1][0]
                    y_move = self.movement_on_attacks[self.attacking - 1][1]
                    if (not self.facing_right):
                        x_move = -x_move

                    x_vel += x_move
                    self.vel[1] += y_move

                # -----------------------------------
                #   Apply velocity to the position.
                # -----------------------------------
                self.pos[0] += (self.vel[0] + x_vel)
                self.pos[1] += self.vel[1]
                return True

            else:
                return False
        else:
            return False

    def set_pos (self, pos: "list[int]") -> None:
        """
        Set the position of the character.

        Args:
            pos (list[int]): The position to set it to.
            start (bool): Is this the starting position? Defaults to False.
        """
        self.pos = pos

    def check_collide (self, object) -> bool:
        """
        Checks to see if there is collision between
        this character and another object's sprite.

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

    def is_facing_right (self) -> bool:
        """
        Is the character facing right.

        Returns:
            bool: Is character facing right.
        """
        return self.facing_right

    def get_pos (self) -> "list[int]":
        """
        Get the position of the current character.

        Returns:
            tuple: Return position. (x_pos, y_pos)
        """
        return self.pos

    def allow_movement (self) -> None:
        """
        Allow the character to move.
        """
        self.can_move = True

    def stop_movement (self) -> None:
        """
        Make the character stop moving.
        """
        if (self.vel[0] > 0):
            value = -5
        elif (self.vel[0] < 0):
            value = 5
        else:
            value = 0
        self.vel = [self.vel[0] + value, 0]

    def reset_jump (self) -> None:
        """
        Reset the jump counter.
        """
        self.jump_counter = 0

    def move_queue (self) -> bool:
        """
        Run the first item of the movement queue.

        Returns:
            bool: If the movement was successful or not.
        """
        if (len (self.movement_queue) != 0):
            data = self.movement_queue.pop (0)
            return self._queue_format_dealings (data)

    def gravity (self) -> None:
        """
        Apply gravity to the character.
        """
        self.vel[1] += self.GRAVITY_EFFECT



    # ============================
    #   Image related functions.
    # ============================

    def draw (self, window: pygame.Surface) -> None:
        """
        Draws the character to the screen.

        Args:
            window (pygame.Surface): The main pygame window.
        """
        if (not self.dead):
            # -----------------------------------
            #   Set a default value for sprite.
            # -----------------------------------
            sprite = self.sprites["WALK"][0]
            if (not self.facing_right):
                sprite = pygame.transform.flip (sprite, True, False)

            if (self.moving):
                if (self.walking):
                    self.walk_modifier = 1
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
                    self.walk_modifier = 3
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

    def get_mask (self) -> pygame.mask.Mask or None:
        """
        Gets the mask of the current sprite on the screen.

        Returns:
            pygame.mask.Mask or None:
                Returns the mask if an image is on the screen.
        """
        if (self.current_surface != None):
            return pygame.mask.from_surface (self.current_surface)

        else:
            return None


    # ====================
    #   Other functions.
    # ====================
     
    def set_sudden_death (self, health: int) -> None:
        """
        Set the character up for sudden death.

        Args:
            health (int): The health to be set at.
        """
        self.hp = health
        self.lives = 1
        self.can_move = False

    def set_player_value (self, value: int) -> None:
        """
        Set the player value.

        Args:
            value (int): The player value.
        """
        self.player = value
        self._create_text ()

    def set_text_pos (self, width: int) -> None:
        """
        Set the position of the text

        Args:
            max (int): The max amount of players.
            width (int): The width of the window
        """
        basic_character_size = 190
        # ----------------------------
        #   Add spacing to the wall.
        # ----------------------------
        padding = 100
        width -= padding * 2

        # -----------------------------------------------
        #   Find the position for this characters text.
        # -----------------------------------------------
        x_pos = padding + (basic_character_size * (self.player - 1))
        self._create_text ([x_pos, 700])
       
    def get_player_value (self) -> int:
        """
        Get the player value assigned to the class.

        Returns:
            int: PLayer value.
        """
        return self.player

    def reset_character (self) -> None:
        """
        Resets the character.
        """
        self.hp = self.MAX_HP
        self.lives = self.MAX_LIVES
        self.dead = False
        self.vel = [0, 0]
        self.movement_queue = []
        self.moving = False
        self.walking = False
        self.running = False
        self.current_surface = self.sprites["WALK"][0]
        self.counters = [0 for i in range (len (self.counters))]

    def get_identifier (self) -> int:
        """
        Get the identifier of the character.

        Returns:
            int: Identifier.
        """
        return self.identifier

    def check (self) -> None:
        """
        Run a few checks needed for the characters.
        """
        for check in self.checks:
            if (check[0] == "RESPAWN"):
                if (self._check_move_after_respawn (check[1])):
                    self.checks.remove (check)


    # //////////////////////////////
    #       Private functions.
    # //////////////////////////////


    def _get_all_animations (self, character_images_path: str) -> dict:
        """
        Load all of the animations into a dictionary.

        Args:
            character_images_path (str):
                The path to the specific images folder for this character.
        """
        # -------------------------------------------
        #   Go through each item in the given path.
        # -------------------------------------------
        self.all_animations = {}
        for path in os.listdir (character_images_path):
            updated_path = os.path.join (character_images_path, path)

            # ---------------------------------------------------
            #   If this path is a directory and not a file then
            #    make pygame surfaces out of all of the images
            #           that have no spaces in them.
            # ---------------------------------------------------
            if (os.path.isdir (updated_path)):
                print (F"Folder: {path}")
                path = path.upper ()
                self.all_animations[path] = [[], []]

                # ----------------------------------------------------
                #   Search for images and make then pygame.Surface's
                # ----------------------------------------------------
                for file in os.listdir (updated_path):
                    file_path = os.path.join (updated_path, file)

                    if (" " not in file and os.path.isfile (file_path)):
                        print (f"\tImage: {file}")
                        self.all_animations[path][0].append (
                            pygame.image.load (file_path)
                        )

                        if (file.find (".jpg") != -1):
                            file = file.replace (".jpg", "")
                        else:
                            file = file.replace (".png", "")

                        number = int (file[-2:])
                        self.all_animations[path][1].append (number)
                print ()

        character_name = character_images_path.split ("\\")[-1]
        print (f"End of images for: {character_name}")

        # ------------------------------------
        #   Sort the list in ascending order
        #       for animation purposes.
        # ------------------------------------
        self._sort_ascending_animations ()

        return self.all_animations

    def _check_move_after_respawn (self, start_time: float) -> bool:
        """
        Check to see if player should be allowed to move again.

        Args:
            start_time (float): Time the player was sent to the respawn point.
        
        Returns:
            bool: Is character's invulnerability over.
        """
        if ((time () - start_time) >= self.INVULNERABLE_TIME):
            self.can_take_damage = True
            return True
        
        else:
            self.can_take_damage = False
            pos = [
                self.pos[0], 
                (self.respawn[1] - self.current_surface.get_height ())
            ]
            self.set_pos (pos)
            return False

    def _draw_health_info (self, window: pygame.Surface) -> None:
        """
        Draw the character details at the bottom of the screen.

        Args:
            window (pygame.Surface): The window to draw onto.
        """
        if (self.text != None):
            self.text[0].set_text_color ((255, 255, 255))
            self.text[0].draw (window)

            health = int (self.get_percentage ())
            if (health >= 75):
                self.text[1].set_text_color ((61, 173, 0))
            elif (health >= 50):
                self.text[1].set_text_color ((255, 255, 41))
            elif (health >= 25):
                self.text[1].set_text_color ((255, 106, 0))
            else:
                self.text[1].set_text_color ((199, 27, 0))

            if (not self.dead):
                self.text[1].set_text (str (health) + "%")
                self.text[1].draw (window)
            
            else:
                self.text[1].set_text_color ((199, 27, 0))
                self.text[1].set_text ("DEAD")
                self.text[1].draw (window)

            image_details = self.text[2][-(self.lives + 1)]
            window.blit (image_details[0], image_details[1])

    def _jump_sequence (self, jump_multiplier: int=1) -> None:
        """
        Allow the character to jump MAX_JUMPS times.

        Args:
            jump_multiplier (int, optional): 
                Multiplier for jumps. Defaults to 1.
        """
        if (self.jump_counter < self.MAX_JUMPS):
            self.vel[1] = -(self.JUMP_FORCE * jump_multiplier)
            self.jump_counter += 1

    def _recursive_sort (self, lists: "list[list]") -> list:
        """
        Simple recursive sort to sort both of the lists in parallel.

        Args:
            lists (list[list]): A list containing multiple lists.

        Returns:
            list[list]:
                Returns the sorted sort list and mirror list. [sort, mirror]
        """
        for pos in range (1, len (lists[0])):
            if (lists[0][pos - 1] > lists[0][pos]):
                for a_list in lists:
                    temp = a_list[pos - 1]
                    a_list[pos - 1] = a_list[pos]
                    a_list[pos] = temp

                return self._recursive_sort (lists)

        return lists[1]

    def _queue_format_dealings (self, data: list) -> bool:
        """
        Go through the data and depending on the 
        function run a certain command.

        Args:
            data (list): The data that is in the queue.

        Returns:
            bool: Whether the function was successful.
        """
        func = data[0]
        vars = data[1:]
        if (func == "MOVE"):
            return self.move (vars[0])

    def _sort_ascending_animations (self) -> None:
        """
        Sort self.all_animations in ascending order.
        """
        for key in self.all_animations:
            list_to_sort = self.all_animations[key][1]
            list_to_mirror = self.all_animations[key][0]

            results = self._recursive_sort ([list_to_sort, list_to_mirror])

            self.all_animations[key] = results

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
        return [int (pos[0] - self.pos[0]), int (pos[1] - self.pos[1])]

    def _move_to_respawn (self) -> None:
        """
        Move to the respawn location.
        """
        self.vel = [0, 0]
        self.set_pos ([self.respawn[0], self.respawn[1]])
        self.movement_queue = []
        self.can_take_damage = False
        self.checks.append (["RESPAWN", time ()])
        self.current_surface = self.sprites["WALK"][0]

    def _create_text (self, pos: "list[int]"=None) -> None:
        """
        Create the text.
        """
        self.text = [
            Text (
                self.name, 
                ((self.player * 150), 700) if (pos == None) else pos, 
                [255, 255, 255]
            ),
            Text (
                "100%", 
                (0, 0),
                [61, 173, 0]
            ),
            [
                [
                    pygame.transform.scale (
                        pygame.image.load (
                            os.path.join (
                                os.path.join (os.getcwd (), "IMGS", "Health"),
                                f"Health_{x}.png"
                            )
                        ),
                        (100, 100)
                    ), 
                    [0, 0]
                ] for x in range (1, 5)
            ]
        ]

        text_1_width = self.text[0].get_width ()
        text_1_height = self.text[0].get_height ()
        space = 10
        self.text[1].set_pos (
            [
                self.text[0].get_pos ()[0] + text_1_width + space,
                self.text[0].get_pos ()[1]
            ]
        )
        for pos in range (len (self.text[2])):
            self.text[2][pos][1][1] = self.text[0].get_pos ()[1] 
            self.text[2][pos][1][1] += text_1_height
            self.text[2][pos][1][0] = self.text[0].get_pos ()[0] 




if (__name__ == "__main__"):
    test = Character (os.path.join (
            os.getcwd (),
            "IMGS",
            "Link"
        ),
        [0, 0]
    )

    test.adjust_health (0)
    print (test.get_percentage ())
    test.adjust_health (-10)
    print (test.get_percentage ())
    test.adjust_health (-30)
    print (test.get_percentage ())
    test.adjust_health (-10)
    print (test.get_percentage ())
    test.adjust_health (-25)
    print (test.get_percentage ())
    test.adjust_health (-10)
    print (test.get_percentage ())

    print (test.get_health ())