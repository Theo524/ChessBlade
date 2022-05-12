from app.chess_app.chess_app_widgets.board import MainChessBoard
from app.chess_app.chess_app_widgets.bar_menu import BarMenu
from app.chess_app.chess_app_widgets.chess_ai import AI
from database.database import DatabaseBrowser

from tkinter import *
from tkinter import messagebox, ttk
import time as time
import datetime
import os
import threading
import csv
import chess


class ChessApp(Tk):
    def __init__(self, mode, **kwargs):
        Tk.__init__(self)

        # make window not visible, to allow everything to be loaded properly before display
        self.withdraw()

        # game icon
        # window icon
        self.tk.call('wm', 'iconphoto', self._w,
                     PhotoImage(file=os.getcwd() + '\\app\\resources\\img\\ChessIcon.png'))

        # The game mode and the path for this chess app settings and files, shown in these variables
        self.mode = mode

        # -------------APP_ATTRIBUTES-------------
        self.title('ChessBlade')
        self.protocol('WM_DELETE_WINDOW', self.end_new_game)

        # -------------BOARD FRAME-------------
        # -------------everything contained here--------------
        # window container
        self.game_frame = Frame(self)
        self.game_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Widgets frame, here is where the notation tab is put
        self.widgets_frame = Frame(self.game_frame)

        try:
            saved_data = kwargs['saved_data']
            fen = saved_data[0]
            notation = saved_data[1]
            deleted_pieces = saved_data[2]
            # Actual game board[saved game]
            # It is inside the game frame
            # (we pass the 'widgets frame' instance to be able to create and update chess notation in real time)
            # in case user opens saved game
            self.main_chess_board = AppBoard(self.game_frame, widgets_frame=self.widgets_frame)
            self.main_chess_board.pack(side=LEFT)
            # create board
            self.main_chess_board.build(board_type='saved', fen=fen)
            # NOTATION
            # insert notation and pieces
            self.main_chess_board.chess_notation = notation
            # The moves variable is updated every turn, so every even number of moves corresponds to a player
            # add move to notation
            for n, move in enumerate(notation, start=1):
                self.main_chess_board.notation_tab.insert('end', f'{n}.{move} ')

        except KeyError:
            # build default board if not a saved game
            self.main_chess_board = AppBoard(self.game_frame, widgets_frame=self.widgets_frame)
            self.main_chess_board.pack(side=LEFT)
            # create board
            self.main_chess_board.build()

        # menu
        menu = BarMenu(self)
        self.configure(menu=menu)

        # Place the widgets frame
        self.widgets_frame.pack(side=LEFT, padx=20)

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
            print(self.main_chess_board.moves)

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


