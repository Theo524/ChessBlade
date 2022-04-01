import random
from tkinter import *
from tkinter import messagebox
from app.chess_app.chess_app_widgets.board import MainChessBoard
import time
import threading


# games
class GuessCoordinate(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.mode = 'guest'
        self.title('Guess the coordinate')
        self.resizable(0, 0)

        # variables
        position_var = StringVar()
        score_var = IntVar()
        time_var = StringVar()
        time_var.set('15')

        # start btn new
        start_button = Button(self, text='Start New Game', cursor='hand2')
        start_button.pack()

        # score AND TIME
        upper_frame = Frame(self, height=10)
        upper_frame.pack(pady=10)

        left_frame = Frame(upper_frame)
        middle_frame = Frame(upper_frame)
        right_frame = Frame(upper_frame)

        time_label_1 = Label(left_frame, text='Time left:', font='arial 15 bold')
        time_label_1.pack(side=LEFT)
        time_label_2 = Label(left_frame, textvariable=time_var, font='arial 15')
        time_label_2.pack(side=LEFT)

        # SCORE
        score_text_1 = Label(right_frame, text='Score:', font='arial 15 bold')
        score_text_2 = Label(right_frame, textvariable=score_var, font='arial 15')
        score_text_2.pack(side=RIGHT)
        score_text_1.pack(side=RIGHT)

        # board
        background = Frame(self)
        background.pack()
        self.board_frame = TrainerBoard(master=background, game='guess the coordinate', position_var=position_var,
                                        score_var=score_var, time_var=time_var, start_button=start_button)
        self.board_frame.build(board_type='empty')
        self.board_frame.pack()
        self.board_frame.enable_board_buttons(False)  # disable board buttons

        # question
        self.lower_frame = Frame(self, height=30)
        self.lower_frame.pack()
        self.positions = self.board_frame.pieces  # list of all chess positions
        position_var.set(random.choice(self.positions))
        position_to_locate_label_1 = Label(middle_frame, text='Locate:', font='arial 15 bold')
        position_to_locate_label_1.pack(side=LEFT)
        position_to_locate_2 = Label(middle_frame, textvariable=position_var, font='arial 15')
        position_to_locate_2.pack(side=LEFT)

        # text frames
        left_frame.pack(side=LEFT, padx=50)
        middle_frame.pack(side=LEFT)
        right_frame.pack(side=LEFT, padx=50)


class FindCheckmateOneMove(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.title('Mate in 1 move')
        self.resizable(0, 0)

        # 1 move challenges
        one_move_fen_str = ['4k3/R7/7R/4Q3/8/8/8/8', '4k3/8/3Q4/8/7B/8/8/4K3',
                            'rnbqkbnr/2pp1ppp/pp6/4p2K/2B1P3/8/PPPP1PPP/RNB1K1NR']

        random_fen = random.choice(one_move_fen_str)
        self.board = FindCheckMateBoard(self, game='1 move', fen=random_fen)
        self.board.build(board_type='empty')
        self.board.pack()

        # type of game(1 move checkmate, 2 move checkmate etc)
        self.board.place_fen_string(random_fen)


class FindCheckmateTwoMoves(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Mate in 2 moves')
        self.resizable(0, 0)

        # 2 move challenges
        two_move_fen_str = ['8/4k3/R7/7R/8/8/8/4K3']

        random_fen = random.choice(two_move_fen_str)

        self.board = FindCheckMateBoard(self, game='2 move', fen=random_fen)
        self.board.build(board_type='empty')
        self.board.pack()

        # type of game(1 move checkmate, 2 move checkmate etc)
        self.board.place_fen_string(random_fen)


# boards
class TrainerBoard(MainChessBoard):
    def __init__(self, master, **kwargs):
        MainChessBoard.__init__(self, master=master)

        # button clicked
        self.current_btn = []

        # change what the board buttons do when clicked
        self.change_buttons_command_mini_games()

        self.enable_board_buttons(False)

        if kwargs['game']:
            self.game = kwargs['game']

        if kwargs['position_var']:
            self.position_var = kwargs['position_var']

        if kwargs['score_var']:
            self.score_var = kwargs['score_var']

        if kwargs['time_var']:
            self.time_var = kwargs['time_var']

        if kwargs['start_button']:
            self.start_button = kwargs['start_button']
            self.start_button.configure(command=self.thread)

    def change_buttons_command_mini_games(self):
        """Changes command for every piece in the board for mini games
        """

        coordinates = self.coordinates[:]
        coordinates.reverse()
        # iterate through the entire board and set the buttons command
        for row in coordinates:
            for position in row:
                self.board[position]['button'].configure(command=lambda p=position: self.get_btn_data(p))
                self.board[position]['button'].configure(text='')

    def get_btn_data(self, position):
        """Data for current button"""

        data = [position, self.board[position]['piece']]
        self.current_btn = data

        # compare if they got it right
        target_pos = self.position_var.get()
        user_response = data[0]

        if self.game == 'guess the coordinate':
            if user_response == target_pos:
                new_score = self.score_var.get() + 1
                self.score_var.set(new_score)
                self.time_var.set('15')

            else:
                messagebox.showerror('Incorrect', f'That\'s not {target_pos}')

            # new position
            position = random.choice(self.pieces)
            self.position_var.set(position)

    def thread(self):
        thread = threading.Thread(target=self.thread_timer)
        thread.start()

    def thread_timer(self):
        """Thread that deals with background game timer

        The user can use this to see how long the game took
        """
        self.enable_board_buttons(True)  # disable board buttons
        self.start_button['state'] = 'disable'

        # convert time str from db to seconds
        self.time_var.set('15')
        for i in range(1000):
            # actual timer
            time.sleep(1)
            new_time = int(self.time_var.get()) - 1
            self.time_var.set(new_time)
            if new_time <= 0:
                messagebox.showerror('Game over', f'Game over. You got {self.score_var.get()} position(s) right.\n '
                                                  f'Enter Start to play again.')
                self.score_var.set(0)
                break

        self.start_button['state'] = 'normal'


class FindCheckMateBoard(MainChessBoard):
    # A board where the user can freely move and has to get checkmate based on a certain number of moves

    def __init__(self, master, game, fen):
        MainChessBoard.__init__(self, master)

        self.difficulty = 'Expert'
        self.game_type = 'computer'
        self.game = game
        self.fen = fen
        self.moves = 0

        self.set_fen()

    def set_fen(self):
        self.ai_board.set_fen(self.fen)

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
            messagebox.showinfo('Game over', f'Checkmate', parent=self.master)
            self.enable_board_buttons(False)
            return

        # STALEMATE
        if self.ai_board.is_stalemate():
            self.game_over = True
            messagebox.showinfo('Game over', f'Game ends in draw')

        if self.game == '1 move':
            if self.moves >= 1:
                self.game_over = True
                messagebox.showerror('Over', 'game over you only had 1 move', parent=self.master)
                self.enable_board_buttons(False)
                return

        if self.game == '2 move':
            if self.moves >= 3:
                self.game_over = True
                messagebox.showerror('Over', 'game over you only had 2 moves', parent=self.master)
                self.enable_board_buttons(False)
                return
