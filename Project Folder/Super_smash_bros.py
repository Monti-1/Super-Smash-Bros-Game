#  ___________________________________________________________________________
# / Programmers:               Super Smash Bros             Date: 2022-12-22  \
# |     - Kyler. V                                                            |
# |     - Muntasir. M                                                         |
# |     - Ashwin. J                                                           |
# |                                                                           |
# |                               Description                                 |
# |                                                                           |
# | This file is the main entry point for Super Smash Bros. This program will |
# |  setup two different players. One player is controlled by W, A, S, and D  |
# |   like a usual game. The other player is controlled by P, L, ;, and '.    |
# |  This is not a common choice of keybindings but it is set there for easy  |
# |                                 testing.                                  |
# |                                                                           |
# |  Once players are created we enter the main game loop where we limit our  |
# |  FPS to 30 and go over game events. In the game events we pass along the  |
# | information to our Player classes and let them decide what to do with the |
# |                               character.                                  |
# |                                                                           |
# | We then check to see if we have any players that are currently attempting |
# |  to initiate an attack. If they are we will check if that spawns another  |
# | object. If it does indeed do so we will add it to our currently displayed |
# | attack objects. Once the attack expires we will remove it from this list. |
# |                                                                           |
# | We then check for collision with the players against everything. This     |
# | includes:                                                                 |
# |                                                                           |
# |     Attacks                                                               |
# |     Platforms (To be added)                                               |
# |                                                                           |
# | If there is any collision between them we deal with it appropriately for  |
# |                      each object it collides with.                        |
# |                                                                           |
# |  Finally we draw onto the screen all of our assets and anything we may    |
# | want displayed. We layer the drawing in a specific way to make sure that  |
# |        anything thats supposed to be behind everything does so.           |
# |                                                                           |
# \___________________________________________________________________________/
from Captain_Falcon import Captain_Falcon
from Lightning import Lightning
from Platform import Platform
from Pikachu import Pikachu
from random import randint
from Player import Player
from Button import Button
from Images import Images
from Link import Link
from Text import Text
from time import time
from pygame import mixer
import pygame
import os

WIN_SIZE = (800, 800) # The size of the game window.
FPS = 30              # A cap to the amount of fps.

def collision (players: "list[Player]", attcks: list, platforms: list) -> None:
    """
    Check for collision between the players attacks and platforms.

    Args:
        players (list[Player]): The list of players in the game.
        attcks (list): The list of attacks on the screen.
        platforms (list): The list of platforms in the game.
    """
    def checks (player: Player, attack) -> bool:
        if (player.has_character ()):
            if (player.get_identifier () != attack.get_identifier ()):
                if (player.check_collision (attack)):
                    return True
        
        return False

    for player in players:
        if (player.has_character ()):
        
            # -------------------------------------------------
            #   Check collisions against players and attacks.
            # -------------------------------------------------
            for attack in attcks:
                if (checks (player, attack)):
                    damage = attack.get_attack_damage ()
                    player.adjust_health (-damage, attack.get_identifier ())

                    knockback = [[0, 0], [0, 0]]
                    for other_player in players:
                        player_2 = other_player.character
                        if (attack.get_identifier () == player_2.get_identifier ()):
                            knockback = player_2.get_knockback ()

                    player_pos = player.get_pos ()
                    attack_pos = attack.get_pos ()
                    if (player_pos[0] < attack_pos[0]):
                        direction = False
                    elif (player_pos[0] > attack_pos[0]):
                        direction = True
                    player.apply_knockback (
                            attack.get_identifier (),
                            force_x=knockback[attack.num - 1][0],
                            force_y=knockback[attack.num - 1][1], 
                            direction=direction
                        )

            # ---------------------------------------------------
            #   Check collisions against players and platforms.
            # ---------------------------------------------------
            for platform in platforms:
                if (not player.check_collision (platform)):
                    player.apply_gravity ()

                else:
                    player.stop_moving ()
                    player.reset_jump ()

                    # ----------------------------------------------------------
                    #   Put the player a little below the top of the platform.
                    # ----------------------------------------------------------
                    pos = player.get_pos ()
                    if (pos != None):
                        while (player.check_collision (platform)):
                            pos[1] -= 1
                            player.set_pos (pos)
                        pos[1] += 3
                        player.set_pos (pos)

            # -------------------------------------------------
            #   Check collisions against players and players.
            # -------------------------------------------------
            for player_two in players:
                if (player_two != player):
                    if (player_two.has_character ()):
                        p2_character = player_two.get_character ()
                        p1_character = player.get_character ()
                        if (player.check_collision (p2_character)):
                            attack = player.get_attacking ()
                            if (attack != 0):
                                attack -= 1

                                damages = p1_character.get_attack_damages ()
                                player_two.adjust_health (
                                    -damages[attack], 
                                    player.get_identifier ()
                                )

                                knockback = p1_character.get_knockback ()
                                player_two.apply_knockback (
                                    p1_character.get_identifier (),
                                    force_x=knockback[attack][0],
                                    force_y=knockback[attack][1], 
                                    direction=p1_character.is_facing_right ()
                                )

            # --------------------------------------
            #   Check if player fell off the edge.
            # --------------------------------------
            if (player.get_pos ()[1] >= WIN_SIZE[1]):
                player.adjust_health (-(player.get_health () + 10), -1)