class AppBoard(MainChessBoard):

    def __init__(self, master, **kwargs):
        # extends the main board
        MainChessBoard.__init__(self, master)

        # Trackers
        self.chess_notation = []
        self.deleted_pieces = []

        # frame containing chess notation tab
        if kwargs:
            self.widgets_frame = kwargs['widgets_frame']
        else:
            self.widgets_frame = Frame(self.master)

        # game mode
        try:
            self.mode = master.master.mode
        except AttributeError:
            self.mode = master.mode

        # game_settings
        settings = self.get_game_settings(self.mode)  # sets game settings
        self.difficulty = settings[0]
        self.time = settings[1]
        self.game_type = settings[2]
        self.player_piece_color = settings[3]
        self.opponent_piece_color = settings[4]
        self.border_color = settings[5]
        self.board_color = settings[6]

        # board look
        # colors for board
        self.board_colors = [
                                'white', self.board_color, 'white', self.board_color, 'white', self.board_color,
                                'white', self.board_color,
                                self.board_color, 'white', self.board_color, 'white', self.board_color, 'white',
                                self.board_color, 'white',
                            ] * 4

        # make board
        self.board = self.make_board()

        # Game border
        self.configure(highlightthickness=5, highlightbackground=self.border_color)

        # file paths
        self.settings_file_path = os.getcwd() + '\\app\\chess_app\\all_settings'

        # deleted_pieces tracking pos
        self.b_x = 0
        self.b_y = 0

        # add notation if needed
        if self.widgets_frame:
            self.add_notation_tab()

        # ai board
        self.ai_board = chess.Board()
        # the actual ai
        self.ai = AI(self.ai_board)

        # to know when the game ends
        self.game_over = False

        # game duration
        self.game_duration = None

        # pawn promotion
        self.promotion_window = None
        self.promotion = False

    @staticmethod
    def get_game_settings(mode):
        """Get game settings

        :param str mode: The game mode the player is in

        :rtype: list
        :returns: list containing settings based on game mode
        """
        if mode == 'guest':

            # open default settings file
            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    print(f'Guest settings : {row}')
                    # retrieve settings in file
                    return row

        if mode == 'user':
            # fetch settings for that specific user
            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    print(f'User settings : {row}')
                    # retrieve these personalized settings from user file
                    return row

    def add_notation_tab(self):
        """Implement game tabs for chess notation"""

        # ---------------NOTEBOOK--------------
        # notebook for chess notation
        self.notebook = ttk.Notebook(self.widgets_frame, height=600, width=600)
        self.notebook.pack(pady=(7, 0), padx=5)

        # first tab
        self.notation_tab = Text(self.notebook)
        self.notation_tab.pack()

        # third tab
        self.board_fen_string_tab = Text(self.notebook)
        self.board_fen_string_tab.pack()

        # second tab
        self.deleted_tab_visual = Frame(self.notebook, bg=self.board_colors[1])
        self.deleted_tab_visual.configure(highlightthickness=5, highlightbackground='black')
        self.deleted_tab_visual.pack()

        # add  tabs to chess notebook
        self.notebook.add(self.notation_tab, text='Notation')
        self.notebook.add(self.deleted_tab_visual, text='Deleted pieces')
        self.notebook.add(self.board_fen_string_tab, text='FEN')

    def update_current_piece(self, position):
        """Command assigned to every button in the board

        :param str position: chessboard coordinate, used to determine moves
        """

        # color of the button, piece and piece color the user just clicked
        current_button_color = self.board[position]['color']
        piece_name = self.board[position]['piece']['piece_name']
        piece_color = self.board[position]['piece']['piece_color']

        if self.tracker:
            # color of the button, piece and piece color last clicked
            # It can be retrieved because the tracker is only updated at the end of this function
            old_piece_name = self.tracker[-1]['selected_piece']['piece_name']
            old_piece_color = self.tracker[-1]['selected_piece']['piece_color']
            old_piece_position = self.tracker[-1]['player_clicked']

        # HIGHLIGHTING MOVES
        # if the game type is 'two_player' mode and a piece was clicked
        if self.game_type == 'two_player':
            if self.player_one_turn:
                # If it is player one turn
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.reset_board_colors()

                    # We only allow player pieces to be highlighted
                    # rooks
                    if self.board[position]['piece']['piece_name'] == 'rook':
                        self.piece_highlighting(f'{position}', 'rook', self.player_piece_color)

                    # prawn
                    if self.board[position]['piece']['piece_name'] == 'prawn':
                        self.piece_highlighting(f'{position}', 'prawn', self.player_piece_color)

                    # bishop
                    if self.board[position]['piece']['piece_name'] == 'bishop':
                        self.piece_highlighting(f'{position}', 'bishop', self.player_piece_color)

                    # knight
                    if self.board[position]['piece']['piece_name'] == 'knight':
                        self.piece_highlighting(f'{position}', 'knight', self.player_piece_color)

                    # queen
                    if self.board[position]['piece']['piece_name'] == 'queen':
                        self.piece_highlighting(f'{position}', 'queen', self.player_piece_color)

                    # king
                    if self.board[position]['piece']['piece_name'] == 'king':
                        self.piece_highlighting(f'{position}', 'king', self.player_piece_color)

                # If the piece is enemy
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.reset_board_colors()

            if self.player_two_turn:
                # If it is the second player turn
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.reset_board_colors()

                    # We only allow enemy pieces to be highlighted

                    # rooks
                    if self.board[position]['piece']['piece_name'] == 'rook':
                        self.piece_highlighting(f'{position}', 'rook', self.opponent_piece_color)

                    # prawn
                    if self.board[position]['piece']['piece_name'] == 'prawn':
                        self.piece_highlighting(f'{position}', 'prawn', self.opponent_piece_color)

                    # bishop
                    if self.board[position]['piece']['piece_name'] == 'bishop':
                        self.piece_highlighting(f'{position}', 'bishop', self.opponent_piece_color)

                    # knight
                    if self.board[position]['piece']['piece_name'] == 'knight':
                        self.piece_highlighting(f'{position}', 'knight', self.opponent_piece_color)

                    # queen
                    if self.board[position]['piece']['piece_name'] == 'queen':
                        self.piece_highlighting(f'{position}', 'queen', self.opponent_piece_color)

                    # king
                    if self.board[position]['piece']['piece_name'] == 'king':
                        self.piece_highlighting(f'{position}', 'king', self.opponent_piece_color)

                # If the piece is black
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.reset_board_colors()

        # if the game type is 'computer'(against ai)
        if self.game_type == 'computer':
            # actually against the ai its always player 1 turn
            if self.player_one_turn:
                # If it is player one turn
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.reset_board_colors()

                    # We only allow player pieces to be highlighted
                    # rooks
                    if self.board[position]['piece']['piece_name'] == 'rook':
                        self.piece_highlighting(f'{position}', 'rook', self.player_piece_color)

                    # prawn
                    if self.board[position]['piece']['piece_name'] == 'prawn':
                        self.piece_highlighting(f'{position}', 'prawn', self.player_piece_color)

                    # bishop
                    if self.board[position]['piece']['piece_name'] == 'bishop':
                        self.piece_highlighting(f'{position}', 'bishop', self.player_piece_color)

                    # knight
                    if self.board[position]['piece']['piece_name'] == 'knight':
                        self.piece_highlighting(f'{position}', 'knight', self.player_piece_color)

                    # queen
                    if self.board[position]['piece']['piece_name'] == 'queen':
                        self.piece_highlighting(f'{position}', 'queen', self.player_piece_color)

                    # king
                    if self.board[position]['piece']['piece_name'] == 'king':
                        self.piece_highlighting(f'{position}', 'king', self.player_piece_color)

        # If the color of the button is green
        # It would mean the player had already clicked a piece previously which marked possible moves in green
        if current_button_color == 'light green':

            first_rank = self.coordinates[0]
            last_rank = self.coordinates[-1]
            # detecting a prawn possibly moving to the last rank
            if self.tracker[-1]['selected_piece']['piece_name'] == 'prawn':
                # if it indeed is a prawn then we get the position
                if position in first_rank or position in last_rank:
                    self.promotion = True
                    # if the point being clicked is one of the last ranks
                    color = self.tracker[-1]['selected_piece']['piece_color']
                    self.prawn_upgrade(color, [old_piece_name, old_piece_color, old_piece_position, position])
                else:
                    self.promotion = False

            if not self.promotion:
                # make the move
                self.make_move(old_piece_name, old_piece_color, old_piece_position, target=position)

            # if against the ai
            if self.game_type == 'computer':
                # after player 1 has made its move the ai does its own move
                # because clicking green would mean a move has just been done
                # however if checkmate the board should stop
                if self.ai_board.is_checkmate() or self.ai_board.is_stalemate():
                    self.game_over = True
                self.make_ai_move()

        # if the button clicked is red, that means the piece is to be deleted
        if current_button_color == 'red':
            first_rank = self.coordinates[0]
            last_rank = self.coordinates[-1]
            # detecting a prawn possibly moving to the last rank
            if self.tracker[-1]['selected_piece']['piece_name'] == 'prawn':
                # if it indeed is a prawn then we get the position
                if position in first_rank or position in last_rank:
                    self.promotion = True
                    # if the point being clicked is one of the last ranks
                    color = self.tracker[-1]['selected_piece']['piece_color']
                    self.prawn_upgrade(color, [old_piece_name, old_piece_color, old_piece_position, position])

                else:
                    self.promotion = False

            if not self.promotion:
                # make the move
                self.make_move(old_piece_name, old_piece_color, old_piece_position, target=position)

            # if against the ai
            # because clicking red would mean a move has just been done
            if self.game_type == 'computer':
                # after player 1 has made its move the ai does its own move
                if self.ai_board.is_checkmate() or self.ai_board.is_stalemate():
                    self.game_over = True
                self.make_ai_move()

        # Whenever the user clicks a non piece or empty space, a messagebox appears
        # reset the board colors
        if current_button_color in ['white', self.board_colors[1]] and piece_name is None:
            # message
            messagebox.showerror('Error', f'{position} is an invalid move')
            self.reset_board_colors()

        # Allows to track user history of clicks, appends the current move
        self.tracker.append({'player_clicked': position,
                             'selected_piece': self.board[position]['piece'],
                             'color': self.board[position]['color']})

        # CHECKMATE
        if self.ai_board.is_checkmate():
            self.game_over = True

            messagebox.showinfo('Game over', f'Checkmate')

            if not self.ai_board.turn:
                self.game_score('checkmate', 1)

            else:
                self.game_score('checkmate', 2)

        # STALEMATE
        if self.ai_board.is_stalemate():
            self.game_over = True

            messagebox.showinfo('Game over', f'Game ends in draw')

            # if the user is playing against the ai update its score
            self.game_score('stalemate')

        if self.game_over:
            new_game = messagebox.askyesno('Game over', f'\nYou predicted this game would end at {self.time}, '
                                                        f'it actually took {self.game_duration}.\n'
                                                        f'Do you want to play a again?')

            if new_game:
                # instructions for new game file
                with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
                    f.write('new_game:yes\n')
                    f.write('saved_game:no')

                self.master.master.destroy()

            else:
                self.enable_board_buttons(False)

