from tkinter import *
from tkinter import ttk, messagebox, colorchooser
import os
from app.resources.database.database import SQLite3DatabaseBrowser
import csv


class Settings(Toplevel):
    def __init__(self, master, mode):
        Toplevel.__init__(self, master)

        self.master = master
        self.mode = mode

        # attributes
        self.lift(master)
        self.title('Settings')
        self.resizable(0, 0)
        self.protocol('WM_DELETE_WINDOW', self.confirm_exit)
        scene = Frame(self, )
        scene.pack(padx=10, pady=5)

        # All the game settings will be contained within this notebook
        notebook = ttk.Notebook(scene)
        notebook.pack(pady=(0, 5))

        # tabs
        # Place the custom frame classes I made previously
        # general settings
        self.general_settings = GeneralSettings(notebook)
        self.general_settings.pack(pady=10, expand=True, fill=BOTH)

        # Access to customization settings is only available as a user
        # customization settings
        self.customization_settings = CustomizationSettings(notebook)
        self.customization_settings.pack(pady=10, expand=True, fill=BOTH)

        # Button which allows to apply the settings made (saves settings to file)
        apply_settings_button = ttk.Button(scene, text='Apply settings', command=self.save_settings)
        apply_settings_button.pack(side=RIGHT)

        # add notebook tabs
        notebook.add(self.general_settings, text='General')
        notebook.add(self.customization_settings, text='Customization')

        # fill user settings
        self.auto_fill()

    def save_settings(self):
        """Saves settings too file"""
        requirements_not_met = 0

        # Retrieving settings data from the classes
        difficulty = self.general_settings.get_difficulty()
        if type(difficulty) != str or len(difficulty) < 1:
            requirements_not_met += 1

        game_type = self.general_settings.get_gamemode()
        if type(game_type) != str or len(game_type) < 1:
            requirements_not_met += 1

        player_color = self.customization_settings.get_piece_color()
        if player_color not in ['black', 'white']:
            requirements_not_met += 1

        border_color = self.customization_settings.get_border_color()
        if type(border_color) != str or len(border_color) < 1:
            requirements_not_met += 1

        board_color = self.customization_settings.get_board_color()
        if type(board_color) != str or len(board_color) < 1:
            requirements_not_met += 1

        piece_format = self.customization_settings.get_piece_format()
        if type(piece_format) != str or len(piece_format) < 1:
            requirements_not_met += 1

        # Confirmation message
        confirm = messagebox.askyesno('Confirmation', 'Are you sure you want to apply these settings?')
        # if the user accepts, store settings, show informative feedback and destroy settings window
        if confirm:
            # first check there are no empty fields
            if requirements_not_met == 0:
                # if user is in guest mode, apply new settings to system
                if self.mode == 'guest':
                    with open(os.getcwd() + '\\app\\temp\\chess_temp\\all_settings\\guest\\default_game_settings.csv', 'w')\
                            as f:
                        f.write('Game_difficulty-game_mode-player_piece_color-border_color-board_color-piece_format\n')
                        f.write(f'{difficulty}-{game_type}-{player_color}-{border_color}-{board_color}-{piece_format}')

                    # also set second read so that settings are saved on device
                    with open(os.getcwd() + '\\app\\temp\\chess_temp\\all_settings\\guest\\settings_saved.txt', 'w') as f:
                        f.write('y')

                    # Confirmation and informative feedback
                    messagebox.showinfo('Success', 'Settings successfully saved.'
                                                   ' Click  \'New game\' in the game menu '
                                                   'to play with these new settings.')

                # if user is in user mode, apply new settings to user account
                if self.mode == 'user':
                    # data
                    data = [difficulty, game_type, player_color, border_color, board_color, piece_format]

                    # apply changes to db
                    self.apply_settings_user_db(data)
                    # save the new settings in a file
                    with open(os.getcwd() + '\\app\\temp\\chess_temp\\all_settings\\user\\user_game_settings.csv', 'w') as f:
                        f.write('Game_difficulty-game_mode-player_piece_color-border_color-board_color-piece_format\n')
                        f.write(f'{difficulty}-{game_type}-{player_color}-{border_color}-{board_color}-{piece_format}')

                    # ensure the user does not leave if playing vs ai
                    game_type = self.master.main_chess_board.game_type
                    if game_type == 'computer':
                        # Confirmation and informative feedback
                        messagebox.showinfo('Success', 'Settings successfully saved. It has been detected that you are'
                                                       ' playing against the ai. If you start a new game to play'
                                                       ' with the new settings this game will be counted as a '
                                                       'defeat in your account.')
                    else:
                        # Confirmation and informative feedback
                        messagebox.showinfo('Success', 'Settings successfully saved.'
                                                       ' Click  \'New game\' in the game menu '
                                                       'to play with these new settings.')
                # destroy settings window
                self.destroy()
            else:
                messagebox.showerror('Error', f'You left {requirements_not_met} empty field(s)')

        else:
            pass

    @staticmethod
    def apply_settings_user_db(data):
        """Apply settings to the user database"""

        # get the username
        with open(os.getcwd() + '\\app\\temp\\login_temp\\current_user_id.txt', 'r') as f:
            user_id = int(f.read())

        # data to be saved
        data = [data[0], data[1], data[2], data[3], data[4], data[5]]

        # save user settings to database
        SQLite3DatabaseBrowser.save(save='settings', user_id=user_id, data=data)

    def confirm_exit(self):
        """Confirms whether user wants to exit window"""

        confirm = messagebox.askyesno('Error', 'Are you sure you want to exit?\nAll settings will be lost!')
        if confirm:
            self.destroy()

    def auto_fill(self):
        """Automatically fill fields based on player settings"""

        if self.mode == 'guest':
            with open(os.getcwd() + '\\app\\temp\\chess_temp\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    # print(f'Guest settings : {row}')
                    # retrieve settings in file
                    # difficulty
                    if row[0] == 'Novice':
                        self.general_settings.difficulty_var.set(1)
                    if row[0] == 'Intermediate':
                        self.general_settings.difficulty_var.set(2)
                    if row[0] == 'Expert':
                        self.general_settings.difficulty_var.set(3)

                    # game type
                    if row[1] == 'two_player':
                        self.general_settings.gamemode_var.set(1)
                    if row[1] == 'computer':
                        self.general_settings.gamemode_var.set(2)

                    # player piece color
                    if row[2] == 'black':
                        self.customization_settings.player_color_var.set(1)
                    if row[2] == 'white':
                        self.customization_settings.player_color_var.set(2)

                    # border color var and combobox
                    self.customization_settings.border_colors.set(row[3])
                    self.customization_settings.border_color_var.set(row[3])

                    # board colors
                    self.customization_settings.board_color_var.set(row[4])

                    # piece format
                    if row[5] == 'spatial':
                        self.customization_settings.piece_format_var.set(1)
                    if row[5] == 'default':
                        self.customization_settings.piece_format_var.set(2)
                    if row[5] == 'spatial':
                        self.customization_settings.piece_format_var.set(3)

        if self.mode == 'user':
            with open(os.getcwd() + '\\app\\temp\\chess_temp\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    # print(f'User settings : {row}')
                    # retrieve settings in file
                    # difficulty
                    if row[0] == 'Novice':
                        self.general_settings.difficulty_var.set(1)
                    if row[0] == 'Intermediate':
                        self.general_settings.difficulty_var.set(2)
                    if row[0] == 'Expert':
                        self.general_settings.difficulty_var.set(3)

                    # game type
                    if row[1] == 'two_player':
                        self.general_settings.gamemode_var.set(1)
                    if row[1] == 'computer':
                        self.general_settings.gamemode_var.set(2)

                    # player piece color
                    if row[2] == 'black':
                        self.customization_settings.player_color_var.set(1)
                    if row[2] == 'white':
                        self.customization_settings.player_color_var.set(2)

                    # border color var and combobox
                    self.customization_settings.border_colors.set(row[3])
                    self.customization_settings.border_color_var.set(row[3])

                    # board colors
                    self.customization_settings.board_color_var.set(row[4])

                    # piece format
                    if row[5] == 'spatial':
                        self.customization_settings.piece_format_var.set(1)
                    if row[5] == 'default':
                        self.customization_settings.piece_format_var.set(2)
                    if row[5] == 'spatial':
                        self.customization_settings.piece_format_var.set(3)


class GeneralSettings(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        scene = Frame(self, height=5, width=100)
        scene.pack()

        # --------------DIFFICULTY--------------
        difficulty_frame = ttk.LabelFrame(scene, text="Difficulty")
        difficulty_frame.pack(fill="both", expand="yes", padx=5, pady=5)

        # we store the difficulty here
        self.difficulty_var = IntVar()

        # novice button
        novice = ttk.Radiobutton(difficulty_frame,
                                 text="Novice",
                                 variable=self.difficulty_var,
                                 value=1,
                                 command=self.get_difficulty)
        novice.pack(side=LEFT, padx=10)

        # intermediate button
        intermediate = ttk.Radiobutton(difficulty_frame,
                                       text="Intermediate",
                                       variable=self.difficulty_var,
                                       value=2,
                                       command=self.get_difficulty)
        intermediate.pack(side=LEFT, padx=5)

        # expert button
        expert = ttk.Radiobutton(difficulty_frame,
                                 text="Expert",
                                 variable=self.difficulty_var,
                                 value=3,
                                 command=self.get_difficulty)
        expert.pack(side=LEFT, padx=10)

        # --------------GAME_TYPE--------------
        gamemode_frame = ttk.LabelFrame(scene, text='Game mode')
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

    def get_difficulty(self):
        """Get difficulty"""

        if self.difficulty_var.get() == 1:
            return 'Novice'
        elif self.difficulty_var.get() == 2:
            return 'Intermediate'
        elif self.difficulty_var.get() == 3:
            return 'Expert'

    def get_gamemode(self):
        """Get game mode"""

        if self.gamemode_var.get() == 1:
            return 'two_player'
        elif self.gamemode_var.get() == 2:
            return 'computer'


class CustomizationSettings(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        scene = Frame(self, height=5, width=100)
        scene.pack()

        # --------------PLAYER_COLOR--------------
        player_color_frame = ttk.LabelFrame(scene, text='User piece color')
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
                                value=2,
                                command=self.get_piece_color)
        white.pack(side=LEFT)

        # this way it is set to none
        self.player_color_var.set(0)

        # ----------------BORDER_COLORS-----------------
        border_color_frame = ttk.LabelFrame(scene, text='Border colors')
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
        board_color_frame = ttk.LabelFrame(scene, text='Board colors')
        board_color_frame.pack(fill="both", pady=5, padx=5)

        Label(board_color_frame, text='Chose board color').pack(side=LEFT, padx=5)

        # variable
        self.board_color_var = StringVar()

        board_color_button = Button(board_color_frame, text="Select board color", command=self.set_board_color)
        board_color_button.pack(side=LEFT, pady=(0, 6), padx=(15, 0))

        # --------------PIECE FORMAT--------------
        piece_format_frame = ttk.LabelFrame(scene, text="Piece format")
        piece_format_frame.pack(fill="both", expand="yes", padx=5, pady=5)

        # we store the difficulty here
        self.piece_format_var = IntVar()

        # spatial button
        spatial = ttk.Radiobutton(piece_format_frame,
                                  text="Spatial",
                                  variable=self.piece_format_var,
                                  value=1,
                                  command=self.get_piece_format)
        spatial.pack(side=LEFT, padx=10)

        # default button
        default = ttk.Radiobutton(piece_format_frame,
                                  text="Default",
                                  variable=self.piece_format_var,
                                  value=2,
                                  command=self.get_piece_format)
        default.pack(side=LEFT, padx=5)

        # fantasy button
        fantasy = ttk.Radiobutton(piece_format_frame,
                                  text="Fantasy",
                                  variable=self.piece_format_var,
                                  value=3,
                                  command=self.get_piece_format)
        fantasy.pack(side=LEFT, padx=10)

    def get_piece_color(self):
        """Get the piece color"""
        if self.player_color_var.get() == 2:
            return 'white'

        elif self.player_color_var.get() == 1:
            return 'black'

    def set_board_color(self):
        """Chose a color for the board"""

        board_color_code = colorchooser.askcolor(title="Choose a board color")
        self.board_color_var.set(board_color_code[1])

    def get_board_color(self):
        """Get the board color from colorchoser widget"""

        return self.board_color_var.get()

    def get_border_color(self):
        """Get the border color"""
        return self.border_colors.get()

    def get_piece_format(self):
        """Get the piece color"""
        if self.piece_format_var.get() == 1:
            return 'spatial'

        if self.piece_format_var.get() == 2:
            return 'default'

        if self.piece_format_var.get() == 3:
            return 'fantasy'
