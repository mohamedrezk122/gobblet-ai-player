class Piece:
    def __init__(self, size=None, color=None, row=None, column=None, stack=None):
        self.color = color  # "w" or "b"
        self.size = size  # four sizes 1 -> 4
        self.stack = stack  # three stack 1 -> 3 ==> None for in board , int for off
        self.row = row  # int for in board , None for off
        self.column = column  # int for in board , None for off


class Player:
    def __init__(self, color, logic):
        self.color = color
        self.pieces = [[] for i in range(3)]
        self.dragged_piece = None  # at beginning
        self.logic = logic

    def drag_piece(self, stack, row, column):
        # check if from outside
        if stack != None and row == None and column == None:
            if len(self.pieces[stack - 1]) != 0:
                self.dragged_piece = self.pieces[stack - 1].pop()
            else:
                return False

        # check if from inside
        elif stack == None and row != None and column != None:
            if (
                len(self.logic.board[row][column]) != 0
                and self.color == self.logic.board[row][column][-1].color
            ):
                self.dragged_piece = self.logic.board[row][column].pop()
            else:
                return False

        # check if he can drop
        for cells_in_row, i in zip(self.logic.board, range(4)):
            for cell, j in zip(cells_in_row, range(4)):
                # check the difference between his position and the checked position
                if row != i or column != j:
                    if len(cell) == 0:
                        return True
                    elif self.dragged_piece.size > cell[-1].size:
                        return True
        # the other player wins
        if self.color == "b":
            self.logic.winner = "w"
        else:
            self.logic.winner = "b"

    def append_piece(self, row, column):
        self.logic.board[row][column].append(self.dragged_piece)
        self.dragged_piece = None
        self.logic.board[row][column][-1].stack = None
        self.logic.board[row][column][-1].row = row
        self.logic.board[row][column][-1].column = column
        return True

    # place piece from outside the board
    def drop_piece(self, row, column):
        # check if you have a dragged piece or not
        if self.dragged_piece != None:
            # check if the target is the same as start
            if self.dragged_piece.row != row or self.dragged_piece.column != column:
                # check if your dragged piece is from outside
                if (
                    self.dragged_piece.stack != None
                    and self.dragged_piece.row == None
                    and self.dragged_piece.column == None
                ):
                    top_colors = []
                    # check if the target is empty or not
                    if len(self.logic.board[row][column]) == 0:
                        return self.append_piece(row, column)

                    else:
                        # check the size availability
                        if (
                            self.logic.board[row][column][-1].size
                            < self.dragged_piece.size
                        ):
                            # check for the color of your opponent:
                            if self.color != self.logic.board[row][column][-1].color:
                                # check for rows
                                for i in range(4):
                                    top_colors = []

                                    for j in range(4):
                                        top_colors.append(
                                            self.logic.get_top(i, j).color
                                        )

                                    if (
                                        top_colors.count("w") == 3 and self.color == "b"
                                    ) or (
                                        top_colors.count("b") == 3 and self.color == "w"
                                    ):
                                        if row == i:
                                            return self.append_piece(row, column)

                                # check for columns
                                for j in range(4):
                                    top_colors = []

                                    for i in range(4):
                                        top_colors.append(
                                            self.logic.get_top(i, j).color
                                        )

                                    if (
                                        top_colors.count("w") == 3 and self.color == "b"
                                    ) or (
                                        top_colors.count("b") == 3 and self.color == "w"
                                    ):
                                        if column == j:
                                            return self.append_piece(row, column)

                                # check for diagonals:
                                # left
                                top_colors = []
                                for i in range(4):
                                    top_colors.append(self.logic.get_top(i, i).color)

                                if (
                                    top_colors.count("w") == 3 and self.color == "b"
                                ) or (top_colors.count("b") == 3 and self.color == "w"):
                                    if (
                                        (row == 0 and column == 0)
                                        or (row == 1 and column == 1)
                                        or (row == 2 and column == 2)
                                        or (row == 3 and column == 3)
                                    ):
                                        return self.append_piece(row, column)

                                # right
                                top_colors = []
                                for i in range(4):
                                    top_colors.append(
                                        self.logic.get_top(i, 3 - i).color
                                    )

                                if (
                                    top_colors.count("w") == 3 and self.color == "b"
                                ) or (top_colors.count("b") == 3 and self.color == "w"):
                                    if (
                                        (row == 0 and column == 3)
                                        or (row == 1 and column == 2)
                                        or (row == 2 and column == 1)
                                        or (row == 3 and column == 0)
                                    ):
                                        return self.append_piece(row, column)
                                return False
                            else:
                                return self.append_piece(row, column)
                        else:
                            return False

                # if from inside
                elif (
                    self.dragged_piece.stack == None
                    and self.dragged_piece.row != None
                    and self.dragged_piece.column != None
                ):
                    if len(self.logic.board[row][column]) == 0:
                        return self.append_piece(row, column)
                    # if the cell is not empty, check if the dragged piece is bigger than the standing piece
                    else:
                        if (
                            self.dragged_piece.size
                            > self.logic.board[row][column][-1].size
                        ):
                            return self.append_piece(row, column)
                        else:
                            return False
            else:
                return False
