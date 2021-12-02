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









"""
board.place_piece('prawn', 'black', 'c5')
board.place_piece('prawn', 'black', 'e5')
board.place_piece('prawn', 'black', 'c4')
board.place_piece('prawn', 'black', 'e4')
board.place_piece('prawn', 'black', 'd4')
board.place_piece('prawn', 'black', 'c6')
board.place_piece('prawn', 'black', 'e6')
board.place_piece('prawn', 'black', 'd6')
"""



# enemy
#board.place_piece('rook', 'black', 'g8')
#board.place_piece('prawn', 'black', 'a2')
#board.place_piece('prawn', 'black', 'g2')
#board.place_piece('prawn', 'black', 'b7')



board.pack()


root.mainloop()
















import string
#flat, groove, -raised, ridge, solid, or sunken
"""
font = ('calibri', 20 )
root = Tk()
root.title('Button styles')
Button(root, text='Default', font=font).pack(pady=5, padx=5, side=LEFT)

Button(root, text='FLAT', relief=FLAT, font=font).pack(pady=5, padx=5, side=LEFT)

Button(root, text='GROOVE', relief=GROOVE, font=font).pack(pady=5, padx=5, side=LEFT)

Button(root, text='RIDGE', relief=RIDGE, font=font).pack(pady=5, padx=5, side=LEFT)

Button(root, text='SOLID', relief=SOLID, font=font).pack(pady=5, padx=5, side=LEFT)

Button(root, text='SUNKEN', relief=SUNKEN, font=font).pack(pady=5, padx=5, side=LEFT)

root.mainloop()
"""