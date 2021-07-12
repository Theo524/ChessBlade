from app.chess_app.objects.board import Board
from app.chess_app.objects.bar_menu import BarMenu

import tkinter
import os
import csv
from tkinter import ttk


class ChessApp(tkinter.Tk):
    """Window container for game objects"""
    def __init__(self, mode):
        tkinter.Tk.__init__(self, mode)

        # The game mode and the path for this chess app settings and files, shown in these variables
        self.mode = mode

        # -------------APP_ATTRIBUTES-------------
        self.resizable(0, 0)
        self.title('Chess by theo')
        self.protocol('WM_DELETE_WINDOW', self.end_new_game)

        # menu
        menu = BarMenu(self)
        self.configure(menu=menu)

        # -------------BOARD FRAME-------------
        # -------------everything contained here--------------
        self.game_frame = tkinter.Frame(self)
        self.game_frame.pack(side=tkinter.TOP)

        # Widgets frame, here is where all the objects apart from the chess board are placed, for now its only chess notation
        self.widgets_frame = tkinter.Frame(self.game_frame)

        # Actual game board
        # It is inside the board frame
        # (we pass the 'widgets frame' instance to be able to create and update chess notation in real time)
        self.main_chess_board = Board(self.game_frame, widgets_frame=self.widgets_frame)
        self.main_chess_board.pack(side=tkinter.LEFT)
        # create board
        self.main_chess_board.build()

        # We can now place the widgets frame
        self.widgets_frame.pack(side=tkinter.LEFT, padx=20)

    def end_new_game(self):
        # Set start_new_game to false, so the game loop can be ended
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no')

        self.destroy()
