#  ___________________________________________________________________________
# / Programmers:                    Player                  Date: 2023-01-14  \
# |     - Kyler. V                                                            |
# |     - Muntasir. M                                                         |
# |     - Ashwin. J                                                           |
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# |                  This class is used to control a player.                  |
# |                                                                           |
# \___________________________________________________________________________/


from Character import Character
from random import randint
from time import time
import pygame

class Player ():
    GRAVITY = 1.5
    KNOCK_BACK_DELAY = .5
    ATTACK_TIME = .3

    def __init__ (
        self,
        move_up: int,
        move_down: int,
        move_left: int,
        move_right: int,
        attacks: "list[int]"
    ):
        """
        Generate a player.

        Args:
            move_up (int): Up key.
            move_down (int): Down key.
            move_left (int): Left key.
            move_right (int): Right key.
            attacks (list[int]): Attack keys.
        """
        self.directions = [
            move_up,
            move_left,
            move_down,
            move_right
        ]
        self.attack_keys = attacks
        self.character = None
        self.movement = [0, 0, 0, 0]
        self.attacking_this_frame = 0
        self.knockback_from = []
        self.attack_info = [0, 0]


    # /////////////////////
    #   Public functions.
    # /////////////////////

    # =======================
    #   Movement functions.
    # =======================

    def move_character (self, offset: "list[int]") -> None:
        """
        Move the character.

        Args:
            offset (list[int]): The offset to move.
        """
        if (self.character != None):
            self.character.move (offset)

    def set_pos (self, pos: "list[int]") -> None:
        """
        Set the position of the character.

        Args:
            pos (list[int]): Position. (x, y)
        """
        if (self.character != None):
            self.character.set_pos (pos)

    def get_pos (self) -> None or "list[int]":
        """
        Get the position of the character.

        Returns:
            list[int] or None: The position of the character.
        """
        if (self.character != None):
            return self.character.pos
  
    def allow_movement (self) -> None:
        """
        Allow the character to move.
        """
        if (self.character != None):
            self.character.allow_movement ()

    def apply_gravity (self) -> None:
        """
        Apply a downward force to our character.
        """
        if (self.character != None):
            self.character.gravity ()
  
    def stop_moving (self) -> None:
        """
        Stop the character from moving.
        """
        if (self.character != None):
            self.character.stop_movement ()

    def reset_jump (self) -> None:
        """
        Reset the jump.
        """
        if (self.character != None):
            self.character.reset_jump ()

    def undo_move (self) -> None:
        """
        Undo the last move made to the character.
        """
        if (self.character != None):
            self.character.undo_move ()

    def apply_knockback (
        self, 
        identifier: int, 
        force_x: int=1, 
        force_y: int=0, 
        direction: bool=False
    ) -> None:
        """
        Apply a knockback force.

        Args:
            identifier (int): 
                The identifier of the object knocking this character back.
            force_x (int, optional):
                Apply a force to the X velocity. Defaults to 0.
            force_y (int, optional):
                Apply a force to the Y velocity. Defaults to 0.
            direction (bool, optional):
                Make the force apply in the same direction as 
                the attack is moving.
        """
        # ---------------------------------------------
        #   Find out if the object applying knockback 
        #   to us has applied knockback to us in the 
        #                 past second.
        # ---------------------------------------------
        go = True
        if (identifier in [x[0] for x in self.knockback_from]):
            go = False
            for data in self.knockback_from:
                if (identifier == data[0]):
                    if ((time () - data[1]) >= self.KNOCK_BACK_DELAY):
                        go = True
                        self.knockback_from.remove (data)

        # -------------------------------------------------
        #   If the object applying knockback didn't apply 
        #      knockback in the last second then apply 
        #                    knockback.
        # -------------------------------------------------
        if (go):
            if (self.character != None):
                if (direction):
                    direction = 1

                else:
                    direction = -1
                
                amount_to_add = force_x // 2
                if (amount_to_add < 1):
                    amount_to_add = 1

                for amount in range (amount_to_add * 4):
                    self.character.add_to_queue (
                        "MOVE",
                        [
                            [
                                (force_x * direction), 
                                -force_y
                            ]
                        ]
                    )
                self.knockback_from.append ([identifier, time ()])


    # =====================
    #   Attack functions.
    # =====================

    def check_collision (self, check_obj) -> bool:
        """
        Check the collision between this object and another object.

        Args:
            check_obj (object): The object to check against.

        Returns:
            bool: If we collide or not.
        """
        if (self.character != None):
            return self.character.check_collide (check_obj)

        return False

    def get_attacking_update_one (self) -> int:
        """
        Did we press attack this frame?

        Returns:
            int: What is the attack status this frame
        """
        return self.attacking_this_frame

    def reset_attacking_update (self) -> None:
        """
        Reset the attacking variable to 0.
        """
        self.attacking_this_frame = 0
    
    def attack (self, attack_pos: int):
        """
        

        Args:
            attack_pos (int): _description_

        Returns:
            _type_: _description_
        """
        if (self.character != None):
            return self.character.attacks[attack_pos - 1] ()

        return None

    def get_attacking (self) -> int:
        """
        Get the attacking value of the attacking

        Returns:
            int: The attacking value.
        """
        if (self.character != None):
            return self.character.get_attacking ()

        else:
            return 0


    # ===================
    #   Draw functions.
    # ===================

    def draw (self, win: pygame.Surface) -> None:
        """
        Draw onto the screen all player details.

        Args:
            win (pygame.Surface): Main window.
        """
        if (self.character != None):
            self.character.draw (win)


    # =====================
    #   Health functions.
    # =====================

    def set_sudden_death (self, health: int, max: int, width: int) -> None:
        """
        Setup the character for sudden death.

        Args:
            health (int): The health to be set at
        """
        if (self.character != None):
            self.set_starting_pos (
                max, 
                width
            )
            self.character.set_sudden_death (health)

    def adjust_health (self, amount: int, identifier: int) -> None:
        """
        Adjust the health of the character.

        Args:
            amount (int): Adjust by this amount.
        """
        if (self.character != None):
            if (self.attack_info[0] == identifier):
                if (time () - self.attack_info[1] > self.ATTACK_TIME):
                    self.character.adjust_health (amount)
            else:
                self.character.adjust_health (amount)
            
            self.attack_info = [identifier, time ()]

    def get_health (self) -> int:
        """
        Get the health of the character.

        Returns:
            int: The current health of the character.
        """
        if (self.character != None):
            return self.character.get_health ()
        return 0

    def get_lives (self) -> int:
        """
        Get the amount of lives the character has life.

        Returns:
            int: The amount of lives.
        """
        if (self.character != None):
            return self.character.get_lives ()
        return -1

    def is_dead (self) -> bool:
        """
        Is this player dead?

        Returns:
            bool: Dead or not.
        """
        if (self.character != None):
            return self.character.is_dead ()

        return False


    # ====================
    #   Other functions.
    # ====================

    def set_starting_pos (self, max: int, width: int) -> None:
        """
        Set the starting position of the characters.

        Args:
            max (int): The amount of players in total.
            width (int): The width of the window.
        """
        if (self.character != None):
            self.character.set_text_pos (width)
            pos = self.character.get_player_value ()

            # ----------------------------
            #   Add spacing to the wall.
            # ----------------------------
            padding = 40
            width -= padding * 2

            # ---------------------------------
            #   Decide where char will spawn.
            # ---------------------------------
            distance_between_chars = (width - (40 * max))
            player_pos = [
                padding + (distance_between_chars * (pos - 1)), 
                200
            ]

            self.character.set_pos (
                player_pos
            )

            self.starting_pos = player_pos

            if (pos == 1):
                self.character.set_direction (True)
            
            elif (max - pos != 0):
                self.character.set_direction (bool (randint (0, 1)))
            
            else: 
                self.character.set_direction (False)

    def set_character (self, character: Character) -> None:
        """
        Set the character value

        Args:
            character (subClass of Character):
                The character that the player has chosen.
        """
        self.character = character
        self._reset_character ()
        self.movement = [0 for i in range (len (self.movement))]

    def get_offset (self) -> "list[int]":
        """
        Get the movement offset.

        Args:
            movement (list[int]): The movement list.

        Returns:
            list[int]: The offset to move the character.
        """
        x_move = 0
        y_move = 0

        if (self.movement[0] != self.movement[2]):
            if (self.movement[0] == 1):
                y_move = -1
            else:
                y_move = 1

        if (self.movement[1] != self.movement[3]):
            if (self.movement[1] == 1):
                x_move = -1
            else:
                x_move = 1

        return [x_move, y_move]

    def key_event (self, event) -> None:
        """
        Decide what to do on key events.

        Args:
            event (pygame.Event): The current pygame event.
        """
        if (event.type == pygame.KEYDOWN):
            self._set_movement (event)
            self._set_attack (event)

        elif (event.type == pygame.KEYUP):
            self._un_set_movement (event)

    def get_identifier (self) -> int:
        """
        Get the characters identifier.

        Returns:
            int: Identifier.
        """
        if (self.character != None):
            return self.character.get_identifier ()
        
        return -2

    def has_character (self) -> bool:
        """
        Check if the player has a link to a character.

        Returns:
            bool: Is self.character is not none.
        """
        if (self.character == None):
            return False
        return True

    def run_checks (self) -> None:
        """
        Run checks on the character.
        """
        if (self.character != None):
            self.character.check ()

    def get_character (self):
        """
        Get the character class

        Returns:
            sub class of Character:
                The character that was assigned to this player.
        """
        return self.character


    # //////////////////////
    #   Private functions.
    # //////////////////////

    def _un_set_movement (self, event) -> None:
        """
        Un-set the movement list.

        Args:
            event (pygame event): An event object.
        """
        for pos, dir in enumerate (self.directions):
            if (event.key == dir):
                self.movement[pos] = 0

    def _set_movement (self, event) -> None:
        """
        Set the movement list.

        Args:
            event (pygame.Event): The current pygame event.
        """
        for pos, dir in enumerate (self.directions):
            if (event.key == dir):
                self.movement[pos] = 1

    def _set_attack (self, event) -> None:
        """
        Set the attacking value of the character.

        Args:
            event (pygame.Event): The current pygame event.
        """
        self.attacking_this_frame = 0
        for pos, key in enumerate (self.attack_keys):
            if (event.key == key):
                if (self.character.get_attacking () == 0):
                    self.character.set_attacking (pos + 1)
                    self.attacking_this_frame = pos + 1
                    self.character.moving = False

    def _reset_character (self) -> None:
        """
        Reset the characters values back to the default.
        """
        self.character.reset_character ()