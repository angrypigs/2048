import pygame
import random

from src.utils import *
from src.block import Block
from src.board import Board



class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((251, 248, 239))
        pygame.draw.rect(self.background,
                         (187, 173, 160),
                         (X_CORNER, Y_CORNER, 800, 800),
                         0, 15)
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.background,
                                 (204, 192, 179),
                                 (X_CORNER + 16 + 196 * i, 
                                  Y_CORNER + 16 + 196 * j,
                                  180, 180),
                                  0, 8)
        self.blocks : list[Block] = []
        self.board = Board()
        self.new_game()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def draw_game(self) -> None:
        self.screen.blit(self.background, (0, 0))
        for block in self.blocks:
            block.draw()
    
    def new_game(self) -> None:
        self.blocks.clear()
        for y, x in self.board.reset_board():
            val = self.board.matrix[y][x]
            self.blocks.append(
                Block(
                    self.screen,
                    val,
                    get_color(val),
                    get_font_color(val),
                    (
                        X_CORNER + 16 + 196 * x, 
                        Y_CORNER + 16 + 196 * y
                    )
                )
            )