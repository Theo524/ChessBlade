from tkinter import *
from tkinter import messagebox
import string
import os
from PIL import Image, ImageTk
import chess

from app.chess_app.chess_app_widgets.chess_ai import AI


# base board that is extended
class MainChessBoard(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)

        # Game attributes
        self.player_one_turn = True
        self.player_two_turn = False
        self.AI_turn = False
        self.moves = 1

        # pieces following
        self.tracker = []

        # required data
        self.letters = list(string.ascii_lowercase[:8])  # chess letters (a-h)
        self.alphabet = list(string.ascii_letters)  # alphabet
        self.nums = [str(i) for i in range(10)]  # Numbers as str (0-9)

        # custom_settings
        self.game_type = 'two_player'
        self.difficulty = 'Intermediate'
        self.player_piece_color = 'black'  ##settings[3]
        self.opponent_piece_color = 'white'  ##settings[4]
        self.border_color = 'black'  ##settings[5]
        self.board_color = 'brown'  # settings[6]
        self.piece_format = 'default'

        # colors for board
        self.board_colors = [
                                'white', self.board_color, 'white', self.board_color, 'white', self.board_color,
                                'white', self.board_color,
                                self.board_color, 'white', self.board_color, 'white', self.board_color, 'white',
                                self.board_color, 'white',
                            ] * 4

        # file paths
        self.pieces_file_path = os.getcwd() + '\\app\\resources\\pieces_img'

        # data structures
        # 2d array of all chess positions, 1d array of all chess positions and the same one reversed
        self.coordinates, self.pieces, self.pieces_reversed = self.add_chess_pieces_positions()  # fill the lists
        self.board = self.make_board()  # game board around which game revolves

        # Dictionaries storing piece images file names
        self.black_pieces, self.white_pieces = self.get_piece_img()

        # Game border
        self.configure(highlightthickness=5, highlightbackground=self.border_color)

        # ai board
        self.ai_board = chess.Board()
        # the actual ai
        self.ai = AI(self.ai_board)

        # to know when the game ends
        self.game_over = False

        # prawn promotion
        self.promotion_window = None
        self.promotion = False

        # kin gin check
        self.king_in_check = []

    def add_chess_pieces_positions(self):
        """Populate 1d and 2d array chess"""

        # get coordinates, e.g. 'a1', 'b1', etc into a 2 dimensional array
        coordinates = []
        for row in range(8):
            temp = []
            for letter in self.letters:
                temp.append(f'{letter}{row + 1}')
            coordinates.append(temp)

        # get coordinates, e.g. 'a1', 'b1', etc into a 1 dimensional array
        pieces = []
        for row in coordinates:
            for piece in row:
                pieces.append(piece)

        # reversed order
        reversed_p = coordinates[:]
        reversed_p.reverse()
        pieces_reversed = []
        for row in reversed_p:
            for piece in row:
                pieces_reversed.append(piece)

        return coordinates, pieces, pieces_reversed

    def make_board(self):
        """Make the board dict"""

        board = {}

        # Create a dictionary with the main key being a coordinate
        # Assign coordinates to their corresponding button
        x = 0
        y = 7
        # repeat 64 times (number of coordinates in chess)
        for i in range(len(self.board_colors)):
            # Store the current coordinate in a variable e.g in the first iteration it represents a8
            # in terms of y and x (from self.coordinates)
            current_position = self.coordinates[y][x]

            # make board
            board[current_position] = {'button': Button(self, bg=self.board_colors[i],
                                                        text=f'\t        {current_position}',
                                                        font=('arial', 7),
                                                        compound=BOTTOM,
                                                        activebackground='light blue',
                                                        relief=SOLID,
                                                        bd=1,
                                                        cursor='tcross',
                                                        highlightbackground="black",
                                                        highlightcolor="black",
                                                        command=lambda p=current_position:
                                                        self.update_current_piece(p)),
                                       'piece': {'piece_name': None, 'piece_color': None},
                                       'color': self.board_colors[i],
                                       'selected': False}

            # coordinates in first iteration are 'x=0, y=7', where the data is 'a8'
            # next coordinates are 'x=1, y=7' where the val is 'b8'
            # hence we move to the next item in the current list by adding 1 to x
            x += 1
            # Once we reach the end of the list, the x coordinate is 8, so we move up one in the y axis
            # by subtracting 1 (from 8 to 7 to 6 and so on...)
            if x == 8:
                y -= 1
                x = 0

        return board

    def place_buttons(self):
        """Place the actual buttons on the screen"""

        x = 0
        y = 0
        for button in self.board.values():
            # We access the button object and use tkinter 'grid()' to set the column and row with x and y
            button['button'].grid(column=x, row=y)

            # We place the buttons on the frame in a linear way, so the first row would be placed
            # and x represents each button/column in this first row
            x += 1
            # When we reach th end of the row, which is 8 buttons per row, we move to the next row
            if x == 8:
                # Set x to 0 to start a series of columns from the begging and increase y by one to move one row down
                x = 0
                y += 1

    def place_default_pieces_on_screen(self):
        """Place default starting pieces on the screen"""

        # Thanks to the method 'place_piece' I've made, we can easily move and delete any piece from the screen
        # We enter the piece, the color and the position we want to place it at as parameters

        # use a FEN string of only pieces (Forsyth-Edwards Notation)
        staring_fen_string = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

        self.place_fen_string(staring_fen_string)

    def place_fen_string(self, fen_str):
        """Convert fen string and place pieces on board

        :param str fen_str: simplified FEN string to be placed on board
        """

        # Thanks to the method 'place_piece' I've made, we can easily move and delete any piece from the screen
        # We enter the piece, the color and the position we want to place it at as parameters

        # create two lists, one for a dict containing useful data and another for key vals
        coordinates_copy = self.coordinates[:]
        coordinates = []
        for row in range(8):
            temp = []
            for letter in self.letters:
                temp.append({f'{letter}{row + 1}': 'blank'})
            coordinates.append(temp)

        # reverse them so they match required indexes
        coordinates.reverse()
        coordinates_copy.reverse()

        # fen value
        full_str = list(fen_str)

        # coordinates
        x = 0
        y = 0

        # iterate trough each value in the fen string
        for symbol in full_str:
            if symbol in ['/']:
                # if bracket
                # move one row down
                y += 1

                # and return to starting col
                x = 0

            if symbol in self.alphabet:
                # if letter, assign letter to dictionary
                coordinates[y][x] = {f'{coordinates_copy[y][x]}': symbol}
                x += 1

            if symbol in self.nums:
                # if number move jump spaces
                x += int(symbol)

        # place pieces on board
        for row in coordinates:
            for val in row:
                # get the key as a list (position)
                position = [key for key in val.keys()]
                # get the piece as a list
                piece = [value for value in val.values()]

                # convert the lists to str
                piece = ''.join(piece)
                position = ''.join(position)

                # get the color from the letter type
                # according to the rules - white, lower case and black uppercase
                if piece in list(string.ascii_lowercase):
                    color = self.opponent_piece_color
                elif piece in list(string.ascii_uppercase):
                    color = self.player_piece_color
                else:
                    color = 'blank'

                piece_dict = {'P': 'prawn', 'p': 'prawn',
                              'R': 'rook', 'r': 'rook',
                              'N': 'knight', 'n': 'knight',
                              'B': 'bishop', 'b': 'bishop',
                              'Q': 'queen', 'q': 'queen',
                              'K': 'king', 'k': 'king',
                              'blank': 'blank'}

                # finally place the piece
                self.place_piece(piece_dict[piece], color, position)

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

        # STALEMATE
        if self.ai_board.is_stalemate():
            self.game_over = True

            messagebox.showinfo('Game over', f'Game ends in draw')

        if self.game_over:
            new_game = messagebox.showinfo('Game over', f'Done')

            self.enable_board_buttons(False)

    def prawn_upgrade(self, color, move_data):
        """Gui for prawn promotion

        :param str color: color of the prawn piece
        :param list move_data: the move to be performed on the board
        """

        # disable all board buttons (force user to promote prawn)
        self.enable_board_buttons(False)

        # gui aspects
        self.promotion_window = Toplevel(master=self.master.master)
        Label(self.promotion_window, text=f'Promote {color} prawn to:', font='Helvetica 15 italic').pack()
        frame_1 = Frame(self.promotion_window)
        frame_1.pack()
        frame_2 = Frame(self.promotion_window)
        frame_2.pack()

        queen_btn = Button(frame_1, command=lambda: self.promotion_click('queen', move_data))
        queen_btn.pack(side=LEFT, pady=5, padx=5)
        temp = ImageTk.PhotoImage(
            Image.open(self.black_pieces['queen'] if color == 'black' else self.white_pieces['queen']))
        queen_btn.configure(image=temp)
        queen_btn.image = temp

        bishop_btn = Button(frame_1, command=lambda: self.promotion_click('bishop', move_data))
        bishop_btn.pack(pady=5, padx=5)
        temp = ImageTk.PhotoImage(
            Image.open(self.black_pieces['bishop'] if color == 'black' else self.white_pieces['bishop']))
        bishop_btn.configure(image=temp)
        bishop_btn.image = temp

        rook_btn = Button(frame_2, command=lambda: self.promotion_click('rook', move_data))
        rook_btn.pack(side=LEFT, pady=5, padx=5)
        temp = ImageTk.PhotoImage(
            Image.open(self.black_pieces['rook'] if color == 'black' else self.white_pieces['rook']))
        rook_btn.configure(image=temp)
        rook_btn.image = temp

        knight_btn = Button(frame_2, command=lambda: self.promotion_click('knight', move_data))
        knight_btn.pack(pady=5, padx=5)
        temp = ImageTk.PhotoImage(
            Image.open(self.black_pieces['knight'] if color == 'black' else self.white_pieces['knight']))
        knight_btn.configure(image=temp)
        knight_btn.image = temp

        self.promotion_window.protocol("WM_DELETE_WINDOW", self.pr_window_on_close)

        # start window
        self.promotion_window.mainloop()

    def promotion_click(self, piece, move_data):
        """Display new piece enable board buttons

        :param str piece: name of piece user chose to promote
        :param list move_data: data needed for a move"""

        # make the move on the boards
        self.make_move(piece, move_data[1], move_data[2], move_data[3])

        # close gui promotion window
        self.promotion_window.destroy()

        # buttons available to click again
        self.enable_board_buttons(True)

    @staticmethod
    def pr_window_on_close():
        """So that the user can't avoid promoting the prawn piece"""

        messagebox.showerror('Error', 'You must select one the options')

    def locate_piece(self, piece, color):
        """Locate a piece on the board"""

        matches = []

        for item in self.board.items():
            # We access the dict item
            # position
            position = item[0]  # str
            position_piece_name = item[1]['piece']['piece_name']  # str
            position_piece_color = item[1]['piece']['piece_color'] # str

            if position_piece_color == color and position_piece_name == piece:
                matches.append(position)

        return matches

    def make_move(self, piece_name, color, old_position, target=''):
        """Make a move in the chess board

        :param str piece_name: the name of the given piece
        :param str color: The color of the given piece
        :param str old_position: The position the piece is in
        :param str target: The position the piece will move to
        """

        # CHESS MOVE
        # place the selected piece in the selected spot
        self.place_piece(piece_name, color, target)
        # replace the place where that piece originally was with a blank space img
        self.place_piece('blank', 'blank', old_position)

        try:
            # move for virtual board(chess lib)
            move = chess.Move.from_uci(f'{old_position}{target}')

            # legal moves available
            legal_moves = list(self.ai_board.legal_moves)
            if self.ai_board.is_legal(move):
                # Make move in virtual board
                self.ai_board.push(move)

            else:
                pass
        except AssertionError:
            # if there was an error is because of the promotion
            # pushes an invalid piece to the board so to avoid that
            # we create a fen string from the current board and place it
            # fen = self.get_game_fen_string_original()
            # self.ai_board = chess.Board(fen=fen)
            # always set a successful move in lib board for more security
            fen = self.get_game_fen_string_original()
            self.ai_board = chess.Board(fen=fen)

        # increase number of moves by one
        self.moves += 1

        # We now swap turns so only one side can make moves
        self.swap_turns()

        # reset board colors back to normal
        self.reset_board_colors()
        try:
            self.master.master.update()
        except AttributeError:
            pass

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

    def reset_board_colors(self):
        """Reset board colors to normal(to eliminate highlighting)"""

        i = 0
        coordinates = self.coordinates[:]
        coordinates.reverse()
        # iterate through the entire board and set the color of each button back to its corresponding one
        # by iterating over the board colors at the same time
        # do not reset checked king

        # reset board color
        for row in coordinates:
            for col in row:
                self.board[col]['button'].configure(bg=self.board_colors[i])
                self.board[col]['color'] = self.board_colors[i]
                i += 1

        # mark king in red if in check
        self.king_color_highlight()

    def king_color_highlight(self):
        """Mark king in red if in check"""
        # put king in check color if needed after resetting board colors
        try:
            if self.king_in_check[1]:
                king_in_check_pos = self.king_in_check[0]
                # set red (lighter tone) hex code
                #
                self.board[king_in_check_pos]['button'].configure(bg='red')
            if not self.king_in_check[1]:
                # reset board colors function remade
                # not called to avoid recursion
                i = 0
                coordinates = self.coordinates[:]
                coordinates.reverse()
                # reset board color
                for row in coordinates:
                    for col in row:
                        self.board[col]['button'].configure(bg=self.board_colors[i])
                        self.board[col]['color'] = self.board_colors[i]
                        i += 1
        except IndexError:
            pass

    def enable_board_buttons(self, flag):
        """Disable or enable board buttons

        :param bool flag: determines whether to enable or disable all buttons
        """

        coordinates = self.coordinates[:]
        coordinates.reverse()
        # iterate through the entire board and set the buttons active or disabled
        # this allows the ai to perform its move without user interruption
        for row in coordinates:
            for col in row:
                if flag:
                    self.board[col]['button']['state'] = 'normal'

                if not flag:
                    self.board[col]['button']['state'] = 'disable'

    def piece_highlighting(self, position, piece, piece_color):
        """Highlights all possible moves for a given piece

        :param str position: Chessboard coordinate
        :param str piece: Piece name
        :param str piece_color: Piece color
        """

        # We highlight the piece being clicked to blue, so it is evident what piece the user selected
        self.board[position]['button'].configure(bg='light blue')

        # rook
        if piece == 'rook':
            # rook moves horizontally and vertically in a straight line

            # The function returns a list of possible moves for the piece
            all_possible_rook_moves = self.get_all_possible_moves('rook', 'none', position)

            if piece_color == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # Empty button with no piece
                        if self.board[position]['piece']['piece_color'] is None:
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is for the enemy
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            # if it is white, highlight it with red so it becomes available to delete
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is not white
                        if self.board[position]['piece']['piece_color'] is None:
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a white piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

        # bishop
        if piece == 'bishop':
            # bishop moves diagonally in all directions
            all_possible_bishop_moves = self.get_all_possible_moves('bishop', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_bishop_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            # if enemy piece, highlight to red
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            # if black piece stop highlighting
                            break

                        # if there is no piece, convert to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:

                for move_pattern in all_possible_bishop_moves:
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            break

                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # knight
        if piece == 'knight':
            # knight moves two blocks forward and marks the side in all directions
            all_possible_knight_moves = self.get_all_possible_moves('knight', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is black, move to the next move
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            break

                        # if the piece is white, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # if there is no piece, highlight and mark green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is black, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # if the piece is white, move to the next move
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            continue

                        # if there is no piece, highlight and mark green green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # queen
        if piece == 'queen':
            # queen moves are just a combination of a rook and a bishop
            all_possible_queen_moves = self.get_all_possible_moves('queen', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            break

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            break

        # king
        if piece == 'king':
            all_possible_king_moves = self.get_all_possible_moves('king', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            continue

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            continue

        # prawns
        if piece_color == self.player_piece_color and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', self.player_piece_color, position)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            right_diagonal = all_prawns[1]
            left_diagonal = all_prawns[2]

            for position in prawn_up:
                # only loops twice, e.g. 'e5' would generate 'e6' and 'e7'

                # if white or black piece stop highlight
                if self.board[position]['piece']['piece_color'] in [self.opponent_piece_color, self.player_piece_color]:
                    break

                # else highlight as green
                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # left diagonal is just one position e.g. for 'b2' it would be 'b1'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # right diagonal is just one position e.g. for 'b2' it would be 'b3'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

        if piece_color == self.opponent_piece_color and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', self.opponent_piece_color, position)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            left_diagonal = all_prawns[1]
            right_diagonal = all_prawns[2]

            for position in prawn_up:
                # if the piece is white we stop highlighting
                if self.board[position]['piece']['piece_color'] in [self.opponent_piece_color, self.player_piece_color]:
                    break

                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # if the piece is black, highlight red
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # if the piece is black, highlight to red
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

    def place_piece(self, piece, color, position):
        """Allows to place a piece anywhere on the board

        :param str piece: Piece name
        :param str color: Piece color
        :param str position: Chessboard coordinate
        """

        # if the color parameter equals black
        if color == 'black':
            # get the black piece image in place with the piece name parameter
            # 'self.black_pieces[piece]' returns file path for that piece img
            temp = ImageTk.PhotoImage(Image.open(self.black_pieces[piece]))
            # configure the tkinter button object at that position and set the 'image' to 'temp'
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # assign the piece to that position in the chess self.board dictionary
            self.board[position]['piece']['piece_name'] = piece

            # assign the piece color to that position in the chess 'self.board' dictionary
            self.board[position]['piece']['piece_color'] = 'black'

        # if the piece color is white
        if color == 'white':
            # get the image
            temp = ImageTk.PhotoImage(Image.open(self.white_pieces[piece]))
            # configure the tkinter button object at that position and set the 'image' to 'temp'
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # assign the piece to that position in the chess self.board dictionary
            self.board[position]['piece']['piece_name'] = piece

            # assign the piece color to that position in the chess 'self.board' dictionary
            self.board[position]['piece']['piece_color'] = 'white'

        # Allows us to delete pieces by placing a 'blank' image on the button
        # will be essential for moving pieces in board
        elif color == 'blank':
            # get the blank image, in this case 'self.white_pieces[piece]' retrieves from the white pieces directory
            # But both 'self.white_pieces and self.black_pieces' directories blank files are the same
            # so it doesnt really matter which one is retrieved from
            temp = ImageTk.PhotoImage(Image.open(self.white_pieces[piece]))
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # set the board piece name to None
            self.board[position]['piece']['piece_name'] = None

            # set the board piece color to None
            self.board[position]['piece']['piece_color'] = None

    def get_all_legal_moves(self, piece, piece_position):
        """Get all legal moves from a specific board position"""

        # determine piece color based on turn
        color = ''
        if self.ai_board.turn:
            color = 'black'
        else:
            color = 'white'

        # list for all legal moves found
        all_moves = []

        # all available legal moves in the current board
        all_legal_moves = list(self.ai_board.legal_moves)

        for move in all_legal_moves:
            # the move look like this usually e.g. 'g3h5'
            # the first two letters are the board coordinates and the second two letters the target
            position = str(move)[:2]
            target = str(move)[2:]

            # with the coordinate being used, find all the targets it has and return that
            if piece == self.board[position]['piece']['piece_name'] and self.board[position]['piece']['piece_color'] == color and position == piece_position:
                all_moves.append(target)

        return all_moves

    def get_all_possible_moves(self, piece, piece_color, position):
        """Generates a list of all possible moves for a piece based on its color and board position

        :param str piece: Piece name
        :param str piece_color: Piece color
        :param str position: Chessboard coordinate

        :returns: A list of all possible moves for the position for the specified piece
        :rtype: list
        """

        # With this list we can get the new positions for this move by modifying only one part
        temp = list(position)

        full_column = [f'{temp[0]}{i}' for i in range(1, 9)]
        full_row = [f'{letter}{temp[1]}' for letter in self.letters]

        index_in_col = full_column.index(position)
        index_in_row = full_row.index(position)

        final = []

        if piece == 'rook':
            # up
            rook_up = [f'{i}' for i in full_column[index_in_col + 1:]]

            #  Down
            rook_down = [f'{i}' for i in full_column[:index_in_col]]
            rook_down.reverse()

            # right
            rook_right = [f'{i}' for i in full_row[index_in_row + 1:]]

            # left
            rook_left = [f'{i}' for i in full_row[:index_in_row]]
            rook_left.reverse()

            # all possible moves combined
            all_possible_rook_moves = [rook_up] + [rook_down] + [rook_left] + [rook_right]
            # legal moves
            legal_moves = self.get_all_legal_moves('rook', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_rook_moves, legal_moves)

            #return all_possible_rook_moves

        if piece == 'bishop':
            # up right diagonal
            bishop_up_right = self.get_diagonal(position, 'up_right')

            # down right diagonal
            bishop_down_right = self.get_diagonal(position, 'down_right')

            # up left diagonal
            bishop_up_left = self.get_diagonal(position, 'up_left')

            # down left diagonal
            bishop_down_left = self.get_diagonal(position, 'down_left')

            # all
            all_possible_bishop_moves = [bishop_up_right] + [bishop_down_right] + \
                                        [bishop_up_left] + [bishop_down_left]

            # legal moves
            legal_moves = self.get_all_legal_moves('bishop', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_bishop_moves, legal_moves)

            #return all_possible_bishop_moves

        if piece == 'knight':
            # Generate moves, by moving positions in board (clockwise)
            move_one = self.move_column(self.move_row(self.move_row(position, 'increase'), 'increase'), 'increase')
            move_two = self.move_row(self.move_column(self.move_column(position, 'increase'), 'increase'), 'increase')

            move_three = self.move_row(self.move_column(self.move_column(position, 'increase'), 'increase'),
                                       'decrease')
            move_four = self.move_column(self.move_row(self.move_row(position, 'decrease'), 'decrease'), 'increase')

            move_five = self.move_column(self.move_row(self.move_row(position, 'decrease'), 'decrease'), 'decrease')
            move_six = self.move_row(self.move_column(self.move_column(position, 'decrease'), 'decrease'), 'decrease')

            move_seven = self.move_row(self.move_column(self.move_column(position, 'decrease'), 'decrease'),
                                       'increase')
            move_eight = self.move_column(self.move_row(self.move_row(position, 'increase'), 'increase'), 'decrease')

            # all moves
            all_possible_knight_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + \
                                        [move_six] + [move_seven] + [move_eight]
            all_possible_knight_moves = [[move] for move in all_possible_knight_moves if move is not None]

            # legal
            legal_moves = self.get_all_legal_moves('knight', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_knight_moves, legal_moves)

            #return all_possible_knight_moves

        if piece == 'queen':
            # basically a copy of the rook and the bishops moves

            # up
            queen_up = [f'{i}' for i in full_column[index_in_col + 1:]]

            #  Down
            queen_down = [f'{i}' for i in full_column[:index_in_col]]
            queen_down.reverse()

            # right
            queen_right = [f'{i}' for i in full_row[index_in_row + 1:]]

            # left
            queen_left = [f'{i}' for i in full_row[:index_in_row]]
            queen_left.reverse()

            # up right diagonal
            queen_up_right = self.get_diagonal(position, 'up_right')

            # down right diagonal
            queen_down_right = self.get_diagonal(position, 'down_right')

            # up left diagonal
            queen_up_left = self.get_diagonal(position, 'up_left')

            # down left diagonal
            queen_down_left = self.get_diagonal(position, 'down_left')
            # all
            all_possible_queen_moves = [queen_down_right] + [queen_right] + [queen_up_right] + [queen_up] + \
                                       [queen_up_left] + [queen_left] + [queen_down_left] + [queen_down]

            # legal moves
            legal_moves = self.get_all_legal_moves('queen', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_queen_moves, legal_moves)

            #return all_possible_queen_moves

        if piece == 'king':
            # clockwise pattern for king
            move_one = self.move_row(position, 'increase')
            move_two = self.move_column(self.move_row(position, 'increase'), 'increase')
            move_three = self.move_column(position, 'increase')
            move_four = self.move_row(self.move_column(position, 'increase'), 'decrease')
            move_five = self.move_row(position, 'decrease')
            move_six = self.move_row(self.move_column(position, 'decrease'), 'decrease')
            move_seven = self.move_column(position, 'decrease')
            move_eight = self.move_row(self.move_column(position, 'decrease'), 'increase')

            # all
            all_possible_king_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + \
                                      [move_six] + [move_seven] + [move_eight]
            all_possible_king_moves = [[move] for move in all_possible_king_moves if move is not None]

            # legal moves
            legal_moves = self.get_all_legal_moves('king', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_king_moves, legal_moves)

            #return all_possible_king_moves

        if piece == 'prawn' and piece_color == self.player_piece_color:
            up_one = self.move_row(position, 'increase')
            up_two = self.move_row(self.move_row(position, 'increase'), 'increase')

            if int(position[1]) >= 3:
                prawn_up = list(filter(self.remove_nones, [up_one]))
            else:
                prawn_up = list(filter(self.remove_nones, [up_one, up_two]))

            # diagonal
            right_diagonal = list(filter(self.remove_nones,
                                         [self.move_column(self.move_row(position, 'increase'), 'increase')]))
            left_diagonal = list(filter(self.remove_nones,
                                        [self.move_column(self.move_row(position, 'increase'), 'decrease')]))

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]

            # legal
            legal_moves = self.get_all_legal_moves('prawn', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_prawn_moves, legal_moves)

            #return all_possible_prawn_moves

        if piece == 'prawn' and piece_color == self.opponent_piece_color:
            # up
            down_one = self.move_row(position, 'decrease')
            down_two = self.move_row(self.move_row(position, 'decrease'), 'decrease')

            if int(position[1]) <= 6:
                prawn_up = list(filter(self.remove_nones, [down_one]))
            else:
                prawn_up = list(filter(self.remove_nones, [down_one, down_two]))

            # diagonal
            right_diagonal = list(filter(self.remove_nones,
                                         [self.move_column(self.move_row(position, 'decrease'), 'increase')]))
            left_diagonal = list(filter(self.remove_nones,
                                        [self.move_column(self.move_row(position, 'decrease'), 'decrease')]))

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]

            # legal moves
            legal_moves = self.get_all_legal_moves('prawn', position)

            # moves based on legal moves and all possible moves
            final = self.remove_illegal_moves(all_possible_prawn_moves, legal_moves)

            #return all_possible_prawn_moves

        print(self.ai_board.legal_moves)
        return final

    @staticmethod
    def remove_illegal_moves(all_possible_moves, legal_moves):
        """Delete illegal moves from all generated moves by filtering"""

        all_moves = []
        for move_set in all_possible_moves:
            temp = []
            for move in move_set:
                if move in legal_moves:
                    temp.append(move)
            all_moves.append(temp)

        #print(f'All moves: {all_possible_moves}\nFiltered from legal moves: {legal_moves}\n\nResulting in: {all_moves}')

        return all_moves

    def get_piece_img(self):
        """Easy way to access file paths for pieces

        :returns: A dictionary containing the file paths for the chess pieces, thus making them easily accessible
        :rtype: dict
        """

        # default, fantasy, spatial
        pieces_path = self.pieces_file_path + f'\\{self.piece_format}'

        # Get the name for all the black pieces and white pieces paths in lists
        # Format of each piece name is 'piece.png'
        black = [piece for (root, dirs, piece) in os.walk(pieces_path + '\\black')]
        white = [piece for (root, dirs, piece) in os.walk(pieces_path + '\\white')]

        # Create a dictionary were the key is the name of the piece and the value is the file path
        # Each loop in the list comprehension returns the file path e.g. 'piece.png'
        # To shorten this we slice this name and remove 4 characters from the end: '.png' in the key
        # The value is simply the full path
        black_pieces = {f'{str(piece[:len(piece) - 4])}':
                            f'{pieces_path}\\black\\{piece}' for piece in black[0]}
        white_pieces = {f'{str(piece[:len(piece) - 4])}':
                            f'{pieces_path}\\white\\{piece}' for piece in white[0]}

        # We return both lists, now we can access any image
        # For example, black rook would be 'black_pieces['rook']', this returns its file path

        return black_pieces, white_pieces

    @staticmethod
    def remove_nones(val):
        """Remove None from array

        :param str val: Value

        :returns: val if not None, else False
        :rtype: bool, str
        """
        if val is None:
            return False

        else:
            return val

    def get_game_fen_string_original(self):
        """Get game fen string from board dict

        :returns: fen string for the current board position
        :rtype: str
        """

        # classify board through pieces and spaces (represented as str '1')
        first_list = []
        i = 0
        copy_of_board = self.board
        for position in self.pieces_reversed:
            if copy_of_board[position]['piece']['piece_name'] is None:
                first_list.append('1')
            else:
                if copy_of_board[position]['piece']['piece_color'] == 'black':
                    if copy_of_board[position]['piece']['piece_name'] == 'knight':
                        letter = 'N'
                    else:
                        letter = copy_of_board[position]['piece']['piece_name'][0].upper()
                    first_list.append(letter)
                else:
                    if copy_of_board[position]['piece']['piece_name'] == 'knight':
                        letter = 'n'

                    else:
                        letter = copy_of_board[position]['piece']['piece_name'][0].lower()
                    first_list.append(letter)

            i += 1
            if i == 8:
                first_list.append('/')
                i = 0

        # make 2d array of this list where each list is a rank
        temp = []
        second_list = []
        for i in first_list:
            if i == '/':
                second_list.append(temp)
                temp = []
            temp.append(i)

        # solution to last element auto deleting bug
        second_list += ['/', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', '1']

        # classify each row by spaces and pieces
        main = []
        third_list = []
        count = 0
        for row in second_list:
            for value in row:
                if value == '1':
                    count += 1
                if value != '1':
                    if count != 0:
                        third_list.append(str(count))
                    third_list.append(value)
                    count = 0
            main.append(third_list)

        last_index = len(third_list) - 1 - third_list[::-1].index('/')
        final_fen = ''.join(third_list[:last_index])

        return final_fen

    def move_row(self, position, operation):
        """Returns position above to or below parameter

        :param str position: chessboard coordinate
        :param str operation: To help determine whether to return position above or under current one e.g.
        for 'b4' it would be 'b5' for increase and 'b3' for decrease

        :return: if coordinate not out of chess board margins return list of of the one chess coordinate
        above or under the provided one,  else return None
        :rtype: string
        """

        # ensure chess position is entered
        if position in self.pieces:
            if operation == 'increase':
                # '8' shouldn't be in the position, because it is the highest row there is, so it can't be increased
                if '8' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index + 8]

            if operation == 'decrease':
                # '2' shouldn't be in the position, because it is the lowest row there is, so it can't be decreased
                if '1' in position:
                    return
                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index - 8]
        else:
            return

    def move_column(self, position, operation):
        """Returns position next to or behind parameter

        :param str position: chessboard coordinate
        :param str operation: To help determine whether to return position ahead or behind current one e.g.
        for 'b4' it would be 'c4' for increase and 'a4' for decrease

        :return: if coordinate not out of chess board margins return list of of the one chess coordinate
        next or behind the provided one,  else return None
        :rtype: string
        """

        # ensure chess position is entered
        if position in self.pieces:

            if operation == 'increase':
                # 'h' shouldn't be in the position, because it is the last element in a row, so it can't be increased
                if 'h' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index + 1]

            if operation == 'decrease':
                # 'a' shouldn't be in the position, because it is the first element in a row, so it can't be decreased
                if 'a' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index - 1]
        else:
            return

    def get_diagonal(self, position, direction):
        """Returns diagonal for a specific position on chessboard

        :param str position: chessboard coordinate
        :param str direction: The direction in which the diagonal will be generated

        :return: list of all the possible moves in a certain diagonal
        :rtype: list
        """

        # lists
        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        list_position = list(position)

        # basically how many columns there are in each direction from the position
        columns_to_right = letters[list_position[0]] + 8
        columns_to_left = letters[list_position[0]]

        diagonal_values = []

        if direction == 'up_right':

            next_diagonal = position
            for i in range(columns_to_right):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'increase'), 'increase')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'down_right':

            next_diagonal = position
            for i in range(columns_to_right):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'increase'), 'decrease')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'up_left':
            next_diagonal = position
            for i in range(columns_to_left):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'decrease'), 'increase')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'down_left':
            next_diagonal = position
            for i in range(columns_to_left):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'decrease'), 'decrease')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

    def build(self, board_type='default', **kwargs):
        """Construct board

        :param board_type: Determines the type of board the user wants to build, defaults to 'default'
        :type board_type: str, optional
        """

        if board_type == 'default':
            self.place_buttons()
            self.place_default_pieces_on_screen()

        if board_type == 'empty':
            self.place_buttons()
            for piece in self.pieces:
                self.place_piece('blank', 'blank', piece)

        if board_type == 'saved':
            self.place_buttons()
            self.place_fen_string(kwargs['fen'])
            # ai board
            # Initialize chess board lib fen
            self.ai_board.set_board_fen(kwargs['fen'])

        # Console
        print('Chess lib board:')
        print(self.ai_board)
        print()
        print('My board')
        print(self)

        #print(self.locate_piece('prawn', 'black'))

    def __str__(self):
        """Returns a text based unicode representation of game"""

        # unicode for pieces
        # lowercase represents white, black represents uppercase
        # site where I got them from: https://altcodeunicode.com/alt-codes-chess-symbols/
        unicode_pieces_dict = {'r': u'\u2656', 'n': u'\u2658', 'b': u'\u2657', 'q': u'\u2655', 'k': u'\u2654',
                               'p': u'\u2659', 'R': u'\u265C', 'N': u'\u265E', 'B': u'\u265D', 'Q': u'\u265B',
                               'K': u'\u265A', 'P': u'\u265F', 'separator': u'\u4E00', 'edge': u'\u007C'}

        # col count
        x = 0
        # spaces and edges
        separator = ' ' + unicode_pieces_dict['separator'] + ' '
        side_edge = unicode_pieces_dict['edge']
        height_edge = unicode_pieces_dict['separator'] * 19

        # boards str add top border
        board_str = f'{height_edge}\n'

        for pos, val in self.board.items():
            # left border vert line
            if x == 0:
                board_str += f'{side_edge}'

            # current piece name
            current_p = 'n' if val['piece']['piece_name'] == 'knight' else val['piece']['piece_name']
            # take first letter if it is a piece if not make it blank space (with separator)
            piece = separator if current_p is None else current_p[0]

            # if it is a piece
            if piece != separator:
                # 'letter' is a single letter. Upper or lowercase depending on color
                letter = str(current_p[0]).upper() if val['piece']['piece_color'] == 'black' \
                    else str(current_p[0]).lower()

                # piece unicode str
                piece = ' ' + str(unicode_pieces_dict[letter]) + ' '

            # add piece to board str
            board_str += piece

            # if x is not ignore else restart to 0 and create new row
            x += 1
            if x == 8:
                board_str += f'{side_edge}\n'
                x = 0

        # add bottom border
        board_str += height_edge

        return board_str