def get_background (imgs: str, index: int) -> pygame.Surface:
    """
    Get a background for the game.

    Args:
        imgs (str): The images path
        index (int): The index of the background.

    Returns:
        pygame.Surface: The background image
    """
    backgrounds = os.path.join (
        imgs,
        "Maps", 
        "Backgrounds"
    )

    return pygame.transform.scale (
        pygame.image.load (
            os.path.join (
                backgrounds,
                f"Background_{index+1}.png"
            )
        ),
        WIN_SIZE
    )

def attack (players: "list[Player]", attacks) -> list:
    """
    Check if the players are attacking
    if so add it to the return list.

    Args:
        players (list[Player]): The list of players.
        attacks (list[Attack]): The list of Attacks

    Returns:
        list:
            The return from all attacks if the attack doesn't return None.
    """
    for player in players:
        value = None
        attack_value = player.get_attacking_update_one ()
        player.reset_attacking_update ()

        if (attack_value != 0):
            value = player.attack (attack_value)
            # ------------------------------
            #   Special cases for attacks.
            # ------------------------------
            if (isinstance (value, Lightning)):
                attack_instances = [
                    isinstance (attack, Lightning)
                    for attack in attacks
                ]
                if (True in attack_instances):
                    value = None

        if (value != None):
            attacks.append (value)

    return attacks

def get_time (minutes: int, seconds: int) -> str:
    """
    Get the time in a string format.

    Args:
        minutes (int): The minutes as a number.
        seconds (int): The seconds as a number.

    Returns:
        str: The time represented as ##:##
    """
    if (len (str (minutes)) < 2):
        minutes = f" {minutes}"
    else:
        minutes = str (minutes)
    
    if (len (str (seconds)) < 2):
        seconds = f"0{seconds}"
    else:
        seconds = str (seconds)
    
    return f"{minutes}:{seconds}"

def draw_window (
    window: pygame.Surface,
    players: list,
    attacks: list,
    platforms: "list[Platform]",
    background: pygame.Surface=None,
    texts: list=[]
) -> "list":
    """
    Draw the window.

    Args:
        window (pygame.Surface): Window to draw on top.
        players (list): The players to draw.
        attacks (list): The attacks to draw.
        platforms (list[Platform]): The platforms to draw.
        background (pygame.Surface, optional): 
            The background to draw. Defaults to None.
        texts (list, optional): Text to draw. Defaults to [].

    Returns:
        list: Attacks left.
    """
    if (background != None):
        window.blit (background, (0, 0))

    else:
        window.fill ((0, 0, 0))

    for platform in platforms:
        platform.draw (window)

    for attack in attacks:
        if (attack.draw (window) != True):
            attacks.remove (attack)

    for player in players:
        player.draw (window)
        if (player.character != None):
            player.character.move_queue ()

    for text in texts:
        text.draw (window)

    pygame.display.update ()
    return attacks


# -------------------------
#   Game state functions.
# -------------------------

