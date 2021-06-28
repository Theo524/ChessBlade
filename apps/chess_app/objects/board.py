from tkinter import *
from tkinter import messagebox
import string
import os
from PIL import Image, ImageTk
from tkinter import ttk
import csv


class Board(Frame):
    # Game attributes
    player_one_turn = True
    player_two_turn = False
    AI_turn = False
    moves = 1

    # Trackers
    chess_notation = []
    deleted_pieces = []
    tracker = []
    # ai_board = []

    # data
    board = {}
    coordinates = []

    def __init__(self, master, widgets_frame):
        Frame.__init__(self, master, widgets_frame)

        # game settings variables (retrieve settings from files)
        with open(os.getcwd() + '\\apps\\login_system_app\\temp\\mode.txt', 'r') as f:
            game_mode = f.read()

        if game_mode == 'guest':

            # open default settings file
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    print(row)
                    # retrieve settings in file
                    difficulty = row[0]
                    time = row[1]
                    game_type = row[2]
                    player_piece_color = row[3]
                    opponent_piece_color = row[4]
                    border_color = row[5]
                    board_color = row[6]

        elif game_mode == 'user':
            # fetch settings for that specific user
            with open(os.getcwd() + '\\apps\\chess_app\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    # retrieve these personalized settings from user file
                    difficulty = row[0]
                    time = row[1]
                    game_type = row[2]
                    player_piece_color = row[3]
                    opponent_piece_color = row[4]
                    border_color = row[5]
                    board_color = row[6]

        # border
        self.configure(highlightthickness=2, highlightbackground=border_color)

        # colors for board
        self.board_colors = [
                           'white', board_color, 'white', board_color, 'white', board_color, 'white', board_color,
                           board_color, 'white', board_color, 'white', board_color, 'white', board_color, 'white',
                       ] * 4

        # file paths
        self.pieces_file_path = os.getcwd() + '\\apps\\chess_app\\pieces'
        self.settings_file_path = os.getcwd() + '\\apps\\chess_app\\all_settings'

        # list containing letters from a to h
        self.letters = list(string.ascii_lowercase[:8])
        self.alphabet = list(string.ascii_letters)

        # nums str
        self.nums = [str(i) for i in range(10)]

        # Will store pieces coordinates in 1d array
        self.pieces = []

        # Dictionaries storing piece images file names
        self.black_pieces, self.white_pieces = self.get_piece_img()

        # methods to implement game visuals
        # ---------------NOTEBOOK--------------
        # notebook for chess notation
        self.notebook = ttk.Notebook(widgets_frame, height=400, width=500)
        self.notebook.pack(pady=(7, 0), padx=5)
        # first tab
        self.notation_tab = Text(self.notebook, width=40, height=10)
        self.notation_tab.pack()

        # second tab
        self.deleted_pieces_tab = Text(self.notebook, width=40, height=10)
        self.deleted_pieces_tab.pack()

        # add both tabs to chess notebook
        self.notebook.add(self.notation_tab, text='Notation')
        self.notebook.add(self.deleted_pieces_tab, text='Deleted')

    def make_board(self):
        """Make the board dict"""

        # get coordinates, e.g. 'a1', 'b1', etc into a 2 dimensional array
        for row in range(8):
            temp = []
            for letter in self.letters:
                temp.append(f'{letter}{row + 1}')
            self.coordinates.append(temp)

        # Create a dictionary with the main key being a coordinate
        # Assign coordinates to their corresponding button
        x = 0
        y = 7
        # repeat 64 times (number of coordinates in chess)
        for i in range(len(self.board_colors)):
            # Store the current coordinate in a variable e.g in the first iteration it represents a8
            # in terms of y and x (from self.coordinates)
            current_position = self.coordinates[y][x]

            # Append the current coordinate to a similar list, but this time it is one dimensional
            self.pieces.append(current_position)

            # Essential part
            # Adds a new value to the empty dictionary 'self.board'
            # The main key (current_position) is the current coordinate, 'a8' in the first iteration
            # Format for future reference ('<>' represents a class object, '--' represent values, '' represent the keys)
            # dict = {'coordinate': {'button': <Button object>,
            #                        'piece': {'piece name': --actual name of piece--, 'piece color': --piece color--},
            #                        'color': --color of the button--]}}
            self.board[current_position] = {'button': Button(self, bg=self.board_colors[i],
                                                             text=f'\t        {current_position}',
                                                             font=('arial', 7),
                                                             compound=BOTTOM,
                                                             activebackground='light blue',
                                                             relief=SOLID,
                                                             highlightthickness=2,
                                                             cursor='tcross',
                                                             highlightbackground="black",
                                                             highlightcolor="black",
                                                             command=lambda p=current_position:
                                                             self.update_current_piece(p)),
                                            'piece': {'piece_name': None, 'piece_color': None},
                                            'color': self.board_colors[i],
                                            'selected': False
                                            }
            # illustration:
            # [[...],
            #  [a7, b7, c7, d7, e7, f7, g7, h7],
            #  [a8, b8, c8, d8, e8, f8, g8, h8]]
            # coordinates in first iteration are 'x=0, y=7', where the data is 'a8'
            # next coordinates are 'x=1, y=7' where the val is 'b8'
            # hence we move to the next item in the current list by adding 1 to x
            x += 1
            # Once we reach the end of the list, the x coordinate is 8, so we move up one in the y axis
            # by subtracting 1 (from 8 to 7 to 6 and so on...)
            if x == 8:
                y -= 1
                x = 0

    def place_default_pieces_on_screen(self):
        """Place default starting pieces on the screen"""

        # Thanks to the method 'place_piece' I've made, we can easily move and delete any piece from the screen
        # We enter the piece, the color and the position we want to place it at as parameters

        # use a FEN string (Forsyth-Edwards Notation)
        staring_fen_string = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.place_fen_string(staring_fen_string)


    def place_fen_string(self, fen_str):
        """Convert fen string to place pieces"""

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
                    color = 'white'
                elif piece in list(string.ascii_uppercase):
                    color = 'black'
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

    def update_current_piece(self, position):
        """Command assigned to every button, to move pieces,
        acts based on what button of the board what the player has clicked"""

        if self.tracker:
            print('\n-------------------TRACKER-------------------')
            print(self.tracker[-1])
            print('---------------END_OF_TRACKER----------------\n')

        # color of the button, piece and piece color the user just clicked
        current_button_color = self.board[position]['color']
        piece_name = self.board[position]['piece']['piece_name']
        piece_color = self.board[position]['piece']['piece_color']

        # HIGHLIGHTING MOVES
        # allowing turns (two player mode)
        # if self.game_type == 'two_player'
        if self.player_one_turn:
            if self.board[position]['piece']['piece_color'] == 'black':
                # if the button piece is black
                print('\n-------------------ACTION-------------------')
                print('Action: Player selected piece')
                print(f'Selected piece: {piece_name}')
                print(f'Piece color: {piece_color}')
                print('-------------------END-------------------')
                self.reset_board_colors()

                # We only allow black pieces to be highlighted

                # rooks
                if self.board[position]['piece']['piece_name'] == 'rook':
                    self.piece_highlighting(f'{position}', 'rook', 'black')

                # prawn
                if self.board[position]['piece']['piece_name'] == 'prawn':
                    self.piece_highlighting(f'{position}', 'prawn', 'black')

                # bishop
                if self.board[position]['piece']['piece_name'] == 'bishop':
                    self.piece_highlighting(f'{position}', 'bishop', 'black')

                # knight
                if self.board[position]['piece']['piece_name'] == 'knight':
                    self.piece_highlighting(f'{position}', 'knight', 'black')

                # queen
                if self.board[position]['piece']['piece_name'] == 'queen':
                    self.piece_highlighting(f'{position}', 'queen', 'black')

                # king
                if self.board[position]['piece']['piece_name'] == 'king':
                    self.piece_highlighting(f'{position}', 'king', 'black')

            # If the piece is white
            if self.board[position]['piece']['piece_color'] == 'white':
                print('\n-------------------ACTION-------------------')
                print('Action: Player selected piece')
                print(f'Selected piece: {piece_name}')
                print(f'Piece color: {piece_color}')
                print('-------------------END-------------------')
                self.reset_board_colors()

        if self.player_two_turn:
            if self.board[position]['piece']['piece_color'] == 'white':
                print('\n-------------------ACTION-------------------')
                print('Action: Player selected piece')
                print(f'Selected piece: {piece_name}')
                print(f'Piece color: {piece_color}')
                print('-------------------END-------------------')
                self.reset_board_colors()

                # We only allow white pieces to be highlighted

                # rooks
                if self.board[position]['piece']['piece_name'] == 'rook':
                    self.piece_highlighting(f'{position}', 'rook', 'white')

                # prawn
                if self.board[position]['piece']['piece_name'] == 'prawn':
                    self.piece_highlighting(f'{position}', 'prawn', 'white')

                # bishop
                if self.board[position]['piece']['piece_name'] == 'bishop':
                    self.piece_highlighting(f'{position}', 'bishop', 'white')

                # knight
                if self.board[position]['piece']['piece_name'] == 'knight':
                    self.piece_highlighting(f'{position}', 'knight', 'white')

                # queen
                if self.board[position]['piece']['piece_name'] == 'queen':
                    self.piece_highlighting(f'{position}', 'queen', 'white')

                # king
                if self.board[position]['piece']['piece_name'] == 'king':
                    self.piece_highlighting(f'{position}', 'king', 'white')

            # If the piece is black
            if self.board[position]['piece']['piece_color'] == 'black':
                print('\n-------------------ACTION-------------------')
                print('Action: Player selected piece')
                print(f'Selected piece: {piece_name}')
                print(f'Piece color: {piece_color}')
                print('-------------------END-------------------')
                self.reset_board_colors()

        # If the color of the button is green
        # It would mean the player had already clicked a piece previously which marked possible moves in green
        if current_button_color == 'light green':
            # Get the last piece clicked, to change pieces, from the end of the tracker
            # It can be retrieved because the tracker is only updated at the end of this function
            old_piece_name = self.tracker[-1]['selected_piece']['piece_name']
            old_piece_color = self.tracker[-1]['selected_piece']['piece_color']
            old_piece_position = self.tracker[-1]['player_clicked']

            # Console output
            print('\n-------------------ACTION-------------------')
            print('Action: Player made a move')
            print(f'Piece: {old_piece_name}')
            print(f'Destination: {old_piece_position}')
            print(f'Piece color: {old_piece_color}')
            print('-------------------END_OF_ACTION-------------------\n')

            # -------------NOTATION-------------
            # chess notation tracker(list)
            self.chess_notation.append(f'{old_piece_name[0].upper()}{position}')
            # The moves variable is updated every turn, so every even number of moves corresponds to a player
            # while every odd number of moves corresponds to the other player
            if self.moves % 2 == 0:
                # even number of moves, 'P2' used to mark player2
                self.notation_tab.insert('end', f'{self.moves}.(P2:{self.chess_notation[-1]}) ')
            else:
                # even number of moves, 'P1' used to mark player1
                self.notation_tab.insert('end', f'{self.moves}.(P1:{self.chess_notation[-1]}) ')

            # update number of moves
            self.moves += 1

            # ---------MOVEMENT---------
            # place a new piece with those attributes in the marked selected spot
            self.place_piece(old_piece_name, old_piece_color, position)
            # replace the place where that piece was with a blank space img
            self.place_piece('blank', 'blank', old_piece_position)

            # set all colors back normal (remove highlighting)
            self.reset_board_colors()

            # We now swap turns so only one side can make moves
            if self.moves % 2 == 0:
                self.player_two_turn = True
                self.player_one_turn = False
            else:
                self.player_two_turn = False
                self.player_one_turn = True

        # if the button clicked is red, that means the piece can be deleted
        if current_button_color == 'red':
            # Get the last piece clicked, to change piece
            old_piece_name = self.tracker[-1]['selected_piece']['piece_name']
            old_piece_color = self.tracker[-1]['selected_piece']['piece_color']
            old_piece_position = self.tracker[-1]['player_clicked']

            # Console output
            print('\n-------------------ACTION-------------------')
            print('Action: Player deleted a piece')
            print(f'Piece used: {old_piece_name}')
            print(f'Deleted piece: {piece_name}')
            print(f'PLayer piece color: {old_piece_color}')
            print('-------------------END_OF_ACTION-------------------\n')

            # --------NOTATION----------
            # This time we add an 'x' in the middle to show that a piece is being destroyed
            self.chess_notation.append(f'{old_piece_name[0].upper()}x{position}')

            # add the move to chess notation
            if self.moves % 2 == 0:
                self.notation_tab.insert('end', f'{self.moves}.(P2:{self.chess_notation[-1]}) ')
            else:
                self.notation_tab.insert('end', f'{self.moves}.(P1:{self.chess_notation[-1]}) ')

            # increase number of moves by one
            self.moves += 1

            # add this deleted piece to the deleted pieces list
            self.deleted_pieces.append([piece_name, piece_color])
            self.deleted_pieces_tab.insert('end', '(')
            self.deleted_pieces_tab.insert('end', self.board[position]['piece']['piece_color'])
            self.deleted_pieces_tab.insert('end', ', ')
            self.deleted_pieces_tab.insert('end', self.board[position]['piece']['piece_name'])
            self.deleted_pieces_tab.insert('end', '), ')

            # Replace pieces
            self.place_piece(old_piece_name, old_piece_color, position)
            self.place_piece('blank', 'blank', old_piece_position)

            # reset board colors
            self.reset_board_colors()

            # swap turns
            if self.moves % 2 == 0:
                self.player_two_turn = True
                self.player_one_turn = False
            else:
                self.player_two_turn = False
                self.player_one_turn = True

        # Whenever the user clicks a non piece or empty space
        # reset the board colors
        if current_button_color in ['white', 'black'] and piece_name is None:

            # message
            messagebox.showerror('Error', f'{position} is an invalid move')

            # Console output
            print('\n-------------------ACTION-------------------')
            print('Action: Player clicked an empty space')
            print(f'Position: {position}')
            print(f'Output: Reset board to normal')
            print('-------------------END-------------------\n')
            self.reset_board_colors()

        # Make AI board (Not done yet)
        # b = 0
        # temp = []
        # for val in self.board.keys():
        # temp.append(val)
        # b += 1
        # if b == 8:
        # b = 0
        # copy = temp[:]
        # self.ai_board.append(copy)
        # temp.clear()
        # print(self.ai_board)

        # Allows to track user history of clicks, appends the current move
        self.tracker.append({'player_clicked': position,
                             'selected_piece': self.board[position]['piece'],
                             'color': self.board[position]['color']})

    def reset_board_colors(self):
        """Reset board colors to normal(to eliminate highlighting)"""

        i = 0
        # iterate through the entire board and set the color of each button back to its corresponding one
        # by iterating over the board colors at the same time
        for position in self.pieces:
            self.board[position]['button'].configure(bg=self.board_colors[i],
                                                     relief=SOLID)
            self.board[position]['color'] = self.board_colors[i]
            i += 1

    def piece_highlighting(self, position, piece, piece_color):
        """Highlights all possible moves for a given piece"""

        # We highlight the piece color to blue, so it is evident what piece the user selected
        self.board[position]['button'].configure(bg='light blue')

        # rook
        if piece == 'rook':
            # rook moves horizontally and vertically in a straight line

            # The function returns a list of possible moves for the piece
            # 'self.get_all_possible_moves' is definitely the longest and hardest function I've made in this project
            all_possible_rook_moves = self.get_all_possible_moves('rook', 'none', position)

            if self.board[position]['piece']['piece_color'] == 'black':
                # black piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is not black
                        if self.board[position]['piece']['piece_color'] != 'black':
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white
                        if self.board[position]['piece']['piece_color'] == 'white':
                            # if it is white, highlight it with red so it becomes availible to delete
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'black' \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

            if self.board[position]['piece']['piece_color'] == 'white':
                # white piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is not white
                        if self.board[position]['piece']['piece_color'] != 'white':
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black
                        if self.board[position]['piece']['piece_color'] == 'black':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a white piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'white' \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

        # bishop
        if piece == 'bishop':
            # bishop moves diagonally in all directions
            all_possible_bishop_moves = self.get_all_possible_moves('bishop', 'white', position)

            if self.board[position]['piece']['piece_color'] == 'black':
                # black piece
                for move_pattern in all_possible_bishop_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == 'white':
                            # if enemy piece, highlight to red
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == 'black':
                            # if black piece stop highlighting
                            break

                        # if there is no piece, convert to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == 'white':

                for move_pattern in all_possible_bishop_moves:
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == 'black':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == 'white':
                            break

                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # knight
        if piece == 'knight':
            # knight moves two blocks forward and marks the side in all directions
            all_possible_knight_moves = self.get_all_possible_moves('knight', 'none', position)

            if self.board[position]['piece']['piece_color'] == 'black':
                # black piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is white, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == 'white':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # if the piece is black, move to the next move
                        if self.board[position]['piece']['piece_color'] == 'black':
                            continue

                        # if there is no piece, highlight and mark green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == 'white':
                # white piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is black, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == 'black':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # if the piece is white, move to the next move
                        if self.board[position]['piece']['piece_color'] == 'white':
                            continue

                        # if there is no piece, highlight and mark green green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # queen
        if piece == 'queen':
            # queen moves are just a combination of a rook and a bishop
            all_possible_queen_moves = self.get_all_possible_moves('queen', 'none', position)

            if self.board[position]['piece']['piece_color'] == 'black':
                # black piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == 'white':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'black':
                            break

            if self.board[position]['piece']['piece_color'] == 'white':
                # white piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == 'black':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'white':
                            break

        if piece == 'king':
            all_possible_king_moves = self.get_all_possible_moves('king', 'none', position)

            if self.board[position]['piece']['piece_color'] == 'black':
                # black piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == 'white':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'black':
                            continue

            if self.board[position]['piece']['piece_color'] == 'white':
                # white piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == 'black':
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == 'white':
                            continue

        # prawns
        if piece_color == 'black' and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', 'black', position)
            print(position)
            print(all_prawns)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            right_diagonal = all_prawns[1]
            left_diagonal = all_prawns[2]

            for position in prawn_up:
                # only loops twice, e.g. 'e5' would generate 'e6' and 'e7'

                # if white or black piece stop highlight
                if self.board[position]['piece']['piece_color'] in ['white', 'black']:
                    break

                # else highlight as green
                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # left diagonal is just one position e.g. for 'b2' it would be 'b1'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == 'white':
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # right diagonal is just one position e.g. for 'b2' it would be 'b3'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == 'white':
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

        if piece_color == 'white' and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', 'white', position)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            left_diagonal = all_prawns[1]
            right_diagonal = all_prawns[2]

            for position in prawn_up:
                # if the piece is white we stop highlighting
                if self.board[position]['piece']['piece_color'] in ['white', 'black']:
                    break

                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # if the piece is black, highlight red
                if self.board[position]['piece']['piece_color'] == 'black':
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # if the piece is black, highlight to red
                if self.board[position]['piece']['piece_color'] == 'black':
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

    def place_piece(self, piece, color, position):
        """Placement of pieces"""

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

    def get_all_possible_moves(self, piece, piece_color, position):
        """Generates a list of all possible moves for a piece basedon its color and board position"""
        # represent a list of the position itself e.g a8 would be ['a', '8']

        # With this list we can get the new positions for this move by modifying only one part
        temp = list(position)

        full_column = [f'{temp[0]}{i}' for i in range(1, 9)]
        full_row = [f'{letter}{temp[1]}' for letter in self.letters]

        index_in_col = full_column.index(position)
        index_in_row = full_row.index(position)

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

            return all_possible_rook_moves

        if piece == 'bishop':

            # up right diagonal
            up_right = [i for i in full_row[index_in_row + 1:]]
            bishop_up_right = self.get_diagonal(up_right, 'go up')

            # down right diagonal
            down_right = [i for i in full_row[index_in_row + 1:]]
            bishop_down_right = self.get_diagonal(down_right, 'go down')

            # up left diagonal
            up_left = [i for i in full_row[:index_in_row]]
            up_left.reverse()
            bishop_up_left = self.get_diagonal(up_left, 'go up')

            # down left diagonal
            down_left = [i for i in full_row[:index_in_row]]
            down_left.reverse()
            bishop_down_left = self.get_diagonal(down_left, 'go down')

            # all
            all_possible_bishop_moves = [bishop_up_right] + [bishop_down_right] + \
                                        [bishop_up_left] + [bishop_down_left]

            return all_possible_bishop_moves

        if piece == 'knight':
            # Generate moves, by moving positions in board (clockwise)
            move_one = self.move_column(self.move_row(self.move_row([position], 'increase'), 'increase'), 'increase')
            move_two = self.move_row(self.move_column(self.move_column([position], 'increase'), 'increase'), 'increase')

            move_three = self.move_row(self.move_column(self.move_column([position], 'increase'), 'increase'),
                                       'decrease')
            move_four = self.move_column(self.move_row(self.move_row([position], 'decrease'), 'decrease'), 'increase')

            move_five = self.move_column(self.move_row(self.move_row([position], 'decrease'), 'decrease'), 'decrease')
            move_six = self.move_row(self.move_column(self.move_column([position], 'decrease'), 'decrease'), 'decrease')

            move_seven = self.move_row(self.move_column(self.move_column([position], 'decrease'), 'decrease'),
                                       'increase')
            move_eight = self.move_column(self.move_row(self.move_row([position], 'increase'), 'increase'), 'decrease')

            all_possible_knight_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + \
                                        [move_six] + [move_seven] + [move_eight]

            return all_possible_knight_moves

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
            up_right = [i for i in full_row[index_in_row + 1:]]
            queen_up_right = self.get_diagonal(up_right, 'go up')

            # down right diagonal
            down_right = [i for i in full_row[index_in_row + 1:]]
            queen_down_right = self.get_diagonal(down_right, 'go down')

            # up left diagonal
            up_left = [i for i in full_row[:index_in_row]]
            up_left.reverse()
            queen_up_left = self.get_diagonal(up_left, 'go up')

            # down left diagonal
            down_left = [i for i in full_row[:index_in_row]]
            down_left.reverse()
            queen_down_left = self.get_diagonal(down_left, 'go down')

            # all
            all_possible_queen_moves = [queen_down_right] + [queen_right] + [queen_up_right] + [queen_up] + \
                                       [queen_up_left] + [queen_left] + [queen_down_left] + [queen_down]

            return all_possible_queen_moves

        if piece == 'king':
            # clockwise pattern for king
            move_one = self.move_row([position], 'increase')
            move_two = self.move_column(self.move_row([position], 'increase'), 'increase')
            move_three = self.move_column([position], 'increase')
            move_four = self.move_row(self.move_column([position], 'increase'), 'decrease')
            move_five = self.move_column([position], 'decrease')
            move_six = self.move_row(self.move_column([position], 'decrease'), 'decrease')
            move_seven = self.move_column([position], 'decrease')
            move_eight = self.move_row(self.move_column([position], 'decrease'), 'increase')

            # all
            all_possible_king_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + \
                                      [move_six] + [move_seven] + [move_eight]

            return all_possible_king_moves

        if piece == 'prawn' and piece_color == 'black':
            up_one = self.move_row([position], 'increase')
            up_two = self.move_row(self.move_row([position], 'increase'), 'increase')
            prawn_up = [up_one[0], up_two[0]]
            print(prawn_up)

            # diagonal
            right_diagonal = self.move_column(self.move_row([position], 'increase'), 'increase')
            left_diagonal = self.move_column(self.move_row([position], 'increase'), 'decrease')

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]

            # all
            return all_possible_prawn_moves

        if piece == 'prawn' and piece_color == 'white':
            # up
            down_one = self.move_row([position], 'decrease')
            down_two = self.move_row(self.move_row([position], 'decrease'), 'decrease')
            prawn_up = [down_one[0], down_two[0]]

            # diagonal
            right_diagonal = self.move_column(self.move_row([position], 'decrease'), 'increase')
            left_diagonal = self.move_column(self.move_row([position], 'decrease'), 'decrease')

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]

            # all
            return all_possible_prawn_moves

    def get_piece_img(self):
        """Easy way to access file paths for pieces"""

        # Get the name for all the black pieces and white pieces paths in lists
        # Format of each piece name is 'piece.png'
        black = [piece for (root, dirs, piece) in os.walk(self.pieces_file_path + '//black')]
        white = [piece for (root, dirs, piece) in os.walk(self.pieces_file_path + '//white')]

        # Create a dictionary were the key is the name of the piece and the value is the file path
        # Each loop in the list comprehension returns the file path e.g. 'piece.png'
        # To shorten this we slice this name and remove 4 characters from the end: '.png' in the key
        # The value is simply the full path
        black_pieces = {f'{str(piece[:len(piece) - 4])}':
                        f'{self.pieces_file_path}\\black\\{piece}' for piece in black[0]}
        white_pieces = {f'{str(piece[:len(piece) - 4])}':
                        f'{self.pieces_file_path}\\white\\{piece}' for piece in white[0]}

        # We return both lists, now we can access any image
        # For example, black rook would be 'black_pieces['rook']', this returns its file path
        return black_pieces, white_pieces

    @staticmethod
    def move_row(array, operation):
        """Allows to increase or decrease a column of chess coordinates by one"""

        # the new increased/decreased list
        new_array = []

        count = 1
        if operation == 'increase':
            # increase operation
            for coordinate in array:
                # divide the position e.g. b5 into a list ['b', '5']
                # to manipulate each part individually
                coordinates = list(coordinate)

                # take the numeric part and increase it by one
                new_coordinate = str(int(coordinates[1]) + count)
                if new_coordinate == '9':
                    break

                # append new value to array
                new_array.append(coordinate[0] + new_coordinate)
                count += 1

        count = 1
        if operation == 'decrease':
            # decrease operation
            for coordinate in array:
                # divide the position e.g. b5 into a list ['b', '5']
                # to manipulate each part individually
                coordinates = list(coordinate)

                # take the numeric part and increase it by one
                new_coordinate = str(int(coordinates[1]) - count)
                if new_coordinate == '0':
                    break

                # append new value to array
                new_array.append(coordinate[0] + new_coordinate)
                count += 1

        # return full new array
        return new_array

    def move_column(self, array, operation):
        """Allows to increase or decrease a row of chess coordinates by one"""

        # the new increased/decreased list
        new_array = []

        count = 1
        if operation == 'increase':
            # increase operation
            for coordinate in array:
                # divide the position e.g. b5 into a list ['b', '5']
                # to manipulate each part individually
                coordinates = list(coordinate)

                letter_index = self.letters.index(str(coordinates[0]))

                # if we reach the endpoint 'h' which is index 7, break
                if letter_index == 7:
                    break

                # take the letter part and increase it by one
                new_letter = self.letters[letter_index + 1]

                # append new value to array
                new_array.append(new_letter + coordinate[1])
                count += 1

        count = 1
        if operation == 'decrease':
            # decrease operation
            for coordinate in array:
                # divide the position e.g. b5 into a list ['b', '5']
                # to manipulate each part individually
                coordinates = list(coordinate)

                letter_index = self.letters.index(str(coordinates[0]))

                # if we reach the endpoint 'a' which is index 0, break
                if letter_index == 0:
                    break

                # take the letter part and increase it by one
                new_letter = self.letters[letter_index - 1]

                # append new value to array
                new_array.append(new_letter + coordinate[1])
                count += 1

        # return full new array
        return new_array

    @staticmethod
    def get_diagonal(array, direction):
        value = 1
        new_array = []
        if direction == 'go up':
            for pos in array:
                coordinate = list(pos)
                new_val = int(coordinate[1]) + value
                if new_val == 9:
                    break
                new_array.append(coordinate[0] + str(new_val))
                value += 1

        if direction == 'go down':
            for pos in array:
                coordinate = list(pos)
                new_val = int(coordinate[1]) - value
                if new_val == 0:
                    break
                new_array.append(coordinate[0] + str(new_val))
                value += 1

        return new_array

    def build(self):
        self.make_board()
        self.place_default_pieces_on_screen()
        self.place_buttons()
