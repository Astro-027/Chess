import pygame
from pathlib import Path

import constants.py
import player.py
import piece.py

class Rook(Piece):

    @staticmethod #TODO make a static variable
    _ways_to_move = [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')]

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Rook.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Rook.png')
        return pygame.image.load(piece_path)
