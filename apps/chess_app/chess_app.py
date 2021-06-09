from apps.chess_app.objects.board import Board
from apps.chess_app.objects.bar_menu import BarMenu
from apps.chess_app.objects.clock import Clock

from tkinter import *
import string
import os
import csv
from tkinter import ttk


class ChessApp(Tk):
    """Window container for game objects"""
    def __init__(self, mode):
        Tk.__init__(self, mode)

        # The game mode and the path for this chess app settings and files, shown in these variables
        self.mode = mode
        # (get rid of after removing from Board class)
        self.chess_path = os.getcwd() + '\\apps\\chess_app'

        # -------------APP_ATTRIBUTES-------------
        # self.resizable(0, 0)
        self.title('CHESS_GRAND_MASTER')
        self.protocol('WM_DELETE_WINDOW', self.end_new_game)
        self.configure(menu=BarMenu(self).menu_bar)

        # -------------BOARD FRAME(LEFT)-------------
        # frame for the chess board
        self.board_frame = Frame(self)
        self.board_frame.pack(side=LEFT)

        # Widgets frame, here is where all the objects apart from the chess board are placed
        self.widgets_frame = Frame(self)

        # Actual game board (we pass the 'widgets frame' instance to be able to update chess notation in real time)
        self.main_chess_board = Board(self.board_frame, self.widgets_frame)
        self.main_chess_board.grid(row=1, column=1)

        # -------------WIDGETS(right)-------------
        # CLOCK (doesn't update)
        self.clock_frame = LabelFrame(self)
        self.clock_frame.pack()
        self.clock = Clock(self.clock_frame)
        self.clock.pack()

        # We can now place the widgets frame
        self.widgets_frame.pack()

        # Place the required box widgets
        self.place_player_stats_and_settings(mode)

        # Don't uncomment this, the countdown works, but it makes the screen lag for some reason
        # self.clock.startCountdown()

    def place_player_stats_and_settings(self, mode):
        """Placing stats and settings boxes"""

        if mode == 'guest':
            # if mode is guest

            # ----------------SETTINGS-----------------
            # get default game settings
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)
                for row in reader:
                    difficulty = row[0]
                    game_type = row[2]
                    player_piece_color = row[3]
                    opponent_piece_color = row[4]
                    self.the_border_color = row[5]

            # --------------GAME STATISTICS BOX----------------
            # box that contains game state data retrieved from settings
            game_stats_frame = LabelFrame(self.widgets_frame, text='Game data', width=320, height=120)
            game_stats_frame.pack(pady=(15, 0))

            # - DATA
            # Difficulty (first row)
            Label(game_stats_frame, text=f'Difficulty:') \
                .grid(column=0, row=0, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{difficulty.upper()}', font='verdana 7 bold') \
                .grid(column=1, row=0, padx=(0, 2), pady=3)

            # Game type (second row)
            Label(game_stats_frame, text=f'Game type:') \
                .grid(column=0, row=1, padx=(5, 0))
            Label(game_stats_frame, text=f'{game_type.upper()}', font='verdana 7 bold') \
                .grid(column=1, row=1, padx=(0, 2))

            # Player_1 piece color (first row)
            Label(game_stats_frame, text=f'Player_1 piece color:') \
                .grid(column=2, row=0, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{player_piece_color.upper()}', font='verdana 7 bold') \
                .grid(column=3, row=0, padx=(0, 2))

            # Player_2 piece color (second row)
            Label(game_stats_frame, text=f'Player_2 piece color:') \
                .grid(column=2, row=1, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{opponent_piece_color.upper()}', font='verdana 7 bold') \
                .grid(column=3, row=1, padx=(0, 2))

            # --------------USER STATISTICS BOX----------------
            # Since the game mode is guest, we show the word 'GUEST' in capital letters and nothing else in this section
            player_stats_frame = LabelFrame(self.widgets_frame, text='Player history', width=320, height=180)
            player_stats_frame.pack(pady=(30, 0))
            Label(player_stats_frame, text='GUEST', font='verdana 30 bold').pack(pady=50, padx=80)

            # PLacing the chess board borders
            self.place_board_coordinates(self.the_border_color)

        if mode == 'user':
            # if the game mode is user
            # --------------PLAYER_SETTINGS----------------
            # retrieve the settings for this user
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)
                for row in reader:
                    difficulty = row[0]
                    game_type = row[2]
                    player_piece_color = row[3]
                    opponent_piece_color = row[4]
                    self.the_border_color = row[5]

            # ----------------GAME_STATISTICS_BOX----------------
            # contains game state data retrieved from the user settings
            # which retrieves data from the settings file
            game_stats_frame = LabelFrame(self.widgets_frame, text='Game data', width=320, height=120)
            game_stats_frame.pack(pady=(15, 0))

            # - DATA
            # Difficulty (first row)
            Label(game_stats_frame, text=f'Difficulty:') \
                .grid(column=0, row=0, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{difficulty.upper()}', font='verdana 7 bold') \
                .grid(column=1, row=0, padx=(0, 2), pady=3)

            # Game type (second row)
            Label(game_stats_frame, text=f'Game type:') \
                .grid(column=0, row=1, padx=(5, 0))
            Label(game_stats_frame, text=f'{game_type.upper()}', font='verdana 7 bold') \
                .grid(column=1, row=1, padx=(0, 2))

            # Player_1 piece color (first row)
            Label(game_stats_frame, text=f'Player_1 piece color:') \
                .grid(column=2, row=0, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{player_piece_color.upper()}', font='verdana 7 bold') \
                .grid(column=3, row=0, padx=(0, 2))

            # Player_2 piece color (second row)
            Label(game_stats_frame, text=f'Player_2 piece color:') \
                .grid(column=2, row=1, padx=(5, 0), pady=3)
            Label(game_stats_frame, text=f'{opponent_piece_color.upper()}', font='verdana 7 bold') \
                .grid(column=3, row=1, padx=(0, 2))

            # ------------USER_STATISTICS--------------
            # We first retrieve the user stats
            with open(os.getcwd() + '//apps//chess_app//all_settings//user//user_stats.csv') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)  # skip header
                for row in reader:
                    # the row is a list containing the data
                    self.number_of_games_played = row[0]
                    self.wins = row[1]
                    self.loses = row[2]
                    self.draws = row[3]
                    self.ranking = row[4]

            # We get the name for this current user
            with open(os.getcwd() + '//apps//login_system_app//temp//current_user.txt', 'r') as f:
                username = f.read()

            # Create the frame
            player_stats_frame = LabelFrame(self.widgets_frame, text='Player history', width=320, height=180)
            player_stats_frame.pack(pady=(18, 0))

            # Place the username as a title at the top of the box frame
            Label(player_stats_frame, text=username, font='verdana 15 bold') \
                .grid(row=0, columnspan=5, padx=20, pady=5)
            ttk.Separator(player_stats_frame, orient='horizontal').grid(row=1, column=0, columnspan=5, sticky='we')

            # - DATA
            # number of games played
            Label(player_stats_frame, text='Number_of_games_played: ', font='calibri 10') \
                .grid(column=0, row=2)
            Label(player_stats_frame, text=self.number_of_games_played, font='verdana 10 bold') \
                .grid(column=1, row=2, padx=(0, 28))

            # wins
            Label(player_stats_frame, text='Wins: ', font='calibri 10') \
                .grid(column=2, row=2, padx=(15, 0))
            Label(player_stats_frame, text=self.wins, font='verdana 10 bold') \
                .grid(column=3, row=2, padx=(0, 25))

            # loses
            Label(player_stats_frame, text='Loses: ', font='calibri 10') \
                .grid(column=0, row=3)
            Label(player_stats_frame, text=self.number_of_games_played, font='verdana 10 bold') \
                .grid(column=1, row=3, padx=(0, 28))

            # draws
            Label(player_stats_frame, text='Draws: ', font='calibri 10') \
                .grid(column=2, row=3, padx=(15, 0))
            Label(player_stats_frame, text=self.draws, font='verdana 10 bold') \
                .grid(column=3, row=3, padx=(0, 25))

            # PLacing the chess board borders
            self.place_board_coordinates(self.the_border_color)

    def place_board_coordinates(self, color):
        """Coordinates for chess board labels in borders"""

        # A list strings containing the letters from a to h (for the upper and lower row)
        letters = string.ascii_lowercase[:8]
        # A list of numbers from 1 to 8 (for the left and right side)
        nums = list(range(1, 9))

        # Upper row(letters, a-h)
        high_row_of_letters = Frame(self.board_frame, bg=color)
        high_row_of_letters.grid(row=0, column=1)
        for i in range(8):
            # Place all the letter in the upper row
            Label(high_row_of_letters, text=letters[i], bg=color, fg='white', width=8)\
                .pack(side=LEFT, padx=3)

        # Lower row(letters, a-h)
        lower_row_of_letters = Frame(self.board_frame, bg=color)
        lower_row_of_letters.grid(row=2, column=1)
        for i in range(8):
            # place all the letters in the lower row
            Label(lower_row_of_letters, text=letters[i], bg=color, fg='white', width=8)\
                .pack(side=LEFT, padx=3)

        # Left column(numbers, 1-8)
        left_row_of_numbers = Frame(self.board_frame, bg=color)
        left_row_of_numbers.grid(row=1, column=0)
        for i in range(8):
            # Place all the numbers
            Label(left_row_of_numbers, text=nums[i], bg=color, fg='white', height=4, width=2)\
                .pack(pady=1)

        # Right column(numbers, 1-8)
        right_row_of_numbers = Frame(self.board_frame, bg=color)
        right_row_of_numbers.grid(row=1, column=2)
        # Place all the numbers
        for i in range(8):
            Label(right_row_of_numbers, text=nums[i], bg=color, fg='white', height=4, width=2)\
                .pack(pady=1)

    def end_new_game(self):
        # Set start_new_game to false, so the game loop can be ended
        with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no')

        self.destroy()
