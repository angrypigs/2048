import pygame
from pygame.math import Vector2
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
        self.blocks_to_remove : list[Block] = []
        self.coords_to_create = None
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not any(self.blocks):
                        self.handle_board_response(self.board.move_left())
                    elif event.key == pygame.K_RIGHT and not any(self.blocks):
                        self.handle_board_response(self.board.move_right())
                    elif event.key == pygame.K_UP and not any(self.blocks):
                        self.handle_board_response(self.board.move_up())
                    elif event.key == pygame.K_DOWN and not any(self.blocks):
                        self.handle_board_response(self.board.move_down())
            self.draw_game()
            if not any(self.blocks) and self.blocks_to_remove:
                for block in self.blocks_to_remove:
                    self.blocks.remove(block)
                self.blocks_to_remove.clear()
            if not any(self.blocks) and self.coords_to_create is not None:
                self.place_block(self.coords_to_create[1], self.coords_to_create[0])
                self.coords_to_create = None
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def handle_board_response(self, response: tuple[tuple]) -> None:
        response = sorted(response, key = self.__response_key)
        print()
        print(response)
        for i in self.board.matrix:
            print(i)
        indexes_to_elevate = []
        coord_flags = [True for i in range(len(self.blocks))]
        increased_flags = [True for i in range(len(self.blocks))]
        for coords, event in response:
            for index, block in enumerate(self.blocks):
                if (block.matrix_coords == Vector2(coords[1], coords[0]) and
                    (event != "remove" or increased_flags[index]) and
                    (type(event) != tuple or coord_flags[index]) and
                    event != "new"):
                    break
            else:
                if event == "new":
                    self.coords_to_create = coords
                else:
                    print(coords, event, "not found")
                continue
            if type(event) == tuple:
                y = event[0] - coords[0]
                x = event[1] - coords[1]
                if x > 0:
                    self.blocks[index].move("right", x, (X_CORNER + BLOCK_PADDING * (event[1] + 1)
                                                + BLOCK_SIZE * event[1] + BLOCK_SIZE // 2))
                    coord_flags[index] = False
                elif x < 0:
                    self.blocks[index].move("left", x, (X_CORNER + BLOCK_PADDING * (event[1] + 1) 
                                            + BLOCK_SIZE * event[1] + BLOCK_SIZE // 2))
                    coord_flags[index] = False
                elif y > 0:
                    self.blocks[index].move("down", y, (Y_CORNER + BLOCK_PADDING * (event[0] + 1)
                                                + BLOCK_SIZE * event[0] + BLOCK_SIZE // 2))
                    coord_flags[index] = False
                elif y < 0:
                    self.blocks[index].move("up", y, (Y_CORNER + BLOCK_PADDING * (event[0] + 1)
                                                + BLOCK_SIZE * event[0] + BLOCK_SIZE // 2))
                    coord_flags[index] = False
            elif event == "increase":
                indexes_to_elevate.append(index)
                self.blocks[index].action = "increase"
                increased_flags[index] = False
            elif event == "remove":
                self.blocks_to_remove.append(self.blocks[index])
        for index in indexes_to_elevate:
            block = self.blocks.pop(index)
            self.blocks.append(block)
                
    def place_block(self, x: int, y: int) -> None:
        val = self.board.matrix[y][x]
        self.blocks.append(
            Block(
                self.screen,
                val,
                (x, y),
                (
                    X_CORNER + BLOCK_PADDING * (x + 1) + BLOCK_SIZE * x + BLOCK_SIZE // 2, 
                    Y_CORNER + BLOCK_PADDING * (y + 1) + BLOCK_SIZE * y + BLOCK_SIZE // 2
                )
            )
        )

    def draw_game(self) -> None:
        self.screen.blit(self.background, (0, 0))
        for block in self.blocks:
            block.draw()
    
    def new_game(self) -> None:
        self.blocks.clear()
        for y, x in self.board.reset_board():
            self.place_block(x, y)

    def __response_key(self, item) -> tuple[int, tuple[int, int]]:
        if item[1] == "increase":
            return (0, item[0])
        elif isinstance(item[1], tuple):
            return (1, item[0])
        elif item[1] == "remove":
            return (2, item[0])
        elif item[1] == "new":
            return (3, item[0])