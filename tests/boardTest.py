import unittest
from tkinter import Tk, Frame
import tkinter
from app.chess_app.objects.board import Board
import chess


class MyTestCase(unittest.TestCase):
    def test_00_add_chess_pieces_positions(self):

        coordinates, pieces, pieces_reversed = board_obj.add_chess_pieces_positions()

        coordinates_match = [['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'],
                             ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                             ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
                             ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
                             ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
                             ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
                             ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
                             ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']]

        pieces_match = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

        pieces_reversed_match = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                                 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                                 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                                 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                                 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                                 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                                 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                                 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

        self.assertListEqual(coordinates, coordinates_match)
        self.assertListEqual(pieces, pieces_match)
        self.assertListEqual(pieces_reversed, pieces_reversed_match)

    def test_01_get_game_settings(self):

        settings_usr = board_obj.get_game_settings('user')
        settings_guest = board_obj.get_game_settings('guest')

        self.assertEqual(len(settings_guest), 7)
        self.assertEqual(len(settings_usr), 7)

    def test_02_board_building(self):

        board = board_obj.board  #

        # check all keys are correct
        pieces = board_obj.pieces_reversed
        valid_key, valid_button, i = 0, 0, 0
        for board_tuple in list(board.items()):
            if board_tuple[0] == pieces[i]:
                valid_key += 1

            if isinstance(type(board_tuple[1]['button']), type(tkinter.Button)):
                valid_button += 1
            i += 1

        self.assertEqual(len(board), 64)
        self.assertEqual(valid_button, 64)
        self.assertEqual(valid_key, 64)


obj_1 = Tk()
obj_1.mode = 'guest'
obj_2 = Frame(obj_1)
board_obj = Board(obj_2)
