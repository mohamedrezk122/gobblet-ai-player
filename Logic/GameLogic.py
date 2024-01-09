class Piece:
    def __init__(self, size = None, color = None, row = None, column = None, stack = None):
        self.color = color # "w" or "b"
        self.size = size # four sizes 1 -> 4
        self.stack = stack # three stack 1 -> 3 ==> None for in board , int for off
        self.row = row # int for in board , None for off
        self.column = column # int for in board , None for off

class Player:
    def __init__(self,color):
        self.color = color
        self.pieces = [ [] for i in range(3)]
        self.dragged_piece = None #at beginning

    def drag_piece(self, stack, row, column):
        # check if from outside
        if stack != None and row == None and column == None:
            if len(self.pieces[stack - 1]) != 0:
                self.dragged_piece = self.pieces[stack - 1].pop()
            else:
                return False
        
        # check if from inside            
        elif stack == None and row != None and column != None:
            if len(Game.board[row][column]) != 0 and self.color == Game.board[row][column][-1].color:
                self.dragged_piece = Game.board[row][column].pop()
            else:
                return False

        # check if he can drop
        for cells_in_row, i in zip(Game.board, range(4)):
            for cell, j in zip(cells_in_row,range(4)):
                # check the difference between his position and the checked position
                if row != i or column != j:
                    if len(cell) == 0:
                        return True
                    elif self.dragged_piece.size > cell[-1].size:
                        return True
        
        # the other player wins
        if self.color == "b":
            Game.winner = "w"
        else:
            Game.winner = "b"

    def append_piece(self, row, column):
        Game.board[row][column].append(self.dragged_piece)
        self.dragged_piece = None
        Game.board[row][column][-1].stack = None
        Game.board[row][column][-1].row = row
        Game.board[row][column][-1].column = column
        return True

    # place piece from outside the board
    def drop_piece(self, row, column):
        # check if you have a dragged piece or not
        if self.dragged_piece != None:
            # check if the target is the same as start
            if self.dragged_piece.row != row or self.dragged_piece.column != column:
                # check if your dragged piece is from outside
                if self.dragged_piece.stack != None and self.dragged_piece.row == None and self.dragged_piece.column == None:
                    top_colors = []
                    # check if the target is empty or not
                    if len(Game.board[row][column]) == 0 :
                        return self.append_piece(row, column)
                    
                    else:
                        # check the size availability
                        if Game.board[row][column][-1].size < self.dragged_piece.size:
                            # check for the color of your opponent:
                            if self.color != Game.board[row][column][-1].color:
                                # check for rows
                                for i in range(4):
                                    top_colors = []

                                    for j in range(4):
                                        top_colors.append(Game.get_top(i, j).color)

                                    if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                        if row == i:
                                            return self.append_piece(row, column)
                                    
                                # check for columns
                                for j in range(4):
                                    top_colors = []

                                    for i in range(4):
                                        top_colors.append(Game.get_top(i, j).color)

                                    if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                        if column == j:
                                            return self.append_piece(row, column)
                                
                                # check for diagonals:
                                # left
                                top_colors = []
                                for i in range(4):
                                    top_colors.append(Game.get_top(i,i).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    if (row == 0 and column == 0) or (row == 1 and column == 1) or (row == 2 and column == 2) or (row == 3 and column == 3):
                                        return self.append_piece(row, column)
                                
                                # right
                                top_colors = []
                                for i in range(4):
                                    top_colors.append(Game.get_top(i, 3 - i).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    if (row == 0 and column == 3) or (row == 1 and column == 2) or (row == 2 and column == 1) or (row == 3 and column == 0):
                                        return self.append_piece(row, column) 
                                
                                return False

                            else:
                                return self.append_piece(row, column)
                        
                        else:
                            return False
                
                # if from inside
                elif self.dragged_piece.stack == None and self.dragged_piece.row != None and self.dragged_piece.column != None:
                    if len(Game.board[row][column]) == 0:
                        return self.append_piece(row, column)

                    # if the cell is not empty, check if the dragged piece is bigger than the standing piece
                    else:
                        if self.dragged_piece.size > Game.board[row][column][-1].size:
                            return self.append_piece(row, column)
                        else:
                            return False
            else:
                return False

class Game:
    #3D gaming board list
    # 2D board with each cell represented by 1D list (stack)
    board = [ [ [] for i in range(4)] for i in range(4) ]
    
    white_player = Player("w")
    black_player = Player("b")
    winner = "" # at beginning , can be "w" or "b"
    current = "b" # at beginning , can be "w" or "b"

    def __init__(self):
        self.player_names = ['black', 'white']
        
    # function to get the top piece on specific cell
    @staticmethod
    def get_top (row, column) -> Piece:
        if len(Game.board[row][column]) != 0:
            return Game.board[row][column][-1]
        else:
            # return a piece with no color
            return Piece()
    
    # function to create all pieces
    @staticmethod
    def create_pieces() :

        for i in range(3):
            size = 1
            
            for j in range(4):
                piece1 = Piece(size, "w", None, None, i + 1)
                piece2 = Piece(size, "b", None, None, i + 1)
                Game.white_player.pieces[i].append(piece1)
                Game.black_player.pieces[i].append(piece2)
                size += 1
                
    # function to check if there is win
    @staticmethod
    def set_winner() :
        top_colors = []

        # check row wins
        for row in range(4):
            top_colors = []

            for column in range(4):
                top_colors.append(Game.get_top(row, column).color)
                if top_colors[column] == None:
                    break

            if top_colors.count(top_colors[0]) == 4:
                Game.winner = top_colors[0]
                return
        
        # check column wins
        for column in range(4):
            top_colors = []

            for row in range(4):
                top_colors.append(Game.get_top(row, column).color)
                if top_colors[row] == None:
                    break

            if top_colors.count(top_colors[0]) == 4:
                Game.winner = top_colors[0]
                return
            
        # check diagonal wins
        # left
        top_colors = []
        for i in range(4):
            top_colors.append(Game.get_top(i,i).color)
            if top_colors[i] == None:
                break

            if top_colors.count(top_colors[0]) == 4:
                Game.winner = top_colors[0]
                return
        
        # right
        top_colors = []
        for i in range(4):
            top_colors.append(Game.get_top(i, 3 - i).color)
            if top_colors[i] == None:
                break

            if top_colors.count(top_colors[0]) == 4 :
                Game.winner = top_colors[0]
                return
            
    @staticmethod
    def play():
        Game.create_pieces()
        while Game.winner == "":
            if Game.current == "b":
                # black player drags and drops
                print("black player turn")
            elif Game.current == "w":
                # white player drags and drops
                print("white player turn: ")

            # drag                
            print("drag a piece:")
            out = input("Outside the board? [y/n]: ")
            if out.upper() == "N":
                start_row = int(input("Enter your row: "))
                start_column = int(input("Enter your column: "))
            elif out.upper() == "Y":
                start_stack = int(input("Enter your stack: "))
            
            if Game.current == "b":
                if out.upper() == "Y":
                    dragged = Game.black_player.drag_piece( start_stack, None, None)
                elif out.upper() == "N":
                    dragged = Game.black_player.drag_piece( None, start_row, start_column)
                while dragged == False:
                    print("invalid drag")
                    print("try again")
                    out = input("Outside the board? [y/n]: ")
                    if out.upper() == "N":
                        start_row = int(input("Enter your row: "))
                        start_column = int(input("Enter your column: "))
                        dragged = Game.black_player.drag_piece( None, start_row, start_column)
                    elif out.upper() == "Y":
                        start_stack = int(input("Enter your stack: "))
                        dragged = Game.black_player.drag_piece( start_stack, None, None)

            elif Game.current == "w":
                if out.upper() == "Y":
                    dragged = Game.white_player.drag_piece( start_stack, None, None)
                elif out.upper() == "N":
                    dragged = Game.white_player.drag_piece( None, start_row, start_column)
                while dragged == False:
                    print("invalid drag")
                    print("try again")
                    print("drag a piece:")
                    if out.upper() == "N":
                        start_row = int(input("Enter your row: "))
                        start_column = int(input("Enter your column: "))
                        dragged = Game.black_player.drag_piece( None, start_row, start_column)
                    elif out.upper() == "Y":
                        start_stack = int(input("Enter your stack: "))
                        dragged = Game.black_player.drag_piece( start_stack, None, None)

            # check if a player dragged but will not be able to drop
            if  Game.winner != "":
                return Game.winner

            # drop
            print("drop a piece:")
            target_row = int(input("Enter your row: "))
            target_column = int(input("Enter your column: "))

            if Game.current == "b":
                dropped = Game.black_player.drop_piece(target_row, target_column)
                while dropped == False:
                    print("invalid drop")
                    print("try again")
                    target_row = int(input("Enter your row: "))
                    target_column = int(input("Enter your column: "))
                    dropped = Game.black_player.drop_piece(target_row, target_column)

            elif Game.current == "w":
                dropped = Game.white_player.drop_piece(target_row, target_column)
                while dropped == False:
                    print("invalid drop")
                    print("try again")
                    target_row = int(input("Enter your row: "))
                    target_column = int(input("Enter your column: "))
                    dropped = Game.white_player.drop_piece(target_row, target_column)
                
            # check for winner
            Game.set_winner()

            if Game.current == "b":
                Game.current = "w"
            elif Game.current == "w":
                Game.current = "b"

        return Game.winner

game = Game()
winner = game.play()
print(winner)