# overwrite for notation
    def make_move(self, piece_name, color, old_position, target=''):
        """Make a move in the chess board

        :param str piece_name: the name of the given piece
        :param str color: The color of the given piece
        :param str old_position: The position the piece is in
        :param str target: The position the piece will move to
        """

        # NOTATION
        # determine move or delete piece for notation
        try:
            if self.board[target]['piece']['piece_name'] is None:
                # a normal move
                # Add to notation
                self.update_notation('moved_piece', target, piece_name, new_piece_name='', color=color)

                # fen tab
                self.board_fen_string_tab.insert('end', f'{self.moves}. {self.get_game_fen_string_original()}\n')

            elif self.board[target]['piece']['piece_name'] is not None:
                # deleting a piece
                # add this deleted piece to the deleted pieces list
                self.deleted_pieces.append([self.board[target]['piece']['piece_name'],
                                            self.board[target]['piece']['piece_color']])
                # Add to notation
                self.update_notation('deleted_piece', target, piece_name,
                                     new_piece_name=str(self.board[target]['piece']['piece_name']), color=color)

                # fen tab
                self.board_fen_string_tab.insert('end', f'{self.moves}. {self.get_game_fen_string_original()}\n')

            # CHESS MOVE
            # place the selected piece in the selected spot
            self.place_piece(piece_name, color, target)
            # replace the place where that piece originally was with a blank space img
            self.place_piece('blank', 'blank', old_position)

        except KeyError:
            # promotion for enemy prawn
            if len(target) == 3:
                # first two letter is position, last part is the piece to be promoted
                # e.g. 'e1q' prawn to queen in e1
                temp = {'q': 'queen', 'r': 'rook', 'b': 'bishop', 'n': 'knight'}
                promotion_str = list(target)
                promotion_position = promotion_str[0] + promotion_str[1]  # e.g. 'a' + '8' = 'a8'
                promotion_piece = temp[promotion_str[2]]  # piece letter e.g. 'q', 'queen'
                # chose piece based on last letter of promotion str
                # chose position based on first two letter of promotion str
                self.place_piece(promotion_piece, self.opponent_piece_color, promotion_position)
                self.place_piece('blank', 'blank', old_position)

                # notation
                self.chess_notation.append(f'{target}')
                # The moves variable is updated every turn, so every even number of moves corresponds to a player
                # add move to notation
                self.notation_tab.insert('end', f'{self.moves}.{target} ')

        try:
            # move for virtual board(chess lib)
            move = chess.Move.from_uci(f'{old_position}{target}')

            # legal moves available
            # legal_moves = list(self.ai_board.legal_moves)
            # print(self.ai_board.is_legal(move))

            # Make move in virtual board
            self.ai_board.push(move)
        except AssertionError:
            # if there was an error is because of the promotion
            # pushes an invalid piece to the board so to avoid that
            # we create a fen string from the current board and place it
            fen = self.get_game_fen_string_original()
            self.ai_board = chess.Board(fen=fen)

        # increase number of moves by one
        self.moves += 1

        # We now swap turns so only one side can make moves
        self.swap_turns()

        # reset board colors back to normal
        self.reset_board_colors()
        self.master.master.update()

    def make_ai_move(self):
        """Move made by ai"""

        # to avoid errors on checkmate or stalemate
        if self.game_over:
            return

        # disable all board buttons so the user can't interrupt
        self.enable_board_buttons(False)

        # depth(how many moves to look ahead) will be based on difficulty
        depth = 1
        if self.difficulty == 'Novice':
            depth = 1

        if self.difficulty == 'Intermediate':
            depth = 2

        if self.difficulty == 'Expert':
            depth = 3

        # get best move depending on difficulty
        original_move = self.ai.selectmove(depth)
        move = list(str(original_move))

        # with this data I can get the name and info to make the move
        # basically 'a8h8' becomes 'a8' 'g8'
        starting_pos = ''.join(move[:2])
        target_pos = ''.join(move[2:])

        # name of piece to be moved
        name = self.board[starting_pos]['piece']['piece_name']

        # color of piece to be moved
        color = self.board[starting_pos]['piece']['piece_color']

        # make move
        self.make_move(piece_name=name, color=color, old_position=starting_pos, target=target_pos)

        # enable board button again
        self.enable_board_buttons(True)

    def swap_turns(self):
        """Swap turns between players"""

        if self.game_type == 'two_player':
            if self.moves % 2 == 0:
                self.player_two_turn = True
                self.player_one_turn = False
            else:
                self.player_two_turn = False
                self.player_one_turn = True

        if self.game_type == 'computer':
            # always player one turn, since its playing against the ai
            self.player_one_turn = True

    def update_notation(self, mode, position, old_piece_name, new_piece_name, color):
        """Add game data to chess notation tabs

        :param str mode: determines what tab to add the data to
        :param str position: chessboard coordinate
        :param str old_piece_name: Used for chess notation move
        :param str new_piece_name: Used for chess notation move
        :param str color: piece_color
        """
        # since chess notation for prawns have no letter and knights use 'N'
        # this small section will handle that
        piece_letter = ''
        if old_piece_name == 'knight':
            piece_letter = 'N'
        else:
            if old_piece_name == 'prawn':
                piece_letter = ''

            if old_piece_name is None:
                pass

            else:
                piece_letter = str(old_piece_name[0].upper()) \
                    if color == 'black' else str(old_piece_name[0].lower())

        # actual notation
        if mode == 'moved_piece':
            # chess notation tracker(list)
            self.chess_notation.append(f'{piece_letter}{position}')
            # The moves variable is updated every turn, so every even number of moves corresponds to a player
            # add move to notation
            self.notation_tab.insert('end', f'{self.moves}.{self.chess_notation[-1]} ')

        if mode == 'deleted_piece':
            # This time we add an 'x' in the middle to show that a piece is being destroyed
            self.chess_notation.append(f'{piece_letter}x{position}')

            # add the move to chess notation tab
            self.notation_tab.insert('end', f'{self.moves}.{self.chess_notation[-1]} ')

            # also add piece image
            # b_x and b_y represent the grid coordinated to place the images
            if self.board[position]['piece']['piece_color'] == 'white':
                img = PhotoImage(file=self.white_pieces[f'{new_piece_name}'])
            else:
                img = PhotoImage(file=self.black_pieces[f'{new_piece_name}'])

            label = Label(self.deleted_tab_visual, image=img)
            label.configure(borderwidth=5, bg=self.board_colors[1])
            label.grid(column=self.b_x, row=self.b_y)
            label.image = img
            self.b_x += 1
            if self.b_x == 8:
                self.b_x = 0
                self.b_y += 1

    def threading(self):
        """Thread"""

        # Call work function to start thread
        t1 = threading.Thread(target=self.thread_timer_work)
        t1.start()

    def thread_timer_work(self):
        """Thread that deals with background game timer

        The user can use this to see how long the game took
        """

        # convert time str from db to seconds
        game_time = self.time
        date_time = datetime.datetime.strptime(game_time, "%H:%M:%S")
        time_str = date_time
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        seconds = int(a_timedelta.total_seconds())
        time_taken = 0

        for i in range(seconds):
            # actual timer
            time.sleep(1)
            time_taken += 1

            if self.game_over:
                # convert time taken
                time_convert = time.gmtime(time_taken)
                # convert seconds to time str
                self.game_duration = time.strftime("%H:%M:%S", time_convert)

    def game_score(self, result, winner=0):
        """Decides whether the game is a win, loss or draw

        :param str result: can be checkmate, stalemate and is the outcome of the game
        :param int winner: can either be 1 or 2, 1 indicates the user, 2 indicates the ai is the winner
        """

        if self.mode == 'user':

            # get the current username
            with open(os.getcwd() + '\\app\\login_system_app\\temp\\current_user.txt') as f:
                username = f.read()

            if self.game_type == 'two_player':
                # practice games  (one v one on a single device) aren't scored
                pass

            if self.game_type == 'computer':
                # 1 is the user, 2 is the ai so it would count as a loss for the user in terms of winner/loser
                # first get the user name to search database (loaded at login)
                if result == 'checkmate' and winner == 1:
                    # user won
                    self.update_db_game_score(username, 'win')

                if result == 'checkmate' and winner == 2:
                    # Computer(AI) won
                    self.update_db_game_score(username, 'loss')

                if result == 'stalemate':
                    # was a draw
                    self.update_db_game_score(username, 'draw')

    def update_db_game_score(self, user, result):
        """Gets a copy of the user statistics from the db and updates them according to the result

        :param str user: The name of the user (account) playing, won't have errors because every user is unique
        :param str result: Can be a win, loss or draw
        """

        # data
        original_data = DatabaseBrowser.load(load='statistics', username=user)

        # increase number of games played by one
        original_data[1] += 1

        # game score
        if result == 'win':
            # add 1 more win
            original_data[2] += 1

            # add points to ranking according to the game difficulty
            # ranking is basically just points
            # the amount of points added also depends on the difficulty
            if self.difficulty == 'Novice':
                original_data[5] += 10

            if self.difficulty == 'Intermediate':
                original_data[5] += 20

            if self.difficulty == 'Expert':
                original_data[5] += 30

        if result == 'loss':
            # add one more loss
            original_data[3] += 1

            # ranking doesn't get updated in loss

        if result == 'draw':
            # add one more draw
            original_data[4] += 1

            # add points to ranking according to the game difficulty
            # the amount of points added also depends on the difficulty
            if self.difficulty == 'Novice':
                original_data[5] += 5

            if self.difficulty == 'Intermediate':
                original_data[5] += 10

            if self.difficulty == 'Expert':
                original_data[5] += 15

        # finally add the data to the database
        DatabaseBrowser.save(save='statistics', username=original_data[0], data=original_data)

