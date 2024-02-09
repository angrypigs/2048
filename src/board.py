import random



class Board:

    def __init__(self) -> None:
        self.matrix = [[0 for x in range(4)] for y in range(4)]

    def __new_block(self) -> tuple[int, int]:
        new_block = random.choices((2, 4), weights=(19, 1))[0]
        chosen_place = random.choice([(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0])
        self.matrix[chosen_place[0]][chosen_place[1]] = new_block
        return chosen_place

    def reset_board(self) -> tuple[tuple[int, int]]:
        start_blocks = []
        self.matrix = [[0 for x in range(4)] for y in range(4)]
        for i in range(2):
            start_blocks.append(self.__new_block())
        return tuple(start_blocks)
