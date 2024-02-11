import random



class Board:

    def __init__(self) -> None:
        self.matrix = [[0 for x in range(4)] for y in range(4)]

    def __new_block(self) -> tuple[int, int]:
        new_block = random.choices((2, 4), weights=(14, 1))[0]
        chosen_place = random.choice([(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0])
        self.matrix[chosen_place[0]][chosen_place[1]] = new_block
        return chosen_place

    def reset_board(self) -> tuple[tuple[int, int]]:
        start_blocks = []
        self.matrix = [[0 for x in range(4)] for y in range(4)]
        for i in range(2):
            start_blocks.append(self.__new_block())
        return tuple(start_blocks)

    def move_left(self):
        movements = []
        flag_any_move = False
        for row in range(4):
            flag_matched = False
            for col in range(1, 4):
                if self.matrix[row][col] != 0:
                    pos = col
                    while pos > 0 and self.matrix[row][pos - 1] == 0:
                        self.matrix[row][pos - 1] = self.matrix[row][pos]
                        self.matrix[row][pos] = 0
                        pos -= 1
                    if pos > 0 and self.matrix[row][pos] == self.matrix[row][pos - 1] and not flag_matched:
                        self.matrix[row][pos] = 0
                        self.matrix[row][pos - 1] *= 2
                        movements.append(((row, col), (row, pos - 1)))
                        movements.append(((row, col), "increase"))
                        movements.append(((row, pos - 1), "remove"))
                        flag_any_move = True
                        flag_matched = True
                    elif pos != col:
                        movements.append(((row, col), (row, pos)))
                        flag_any_move = True
                        flag_matched = False
        if flag_any_move:
            a, b = self.__new_block()
            movements.append(((a, b), "new"))
        return tuple(movements)

    def move_right(self):
        movements = []
        flag_any_move = False
        for row in range(4):
            flag_matched = False
            for col in range(2, -1, -1):
                if self.matrix[row][col] != 0:
                    pos = col
                    while pos < 3 and self.matrix[row][pos + 1] == 0:
                        self.matrix[row][pos + 1] = self.matrix[row][pos]
                        self.matrix[row][pos] = 0
                        pos += 1
                    if pos < 3 and self.matrix[row][pos] == self.matrix[row][pos + 1] and not flag_matched:
                        self.matrix[row][pos] = 0
                        self.matrix[row][pos + 1] *= 2
                        movements.append(((row, col), (row, pos + 1)))
                        movements.append(((row, col), "increase"))
                        movements.append(((row, pos + 1), "remove"))
                        flag_any_move = True
                        flag_matched = True
                    elif pos != col:
                        movements.append(((row, col), (row, pos)))
                        flag_any_move = True
                        flag_matched = False
        if flag_any_move:
            a, b = self.__new_block()
            movements.append(((a, b), "new"))
        return tuple(movements)

    def move_up(self):
        movements = []
        flag_any_move = False
        for col in range(4):
            flag_matched = False
            for row in range(1, 4):
                if self.matrix[row][col] != 0:
                    pos = row
                    while pos > 0 and self.matrix[pos - 1][col] == 0:
                        self.matrix[pos - 1][col] = self.matrix[pos][col]
                        self.matrix[pos][col] = 0
                        pos -= 1
                    if pos > 0 and self.matrix[pos][col] == self.matrix[pos - 1][col] and not flag_matched:
                        self.matrix[pos][col] = 0
                        self.matrix[pos - 1][col] *= 2
                        movements.append(((row, col), (pos - 1, col)))
                        movements.append(((row, col), "increase"))
                        movements.append(((pos - 1, col), "remove"))
                        flag_any_move = True
                        flag_matched = True
                    elif pos != row:
                        movements.append(((row, col), (pos, col)))
                        flag_any_move = True
                        flag_matched = False
        if flag_any_move:
            a, b = self.__new_block()
            movements.append(((a, b), "new"))
        return tuple(movements)

    def move_down(self):
        movements = []
        flag_any_move = False
        for col in range(4):
            flag_matched = False
            for row in range(2, -1, -1):
                if self.matrix[row][col] != 0:
                    pos = row
                    while pos < 3 and self.matrix[pos + 1][col] == 0:
                        self.matrix[pos + 1][col] = self.matrix[pos][col]
                        self.matrix[pos][col] = 0
                        pos += 1
                    if pos < 3 and self.matrix[pos][col] == self.matrix[pos + 1][col] and not flag_matched:
                        self.matrix[pos][col] = 0
                        self.matrix[pos + 1][col] *= 2
                        movements.append(((row, col), (pos + 1, col)))
                        movements.append(((row, col), "increase"))
                        movements.append(((pos + 1, col), "remove"))
                        flag_any_move = True
                        flag_matched = True
                    elif pos != row:
                        movements.append(((row, col), (pos, col)))
                        flag_any_move = True
                        flag_matched = False
        if flag_any_move:
            a, b = self.__new_block()
            movements.append(((a, b), "new"))
        return tuple(movements)
