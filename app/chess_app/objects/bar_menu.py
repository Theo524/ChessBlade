from tkinter import *
import os
from app.chess_app.objects.settings import Settings


class BarMenu(Menu):
    def __init__(self, root):
        Menu.__init__(self, root)

        # Create a menu
        self.game_menu = Menu(self, tearoff=0)
        # Add the game menu options
        self.game_menu.add_command(label='New game', command=self.new_game)
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

    @staticmethod
    def open_settings():
        """Open game settings"""
        s = Settings()
        s.mainloop()

    def new_game(self):
        # os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # Set new game file to 'yes' and destroy window, so a new ChessAPp is run
        with open(os.getcwd() + '//apps//chess_app//all_settings//data.txt', 'w') as f:
            f.write('new_game:yes')

        self.master.destroy()

    def exit(self):
        # Set new game file to 'no' and destroy window so the looping chess app stops
        with open(os.getcwd() + '//apps//chess_app//all_settings//data.txt', 'w') as f:
            f.write('new_game:no')

        self.master.destroy()
