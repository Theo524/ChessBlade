from tkinter import *
from tkinter import ttk, messagebox
import os
import sqlite3


class Settings(Tk):
    def __init__(self):
        Tk.__init__(self)

        # attributes
        self.title('Settings')
        self.resizable(0, 0)

        # All the game settings will be contained within this notebook
        notebook = ttk.Notebook(self)
        notebook.pack()

        # tabs
        # Place the custom frame classes I made previously
        # general settings
        self.general_settings = GeneralSettings(notebook)
        self.general_settings.pack(pady=10, expand=True, fill=BOTH)
        # customization settings
        self.customization_settings = CustomizationSettings(notebook)
        self.customization_settings.pack(pady=10, expand=True, fill=BOTH)

        # Button which allows to apply the settings made (saves settings to file)
        apply_settings_button = ttk.Button(self, text='Apply settings', command=self.save_settings)
        apply_settings_button.pack(padx=(190, 0), pady=5)

        # add notebook tabs
        notebook.add(self.general_settings, text='General')
        notebook.add(self.customization_settings, text='Customization')

    def save_settings(self):
        """Saves settings too file"""

        # Retrieving settings from the classes
        self.difficulty = self.general_settings.get_difficulty()
        self.time = self.general_settings.get_time()
        self.game_type = self.general_settings.get_gamemode()
        self.player_color = self.customization_settings.get_piece_color()

        if self.player_color == 'black':
            self.opponent_color = 'white'
        else:
            self.opponent_color = 'black'

        self.border_color = self.customization_settings.get_border_color()
        self.board_color = self.customization_settings.get_board_color()

        # get game mode
        with open(os.getcwd() + '\\apps\\login_system_app\\temp\\mode.txt', 'r') as f:
            game_mode = f.read()

        # Confirmation message
        confirm = messagebox.askyesno('Confirmation', 'Are you sure you want to apply these settings?')
        # if the user accepts, store settings, show informative feedback and destroy settings window
        if confirm:
            print(f'{self.difficulty}-{self.time}-{self.game_type}-{self.player_color}-{self.opponent_color}'
                            f'-{self.border_color}-{self.board_color}')
            # if user is in guest mode, apply new settings to system
            if game_mode == 'guest':
                with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'w') as f:
                    f.write('Game_difficulty, time, game_mode, player_piece_color, opponent_piece_color, border_color,'
                            'board_color\n')
                    f.write(f'{self.difficulty}-{self.time}-{self.game_type}-{self.player_color}-{self.opponent_color}'
                            f'-{self.border_color}-{self.board_color}')

            # if user is in user mode, apply new settings to user account
            if game_mode == 'user':
                # apply changes to db
                self.apply_settings_user_db()
                # save the new settings in a file
                with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\user\\user_game_settings.csv', 'w') as f:
                    f.write('Game_difficulty-time-game_mode-player_piece_color-opponent_piece_color-border_color-'
                            'board_color\n')
                    f.write(f'{self.difficulty}-{self.time}-{self.game_type}-{self.player_color}-{self.opponent_color}'
                            f'-{self.border_color}-{self.board_color}')

            # Confirmation and informative feedback
            messagebox.showinfo('Success', 'Settings successfully saved. Start a new game to play with new settings.')
            # destroy settings window
            self.destroy()
        else:
            pass

    def apply_settings_user_db(self):
        """Apply settings to the user database"""

        # get the username
        with open(os.getcwd() + '\\apps\\login_system_app\\temp\\current_user.txt', 'r') as f:
            username = f.read()

        # Open the sql database and retrieve all the data this user has
        # All usernames in the sql file are unique so there won't be any problems
        conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
        c = conn.cursor()

        with conn:
            # update all user stats
            c.execute("UPDATE user_settings SET "
                      "difficulty = :game_difficulty AND "
                      "time = :time AND "
                      "game_type = :game_type AND "
                      "player_piece_color = :player_piece_color AND "
                      "opponent_piece_color = :opponent_piece_color AND "
                      "border_color = :border_color AND "
                      "board_color = :board_color "
                      "WHERE user=:user",
                      {'game_difficulty': self.difficulty,
                       'time': self.time,
                       'game_type': self.game_type,
                       'player_piece_color': self.player_color,
                       'opponent_piece_color': self.opponent_color,
                       'border_color': self.border_color,
                       'board_color': self.board_color,
                       'user': username})

    def reset(self):
        """Default settings values"""

        self.general_settings.difficulty_var.set(1)
        self.general_settings.gamemode_var.set(1)
        self.customization_settings.border_color_var.set('black')
        self.customization_settings.player_color_var.set('black')
        self.customization_settings.board_color_var.set('brown')


