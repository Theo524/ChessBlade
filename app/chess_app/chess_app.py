from app.chess_app.chess_app_widgets.board import Board
from app.chess_app.chess_app_widgets.bar_menu import BarMenu

import tkinter
from tkinter import messagebox
import os


class ChessApp(tkinter.Tk):
    def __init__(self, mode, **kwargs):
        tkinter.Tk.__init__(self)

        # make window not visible, to allow everything to be loaded properly before display
        self.withdraw()

        # The game mode and the path for this chess app settings and files, shown in these variables
        self.mode = mode

        # -------------APP_ATTRIBUTES-------------
        self.title('ChessBlade')
        self.protocol('WM_DELETE_WINDOW', self.end_new_game)

        # -------------BOARD FRAME-------------
        # -------------everything contained here--------------
        # window container
        self.game_frame = tkinter.Frame(self)
        self.game_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Widgets frame, here is where the notation tab is put
        self.widgets_frame = tkinter.Frame(self.game_frame)

        try:
            fen = kwargs['fen']
            # Actual game board
            # It is inside the game frame
            # (we pass the 'widgets frame' instance to be able to create and update chess notation in real time)
            # in case user opens saved game
            self.main_chess_board = Board(self.game_frame, widgets_frame=self.widgets_frame)
            self.main_chess_board.pack(side=tkinter.LEFT)
            # create board
            self.main_chess_board.build(board_type='saved', fen=fen)
        except KeyError:
            # build default board if not a saved game
            self.main_chess_board = Board(self.game_frame, widgets_frame=self.widgets_frame)
            self.main_chess_board.pack(side=tkinter.LEFT)
            # create board
            self.main_chess_board.build()

        # menu
        menu = BarMenu(self)
        self.configure(menu=menu)

        # Place the widgets frame
        self.widgets_frame.pack(side=tkinter.LEFT, padx=20)

        # window size (based on game widgets)
        self.game_frame.update()
        width = self.game_frame.winfo_width() + 5
        height = self.game_frame.winfo_height() + 5
        self.geometry(f'{width}x{height}')

        # show window
        self.deiconify()

    def end_new_game(self):

        # also prevent user from leaving game against ai
        # get settings
        if self.mode == 'user':
            game_type = self.main_chess_board.game_type

            if game_type == 'computer' and self.main_chess_board.moves > 0:
                # this means the user is playing against the ai, so it should leave the game
                leave_game = messagebox.askyesno('End game?',  'You\'re playing against the ai, if you leave '
                                                               'the match now it will be counted as a loss. '
                                                               'Are you sure you want to leave?')

                if leave_game:
                    # store loss for the user
                    self.main_chess_board.game_score('checkmate', 2)
                    pass

                if not leave_game:
                    # do not close window
                    return

        else:
            leave_game = messagebox.askyesno('End game?', 'Are you sure you wan to exit?')

            if leave_game:
                pass

            else:
                return

        # Set start_new_game to false, so the game loop can be ended
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no\n')
            f.write('saved_game:no')

        self.destroy()
