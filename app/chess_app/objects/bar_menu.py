from tkinter import *
import os
from app.chess_app.objects.settings import Settings
from tkinter import ttk
import csv


class BarMenu(Menu):
    def __init__(self, root):
        Menu.__init__(self, root)

        # GAME MODE
        self.mode = root.mode

        # Create a menu
        self.game_menu = Menu(self, tearoff=0)
        # Add the game menu options
        self.game_menu.add_command(label='New game', command=self.new_game)
        if self.mode == 'user':
            self.game_menu.add_command(label='Player stats', command=self.show_player_stats)
            self.game_menu.add_command(label='Save')
        self.game_menu.add_command(label='Exit', command=self.exit)
        # Name the game menu
        self.add_cascade(label='Game', menu=self.game_menu)

        # Create another menu
        self.help_menu = Menu(self, tearoff=0)
        # Add menu options
        self.help_menu.add_command(label='Settings', command=self.open_settings)
        self.help_menu.add_command(label='Rules')
        # Name teh menu
        self.add_cascade(label='Help', menu=self.help_menu)

        # Create another menu
        self.about_menu = Menu(self, tearoff=0)
        # Add menu options
        self.about_menu.add_command(label='Contact us')
        self.about_menu.add_command(label='About us')
        # Name the menu
        self.add_cascade(label='About', menu=self.about_menu)

    def open_settings(self):
        """Open game settings"""
        s = Settings(self.mode)
        s.mainloop()

    def new_game(self):
        # os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # Set new game file to 'yes' and destroy window, so a new ChessAPp is run
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:yes')

        self.master.destroy()

    def exit(self):
        # Set new game file to 'no' and destroy window so the looping chess app stops
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no')

        self.master.destroy()

    def show_player_stats(self):
        """Shows player data"""

        with open(os.getcwd() + '//app//chess_app//all_settings//user//user_stats.csv') as f:
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
        with open(os.getcwd() + '//app//login_system_app//temp//current_user.txt', 'r') as f:
            username = f.read()

        new_window = Toplevel()

        # Create the frame
        player_stats_frame = Frame(new_window, text='Player history', width=320, height=180)
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