class GeneralSettings(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # --------------DIFFICULTY--------------
        difficulty_frame = ttk.LabelFrame(self, text="Difficulty")
        difficulty_frame.pack(fill="both", expand="yes", pady=5, padx=5)

        # we store the difficulty here
        self.difficulty_var = IntVar()

        # novice button
        novice = ttk.Radiobutton(difficulty_frame,
                                 text="Novice",
                                 variable=self.difficulty_var,
                                 value=1,
                                 command=self.get_difficulty)
        novice.pack(side=LEFT)

        # intermediate button
        intermediate = ttk.Radiobutton(difficulty_frame,
                                       text="Intermediate",
                                       variable=self.difficulty_var,
                                       value=2,
                                       command=self.get_difficulty)
        intermediate.pack(side=LEFT)

        # expert button
        expert = ttk.Radiobutton(difficulty_frame,
                                 text="Expert",
                                 variable=self.difficulty_var,
                                 value=3,
                                 command=self.get_difficulty)
        expert.pack(side=LEFT)

        # Set default to 1 (novice)
        self.difficulty_var.set(1)

        # --------------TIME--------------
        time_frame = ttk.LabelFrame(self, text="Time")
        time_frame.pack(fill="both", expand="yes", pady=5, padx=5)

        # variables
        self.time_in_hours = StringVar(value=2)
        self.time_in_minutes = StringVar(value=30)
        self.time_in_seconds = StringVar(value=0)

        # hours entry
        Label(time_frame, text='Hours').pack(side=LEFT)
        time_limit_hours = ttk.Spinbox(time_frame, width=3, from_=0, to=2, textvariable=self.time_in_hours, wrap=True)
        time_limit_hours.pack(side=LEFT, padx=3)

        # minutes entry
        Label(time_frame, text='Minutes').pack(side=LEFT)
        time_limit_minutes = ttk.Spinbox(time_frame, width=3, from_=0, to=60, textvariable=self.time_in_minutes,
                                         wrap=True)
        time_limit_minutes.pack(side=LEFT, padx=3)

        # seconds entry
        Label(time_frame, text='Seconds').pack(side=LEFT)
        time_limit_seconds = ttk.Spinbox(time_frame, width=3, from_=0, to=60, textvariable=self.time_in_seconds,
                                         wrap=True)
        time_limit_seconds.pack(side=LEFT, padx=3)

        # --------------GAME_TYPE--------------
        gamemode_frame = ttk.LabelFrame(self, text='Game mode')
        gamemode_frame.pack(fill="both", expand="yes", pady=5, padx=5)
        self.gamemode_var = IntVar()

        # Two player mode
        two_player = ttk.Radiobutton(gamemode_frame,
                                     text='Two player',
                                     variable=self.gamemode_var,
                                     value=1,
                                     command=self.get_gamemode)
        two_player.pack(side=LEFT, padx=(5, 50))

        # vs computer (AI) mode
        computer = ttk.Radiobutton(gamemode_frame,
                                   text='Computer',
                                   variable=self.gamemode_var,
                                   value=2,
                                   command=self.get_gamemode)
        computer.pack(side=LEFT)
        # set default game mode to 'two player'
        self.gamemode_var.set(1)

    def get_difficulty(self):
        """Get difficulty"""

        if self.difficulty_var.get() == 1:
            return 'easy'
        elif self.difficulty_var.get() == 2:
            return 'medium'
        elif self.difficulty_var.get() == 3:
            return 'hard'

    def get_time(self):
        """Get time"""

        # All the time fractions
        all_time = [self.time_in_hours.get()] + [self.time_in_minutes.get()] + [self.time_in_seconds.get()]
        new = []

        # Format the time
        # Converting all 1 digit number to 2 digit, e.g. '1' to '01'
        for i in all_time:
            if len(i) == 1:
                substitute = i.replace(i, f'0{i}')
                new.append(substitute)
            else:
                new.append(i)

        #  final string in format hh:mm:ss
        full_str = f'{new[0]}:{new[1]}:{new[2]}'

        return full_str

    def get_gamemode(self):
        """Get game mode"""

        if self.gamemode_var.get() == 1:
            return 'two player'
        elif self.gamemode_var.get() == 2:
            return 'computer'


class CustomizationSettings(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # --------------PLAYER_COLOR--------------
        player_color_frame = ttk.LabelFrame(self, text='User piece color')
        player_color_frame.pack(fill="both", pady=5, padx=5)

        # variables to store color val
        self.player_color_var = IntVar()

        # Black button
        black = ttk.Radiobutton(player_color_frame,
                                text='black',
                                variable=self.player_color_var,
                                value=1,
                                command=self.get_piece_color)
        black.pack(side=LEFT, padx=(5, 50))

        # White button
        white = ttk.Radiobutton(player_color_frame,
                                text='white',
                                variable=self.player_color_var,
                                value=0,
                                command=self.get_piece_color)
        white.pack(side=LEFT)

        # ----------------BORDER_COLORS-----------------
        border_color_frame = ttk.LabelFrame(self, text='Border colors')
        border_color_frame.pack(fill="both", pady=5, padx=5)

        Label(border_color_frame, text='Chose border color').pack(side=LEFT, padx=5)

        # variable
        self.border_color_var = StringVar()

        self.border_colors = ttk.Combobox(border_color_frame, textvariable=self.border_color_var, width=10)
        self.border_colors.set('black')
        # color options
        self.border_colors['values'] = ('black', 'brown', 'green', 'purple', 'blue')
        self.border_colors.pack(pady=(0, 6))

        # ----------------BOARD_COLORS-----------------
        board_color_frame = ttk.LabelFrame(self, text='Board colors')
        board_color_frame.pack(fill="both", pady=5, padx=5)

        Label(board_color_frame, text='Chose board color').pack(side=LEFT, padx=5)

        # variable
        self.board_color_var = StringVar()

        self.board_colors = ttk.Combobox(board_color_frame, textvariable=self.board_color_var, width=10)
        self.board_colors.set('brown')
        # color options
        self.board_colors['values'] = ('black',  'brown', 'green', 'purple', 'blue')
        self.board_colors.pack(pady=(0, 6))

    def get_piece_color(self):
        """Get the piece color"""
        if self.player_color_var.get() == 0:
            return 'white'

        elif self.player_color_var.get() == 1:
            return 'black'

    def get_board_color(self):
        """Get the board color"""
        return self.board_colors.get()

    def get_border_color(self):
        """Get the border color"""
        return self.border_colors.get()

