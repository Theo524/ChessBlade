from tkinter import *
from app.chess_app.objects.board import Board

# build an empty board and place pieces wherever you want
root = Tk()
root.mode = 'guest'
root.resizable(0, 0)
board_frame = Frame(root)
board_frame.pack()

# board
board = Board(board_frame)
board.build(board_type='empty')

# Place random pieces on board like this (start with black piece for movement)
board.place_piece('queen', 'black', 'c5')


board.pack()
root.mainloop()
