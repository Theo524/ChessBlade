from apps.chess_app.objects.board import Board
from apps.chess_app.objects.bar_menu import BarMenu
from apps.chess_app.objects.clock import Clock

from tkinter import *
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
        self.title('Chess by theo')
        self.protocol('WM_DELETE_WINDOW', self.end_new_game)
        menu = BarMenu(self)
        self.configure(menu=menu)

        # -------------BOARD FRAME(LEFT)-------------
        # frame for the chess board
        if mode == 'guest':
            # get board background color for guest mode
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)
                for row in reader:
                    self.the_border_color = row[5]
                    self.board_color = row[6]

        if mode == 'user':
            # get board background color for user mode
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)
                for row in reader:
                    print(row)
                    self.the_border_color = row[5]
                    self.board_color = row[6]

        # -------------everything contained here--------------
        self.game_frame = Frame(self)
        self.game_frame.pack(side=TOP)

        # Frame for board
        self.board_frame = Frame(self.game_frame)
        self.board_frame.pack(side=LEFT)

        # Widgets frame, here is where all the objects apart from the chess board are placed
        self.widgets_frame = Frame(self.game_frame)

        # clock temp
        self.clock_frame = LabelFrame(self.widgets_frame)
        self.clock_frame.pack(ipadx=30)
        self.temp = Label(self.clock_frame, text='time goes here', font='calibri 20')
        self.temp.pack()

        # Actual game board
        # It is inside the board frame
        # (we pass the 'widgets frame' instance to be able to create and update chess notation in real time)
        self.main_chess_board = Board(self.board_frame, widgets_frame=self.widgets_frame)
        self.main_chess_board.pack()
        # creates board
        self.main_chess_board.build()

        # -------------WIDGETS(right)-------------
        # CLOCK (doesn't update)
        #self.clock = Clock(self.clock_frame)
        #self.clock.pack()

        # We can now place the widgets frame
        self.widgets_frame.pack(side=LEFT, padx=20)

        # Place the required box widgets
        self.place_player_stats_and_settings(mode)

        # clock frame goes at the bottom

        # Don't uncomment this, the countdown works, but it makes the screen lag for some reason
        # self.clock.startCountdown()

    def place_player_stats_and_settings(self, mode):
        """Placing stats and settings boxes"""

        if mode == 'guest':
            # if mode is guest

            # ----------------SETTINGS-----------------
            # default game settings

            # --------------USER STATISTICS BOX----------------
            # Since the game mode is guest, we show the word 'GUEST' in capital letters and nothing else in this section
            player_stats_frame = LabelFrame(self.widgets_frame, text='Player history', width=320, height=180)
            player_stats_frame.pack(pady=5)
            Label(player_stats_frame, text='GUEST', font='verdana 30 bold').pack(pady=50, padx=80)

            # PLacing the chess board borders
            #self.place_board_coordinates(self.the_border_color)

        if mode == 'user':
            # if the game mode is user
            # --------------PLAYER_SETTINGS----------------
            # retrieve the settings for this user

            # ------------USER_STATISTICS--------------
            # We first retrieve the user stats
            with open(os.getcwd() + '//apps//chess_app//all_settings//user//user_stats.csv') as f:
                reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
                next(reader)  # skip header
                for row in reader:
                    # the row is a list containing the data
                    number_of_games_played = row[0]
                    wins = row[1]
                    loses = row[2]
                    draws = row[3]
                    ranking = row[4]

            # We get the name for this current user
            with open(os.getcwd() + '//apps//login_system_app//temp//current_user.txt', 'r') as f:
                username = f.read()

            # Create the frame
            player_stats_frame = LabelFrame(self.widgets_frame, text='Player history', width=320, height=180)
            player_stats_frame.pack(pady=5)

            # Place the username as a title at the top of the box frame
            Label(player_stats_frame, text=username, font='verdana 15 bold') \
                .grid(row=0, columnspan=5, padx=20, pady=5)
            ttk.Separator(player_stats_frame, orient='horizontal').grid(row=1, column=0, columnspan=5, sticky='we')

            # - DATA
            # number of games played
            Label(player_stats_frame, text='Number_of_games_played: ', font='calibri 10') \
                .grid(column=0, row=2)
            Label(player_stats_frame, text=number_of_games_played, font='verdana 10 bold') \
                .grid(column=1, row=2, padx=(0, 28))

            # wins
            Label(player_stats_frame, text='Wins: ', font='calibri 10') \
                .grid(column=2, row=2, padx=(15, 0))
            Label(player_stats_frame, text=wins, font='verdana 10 bold') \
                .grid(column=3, row=2, padx=(0, 25))

            # loses
            Label(player_stats_frame, text='Loses: ', font='calibri 10') \
                .grid(column=0, row=3)
            Label(player_stats_frame, text=number_of_games_played, font='verdana 10 bold') \
                .grid(column=1, row=3, padx=(0, 28))

            # draws
            Label(player_stats_frame, text='Draws: ', font='calibri 10') \
                .grid(column=2, row=3, padx=(15, 0))
            Label(player_stats_frame, text=draws, font='verdana 10 bold') \
                .grid(column=3, row=3, padx=(0, 25))

            # PLacing the chess board borders
            #self.place_board_coordinates(self.the_border_color)

    def end_new_game(self):
        # Set start_new_game to false, so the game loop can be ended
        with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no')

        self.destroy()
