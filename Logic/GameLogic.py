class Piece:
    def __init__(self, size, color, row, column, collection):
        self.color = color # "w" or "b"
        self.size = size # four sizes 1 -> 4
        self.collection = collection # three collection 1 -> 3 ==> None for in board , int for off
        self.row = row # int for in board , None for off
        self.column = column # int for in board , None for off

class Player:
    def __init__(self,color):
        self.color = color
        self.pieces = [ [] for i in range(3)]
        self.dragged_piece = None #at beginning

    def drag_piece(self, color, collection, row, column):
        # check if the player tries to access his color
        if color == self.color:

            # check if from outside
            if collection != None and row == None and column == None:
                if len(self.pieces[collection - 1]) != 0:
                    self.dragged_piece = self.pieces[collection - 1].pop()
            
            # check if from inside            
            elif collection == None and row != None and column != None:
                if len(Game.board[row][column]) != 0:
                    self.dragged_piece = Game.board[row][column].pop()

    # place piece from outside the board
    def drop_piece(self, row, column):
        # check if you have a dragged piece or not
        if self.dragged_piece != None:
            append = False
            # check if your dragged piece is from outside
            if self.dragged_piece.collection != None and self.dragged_piece.row == None and self.dragged_piece.column == None:
                top_colors = []
                # check if the target is empty or not
                if len(Game.board[row][column]) == 0 :
                    append = True
                
                else:
                    # check the size availability
                    if Game.board[row][column][-1].size < self.dragged_piece.size:

                        # check for the color of your opponent:
                        if self.color != Game.board[row][column][-1].color:
                            
                            # check for rows
                            for row in range(4):

                                for column in range(4):
                                    top_colors.append(Game.get_top(row, column).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    append = True
                                
                                else:
                                    return False
                                
                            # check for columns
                            for column in range(4):

                                for row in range(4):
                                    top_colors.append(Game.get_top(row, column).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    append = True
                                
                                else:
                                    return False
                            
                            # check for diagonals:
                            # left
                            for i in range(4):
                                top_colors.append(Game.get_top(i,i).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    append = True
                                
                                else:
                                    return False
                            
                            # right
                            for i in range(4):
                                top_colors.append(Game.get_top(i, 3 - i).color)

                                if (top_colors.count("w") == 3 and self.color == "b") or (top_colors.count("b") == 3 and self.color == "w"):
                                    append = True
                                
                                else:
                                    return False
                        
                        else:
                            append = True
                    
                    else:
                        return False
            
            # if from inside
            elif self.dragged_piece.collection == None and self.dragged_piece.row != None and self.dragged_piece.column != None:
                if len(Game.board[row][column]) == 0:
                    append = True

                # if the cell is not empty, check if the dragged piece is bigger than the standing piece
                else:

                    if self.dragged_piece.size > Game.board[row][column][-1].size:
                        append = True
                    else:
                        return False

            if append == True:
                Game.board[row][column].append(self.dragged_piece)
                Game.board[row][column][-1] = None
                Game.board[row][column][-1].row = row
                Game.board[row][column][-1].column = column
                return True

class Game:
    def __init__(self):
        self.winner = None
        self.player_names = ['black', 'white']
        
    #3D gaming board list
    # 2D board with each cell represented by 1D list (stack)
    board = [ [ [] for i in range(4)] for i in range(4) ]
    
    white_player = Player("w")
    black_player = Player("b")

    # function to get the top piece on specific cell
    def get_top (row, column):
        return Game.board[row][column][-1]
    
    # function to create all pieces
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
    def check_win() :
        winner = ""
        top_colors = []

        # check row wins
        for row in range(4):

            for column in range(4):
                top_colors.append(Game.get_top(row, column).color)

            if top_colors.count(top_colors[0]) == 4:
                winner = top_colors[0]
                return winner
        
        # check column wins
        for column in range(4):

            for row in range(4):
                top_colors.append(Game.get_top(row, column))

            if top_colors.count(top_colors[0]) == 4:
                winner = top_colors[0]
                return winner
            
        # check diagonal wins
        # left
        for i in range(4):
            top_colors.append(Game.get_top(i,i).color)

            if top_colors.count(top_colors[0]) == 4:
                winner = top_colors[0]
                return winner
        
        # right
        for i in range(4):
            top_colors.append(Game.get_top(i, 3 - i).color)

            if top_colors.count(top_colors[0]) == 4 :
                winner = top_colors[0]
                return winner
