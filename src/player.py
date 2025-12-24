import pygame

from piece import Piece

class Player:
    def __init__(self, color):
        shape1 = [
            [1]
        ]

        self.piece1 = Piece(shape1, (0,0), color)