def activate_tie (players: "list[Player]", background: int) -> "list[Text]":
    """
    Activate the tie condition of the game.

    Args:
        players (list[Player]): The remaining players.
        background (int): The background index.

    Returns:
        list[Text]: Text to be displayed.
    """
    # --------------------------------------------
    #   Set the characters to sudden death mode.
    # --------------------------------------------
    sudden_death_health = 400
    for player in players:
        player.set_sudden_death (
            sudden_death_health,
            len (players),
            WIN_SIZE[0]
        )
    
    # ---------------------------------------------
    #   Create the text that is going to be used.
    # ---------------------------------------------
    black_bgrnds = [1]
    text_color = (255, 255, 255)
    if (background in black_bgrnds):
        text_color = (0, 0, 0)

    text = Text (
        "SUDDEN DEATH",
        [0, 0],
        text_color,
        font_size=50
    )

    text.set_pos (
        [
            (WIN_SIZE[0] // 2) - (text.get_width () // 2), 
            (WIN_SIZE[1] // 2)
        ]
    )
    return [
        text, 
        [
            20,     # Text expiry time in seconds,
            False,  # Have we done the appropriate steps
            1,      # Minutes for sudden death to last
            0       # Seconds for sudden death to last
        ]
    ]

def activate_win (player: Player, background: int) -> "list[Text]":
    """
    Activate the win condition of the game.

    Args:
        player (Player): The winning player.
        background (int): The background index.

    Returns:
        list[Text]: Text to be displayed.
    """
    player_character = player.get_character ()
    player_value = player_character.get_player_value ()

    # --------------
    #   Make text.
    # --------------
    black_bgrnds = [1]
    text_color = (255, 255, 255)
    if (background in black_bgrnds):
        text_color = (0, 0, 0)

    text_1 = Text (
        f"Congrats player {player_value}!",
        (0, 0),
        text_color,
        font_size=30
    )
    text_2 = Text (
        "You win!",
        (0, 0),
        text_color,
        font_size=30
    )

    # -------------------------
    #   Adjust the positions.
    # -------------------------
    spacing = 1
    offset = -100
    text_1_dimensions = [text_1.get_width (), text_1.get_height ()]
    text_1_pos = [
        (WIN_SIZE[0] // 2) - (text_1_dimensions[0] // 2),
        ((WIN_SIZE[1] // 2) - (text_1_dimensions[1] // 2)) - (spacing // 2)
    ]

    text_2_dimensions = [text_2.get_width (), text_2.get_height ()]
    text_2_pos = [
        (WIN_SIZE[0] // 2) - (text_2_dimensions[0] // 2),
        ((WIN_SIZE[1] // 2) - (text_2_dimensions[1] // 2)) - (spacing // 2)
    ]
    text_2_pos[1] += text_1_dimensions[1] + spacing

    text_1_pos[1] += offset
    text_2_pos[1] += offset

    text_1.set_pos (text_1_pos)
    text_2.set_pos (text_2_pos)

    return [text_1, text_2, time ()]

def activate_draw (background: int):
    """
    Activate the draw condition of the game.

    Args:
        background (int): The background index
    """
    black_bgrnds = [1]
    text_color = (255, 255, 255)
    if (background in black_bgrnds):
        text_color = (0, 0, 0)

    text = Text (
        "Draw",
        [0, 0],
        text_color,
        font_size=30
    )

    text.set_pos (
        [
            (WIN_SIZE[0] // 2) - (text.get_width () // 2),
            (WIN_SIZE[1] // 2) - 100 
        ]
    )
    return [text, time ()]

def check_end_game (
    players: "list[Player]", 
    background: int,
    sudden_death: bool
) -> "list[Text]" or None:
    """
    Check all end game conditions.

    Args:
        players (list[Player]): All players.
        background (int): The background index.
        sudden_death (bool): Are we in sudden death.
    
    Returns:
        list or None: None or [text, text, ..., time or list]
    """
    # ----------------------------------
    #   Get the health of all players.
    # ----------------------------------
    healths = []
    for player in players:
        if (player.get_health () != 0):
            healths.append (
                [
                    player.get_lives (), 
                    player.get_health (), 
                    player
                ]
            )

    # ---------------------------
    #   Rank all health values.
    # ---------------------------
    ranks = {}
    for health in healths:
        if (health[0] not in ranks.keys ()):
            ranks[health[0]] = [[health[1], health[2]]]
        else:
            ranks[health[0]].append ([health[1], health[2]]) 
    
    rankings = list (ranks.keys ())
    rankings.sort (reverse=True)

    # -----------------------------
    #   Check for win conditions.
    # -----------------------------
    if (len (rankings) > 1):
        # ------------------------------------------
        #   If there are players at different live 
        #          values decide who wins. 
        # ------------------------------------------
        if (len (ranks[rankings[0]]) > 1):
            if (sudden_death):
                highest = [0, None]
                for player in ranks[rankings[0]]:
                    if (player[0] > highest[0]):
                        highest = [player[0], player[1]]
                
                return activate_win (highest[1], background)
            return activate_tie ([player[1] for player in ranks[rank]], background)
        else:
            return activate_win (ranks[rankings[0]][0][1], background)
    
    else:
        # -------------------------------------
        #   If all players left have the same 
        #         amount of lives left.
        # -------------------------------------
        rank = rankings[0]
        healths = {}
        for player in ranks[rank]:
            if (player[0] not in healths.keys ()):
                healths[player[0]] = [player[1]]
            else:
                healths[player[0]].append (player[1])
        
        rankings = list (healths.keys ())
        rankings.sort (reverse=True)

        # -----------------------------------------
        #   Decide who wins or if there is a tie.
        # -----------------------------------------
        ranking = rankings[0]
        if (len (ranks[rank]) > 1):
            if (sudden_death):
                highest = [0, None]
                count = 0
                for player in ranks[rank]:
                    if (player[0] > highest[0]):
                        highest = [player[0], player[1]]
                        count = 0
                    if (player[0] == highest[0]):
                        count += 1
                
                if (count != 0):
                    return activate_draw (background)
                return activate_win (highest[1], background)
            return activate_tie ([player[1] for player in ranks[rank]], background)
        else:
            return activate_win (ranks[rank][ranking][0], background)


# ------------------
#   Main function.
# ------------------

def main ():
    def main_menu (win: pygame.Surface, plyrs: list) -> list:
        """
        Create the main menu.

        Args:
            win (pygame.Surface): The window to draw on.

        Returns:
            list: The players and if the user quit
        """
        # I have no idea why this variable is out of scope.
        global players_selected 
        plyr_names = ["Link", "Pikachu", "Captain Falcon"]
        bg_names = ["Haunted forest", "Peachy meadow", "Interstellar"]

        players_selected = 1
        max_players = 2
        padding = 20
        button_width = 200
        button_height = 100


        def player_select (_: int=0, data_in=None) -> list:
            """
            Select player screen.

            Args:
                _ (int): Unused variable.
                data_in : Used with detail_checker. Defaults to None.

            Returns:
                list: [[buttons], [images], [texts], data]
            """
            player_text = Text (
                text=f"Player {players_selected}", pos=[0, 0], 
                text_color=(255, 255, 255), font_size=30
            )
            player_text.set_pos (
                [
                    (WIN_SIZE[0] // 2) - (player_text.get_width () // 2),
                    10
                ]
            )
            x = WIN_SIZE[0] - (2 * padding)
            x -= len (plyr_names) * button_width
            x //= len (plyrs) - 1
            return [
                [
                    Button (
                        x=padding + (button_width * pos) + (x * pos), 
                        y=100, width=button_width, height=button_height,
                        buttonText=plyr_names[pos], 
                        onclickFunction=detail_checker, index=pos
                    ) for pos in range (len (plyrs))
                ],
                [
                    Images (
                        x=padding + (button_width * pos) + (x * pos),
                        y=250, width=200, height=400, image=plyr_names[pos], 
                        sub_image_path="Char"
                    ) for pos in range (len (plyrs))
                ],
                [
                    player_text
                ],
                data_in
            ]

        def maps (data_in: int) -> list:
            """
            The map selection mini screen.

            Returns:
                list: [[buttons], [images], [texts], data]
            """
            map_text = Text (
                text="Select map", pos=[0, 0], 
                text_color=(255, 255, 255), font_size=30
            )
            map_text.set_pos (
                [
                    (WIN_SIZE[0] // 2) - (map_text.get_width () // 2),
                    10
                ]
            )
            x = WIN_SIZE[0] - (2 * padding)
            x -= len (bg_names) * button_width
            x //= len (bg_names) - 1
            return [
                [
                    Button (
                        x=padding + (button_width * pos) + (x * pos), 
                        y=650, width=button_width, height=button_height,
                        buttonText=bg_names[pos], 
                        onclickFunction=detail_checker, index=pos
                    ) for pos in range (len (bg_names))
                ],
                [
                    Images (
                        x=padding + (button_width * pos) + (x * pos),
                        y=100, width=200, height=500, image=bg_names[pos], 
                        sub_image_path="Bg"
                    ) for pos in range (len (bg_names))
                ],
                [
                    map_text
                ],
                data_in
            ]

        def detail_checker (index: int) -> list:
            global players_selected
            """
            Middle man function between mini screen switches.

            Args:
                index (int): The index of what was selected.

            Returns:
                list: [[buttons], [images], [texts], data]
            """
            if (players_selected < max_players):
                players_selected += 1
                return player_select (data_in=index)
            
            elif (players_selected == max_players + 1):
                return [[], [], [], index]

            else:
                players_selected += 1
                return maps (index)
                

        buttons = [
            Button (
                x=(WIN_SIZE[0] // 2) - (button_width // 2),
                y=600,
                width=button_width,
                height=button_height,
                buttonText="Start",
                onclickFunction=player_select,
                index=0
            )
        ]

        images = []
        texts = []
        data = []
        time_temp = 0

        quit = False
        run = True
        while run:
            # ----------------------------
            #   Deal with pygame events.
            # ----------------------------
            for event in pygame.event.get ():
                if (event.type == pygame.QUIT):
                    run = False
                    quit = True
                
                if (event.type == pygame.MOUSEBUTTONUP):
                    if (time () - time_temp > 1 or time_temp == 0):
                        for button in buttons:
                            returns = button.clicked ()
                            if (returns != None):
                                buttons = returns[0]
                                images = returns[1]
                                texts = returns[2]
                                if (returns[3] != None):
                                    data.append (returns[3])

            # -------------------------
            #   Draw onto the window.
            # -------------------------
            win.fill ((0, 0, 0))

            for button in buttons:
                button.update_color ()
                button.draw (win)
            
            for image in images:
                image.draw (win)
            
            for text in texts:
                text.draw (win)
            
            pygame.display.update ()

            if (len (buttons) == 0):
                if (len (images) == 0):
                    if (len (texts) == 0):
                        run = False
        
        return data + [quit]

    global win
    win = pygame.display.set_mode (WIN_SIZE)
    clock = pygame.time.Clock ()

    music_file = r"C:\Users\munta\Downloads\Project Folder\Project Folder\SOUNDS\bg_music_02.mp3"
    mixer.init ()
    mixer.music.load (music_file)
    mixer.music.play (loops=-1)

    imgs_path = os.path.join (
        os.getcwd (),
        "Project Folder"
        "IMGS"
    )
    players_classes = [
        Link (imgs_path, [0, 0], 0),
        Pikachu (imgs_path, [0, 0], 0),
        Captain_Falcon (imgs_path, [0, 0], 0)
    ]

    run = True
    timer_minutes = 5
    timer_seconds = 0

    platforms = [
        Platform (
            0, 0,
            pygame.image.load (
                os.path.join (
                    os.getcwd (), 
                    "IMGS", 
                    "Maps", 
                    "Platforms",
                    "Platform_2.png"
                )
            )
        )
    ]

    platforms[0].set_pos (
        [
            # Offset by 10
            (WIN_SIZE[0] // 2) - (platforms[0].get_width () // 2) - 10,
            400
        ]
    )

    players = [
        Player (
            pygame.K_w, # Up
            pygame.K_s, # Down
            pygame.K_a, # Left
            pygame.K_d, # Right
            [
                pygame.K_q, # Attack 1
                pygame.K_e  # Attack 2
            ]
        ),
        Player (
            pygame.K_p,             # Up
            pygame.K_SEMICOLON,     # Down
            pygame.K_l,             # Left
            pygame.K_QUOTE,         # Right
            [
                pygame.K_o,             # Attack 1
                pygame.K_LEFTBRACKET    # Attack 2
            ]
        )
    ]
    attacks = []
    
    tie_checks = [False]
    timer_paused = False
    time_recorded = time ()
    move_screen = -1
    while (run):
        clock.tick (FPS)

        # ---------------------
        #   Changing screens.
        # ---------------------
        if (move_screen != 0 or move_screen == -1):
            if (time () - move_screen > 10 or move_screen == -1):
                move_screen = 0

                data = main_menu (win, players_classes)
                if (data[-1]):
                    return

                timer_minutes = 0
                timer_seconds = 20
                tie_checks = [False]

                background = get_background (imgs_path, data[-2])
                background_index = data[-2]
                data = data[:-2]

                timer = get_time (timer_minutes, timer_seconds)
                texts = [
                    Text (
                        timer,
                        (WIN_SIZE[1] - len (timer) * 9, 0),
                        (255, 255, 255)
                    )
                ]

                # -----------------------------------------------
                #   Assign the correct character to the player.
                # -----------------------------------------------
                for pos, player in enumerate (players):
                    if (pos < len (data)):
                        players_classes[data[pos]].set_player_value (pos + 1)
                        player.set_character (players_classes[data[pos]])

                # ------------------------------------------------------
                #   Get the players to spawn in relatively nice areas.
                # ------------------------------------------------------
                for player in players:
                    player.set_starting_pos (len (players), WIN_SIZE[0])
                
                timer_paused = False

        # ---------------
        #   Game timer.
        # ---------------
        if (not timer_paused):
            if ((time () - time_recorded) >= 1):
                if ((timer_seconds - 1) < 0):
                    timer_seconds = 59
                    timer_minutes -= 1
                
                else:
                    timer_seconds -= 1

                # ----------------------
                #   End of game check.
                # ----------------------
                if (timer_minutes == 0 and move_screen == 0):
                    if (timer_seconds == 0):
                        text = check_end_game (
                            players, 
                            background_index,
                            tie_checks[0]
                        )
                        if (text != None):
                            if (isinstance (text[-1], list)):
                                tie_checks = [
                                    True, 
                                    text,
                                    time ()
                                ]
                                texts.append (text[0])
                                timer_paused = True
                                
                            else:
                                move_screen = text[-1]
                                timer_paused = True
                                for text_item in text[:-1]:
                                    texts.append (text_item)          

                time_recorded = time ()
                texts[0].set_text (get_time (timer_minutes, timer_seconds))

        # ----------------------------
        #   Check for event updates.
        # ----------------------------
        for event in pygame.event.get ():
            if (event.type == pygame.QUIT):
                run = False

            # ----------------------------------
            #   Process all player key events.
            # ----------------------------------
            for player in players:
                player.key_event (event)

        # --------------------------------------
        #   Run game checks and player checks.
        # --------------------------------------
        attacks = attack (players, attacks)
        collision (players, attacks, platforms)

        for player in players:
            player.move_character (player.get_offset ())
            player.run_checks ()

            # --------------------------------
            #   If a player is dead check to 
            #    see if there is a winner.
            # --------------------------------
            if (player.is_dead () and move_screen == 0):
                text = check_end_game (
                    players,
                    background_index,
                    tie_checks[0]
                )
                if (text != None):
                    if (isinstance (text[-1], list) == False):
                        move_screen = text[-1]
                        timer_paused = True
                        for text_item in text[:-1]:
                            texts.append (text_item)


        # ------------------------
        #   Sudden death checks.
        # ------------------------
        if (tie_checks[0]):
            if (time () - tie_checks[2] > tie_checks[1][1][0]):
                if (not tie_checks[1][1][1]):
                    texts.remove (tie_checks[1][0])
                    for player in players:
                        player.allow_movement ()
                    
                    timer_minutes = tie_checks[1][1][2]
                    timer_seconds = tie_checks[1][1][3]
                    timer_paused = False
                    tie_checks[1][1][1] = True
                

        # --------------------
        #   Draw the window.
        # --------------------
        attacks = draw_window (
            win, 
            players, 
            attacks, 
            platforms, 
            background=background,
            texts=texts
        )


if (__name__ == "__main__"):
    main ()