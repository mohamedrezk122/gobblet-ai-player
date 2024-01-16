siz=4
count=0
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

    ##############################################     
    def get_valid_moves():
        valid_moves = []
        global siz,count
        # Iterate through the game board to find all possible valid moves
        count+=1
        if(count>3):
           count=1
           siz-=1 
        for row in range(4):
            for col in range(4):
                if Game.get_top(row,col).size==None:
                    # If the cell is empty, it's a valid move to place a piece there
                    valid_moves.append((row, col))
                elif Game.get_top(row,col).size < siz:
                    # If the cell has a stack but the top piece size is less than 4,
                    # placing a piece with a larger size is a valid move
                    valid_moves.append((row, col))
        return valid_moves


    def undo_move(mov):
        row,col=mov
        # Check if the move was valid
        if 0 <= row < 4 and 0 <= col < 4 and len(Game.board[row][col]) > 0:
            # Undo the move by removing the piece placed at the specified position
            Game.board[row][col].pop()


    def evaluate_state(p):
        # Evaluate the game state
        player_score = 0

        # Evaluate based on pieces on the board
        for row in range(4):
            for col in range(4):
                    if (Game.get_top(row,col).size) and (Game.get_top(row,col).color==p):
                        player_score += Game.get_top(row,col).size  # Add score based on the size of the piece
        # Other evaluation factors could include controlling specific squares, board position, etc.
        return player_score


    def create_piece(size, color):
        return Piece(size=size, color=color,row=None,column=None,stack=None)


    def make_move(move, player_color):
        row, col = move
        stak=1
        # Check if the move is within the bounds of the board
        if 0 <= row < 4 and 0 <= col < 4:
            # Perform the move if the cell is empty or the top piece size is smaller than 4
            if len(Game.board[row][col]) == 0 or Game.board[row][col][-1].size < 4:
                new_piece = Game.create_piece(stak, player_color)
                # Place the new piece on the board at the specified position   
                Game.board[row][col].append(new_piece)
                return True  # Move successful
        return False


    def alphabeta(depth, alpha, beta, maximizing_player,p):
        if depth == 0 or Game.set_winner() is not None:
            return Game.evaluate_state(p)
        valid_moves = Game.get_valid_moves()
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                Game.make_move(move,p)
                eval = Game.alphabeta(depth - 1, alpha, beta, False,p)
                Game.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break   
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                Game.make_move(move,p)
                eval = Game.alphabeta(depth - 1, alpha, beta, True,p)
                Game.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def make_best_move(depth,p):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True
        valid_moves = Game.get_valid_moves()
        print(valid_moves)           
        for move in valid_moves: 
           Game.make_move(move,p)    
           eval = Game.alphabeta(depth - 1, alpha, beta, not maximizing_player,p)
           Game.undo_move(move)
           if eval > max_eval:
                max_eval = eval
                best_move = move        
        return best_move


############################################

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
        mod=input("choose your rival(H or A):")
        if(mod=='H'):
         Game.current=input("choose your colour:")    
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
            print(Game.get_valid_moves())
            print(Game.evaluate_state("b"))    
            if Game.current == "b":
                Game.current = "w"
            elif Game.current == "w":
                Game.current = "b"
         return Game.winner
        ##### AI PART##### 
        else:
         rc=0
         Game.current="b"   
         while Game.winner == "":
            if Game.current == "b":
                # black player drags and drops
                print("black player turn")
                print("drag a piece:")
                out = input("Outside the board? [y/n]: ")
                if out.upper() == "N":
                 start_row = int(input("Enter your row: "))
                 start_column = int(input("Enter your column: "))
                elif out.upper() == "Y":
                 start_stack = int(input("Enter your stack: "))
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
                print("drop a piece:")
                target_row = int(input("Enter your row: "))
                target_column = int(input("Enter your column: "))        
                dropped = Game.black_player.drop_piece(target_row, target_column)
                while dropped == False:
                    print("invalid drop")
                    print("try again")
                    target_row = int(input("Enter your row: "))
                    target_column = int(input("Enter your column: "))
                    dropped = Game.black_player.drop_piece(target_row, target_column)
                print(Game.get_top(target_row,target_column).size)    
            elif Game.current == "w":
                print("AI turn ")
                mov=Game.make_best_move(1,"w")
                print(mov)
                target_row,target_column=mov
                Game.white_player.drag_piece(rc,None,None)
                Game.white_player.drop_piece(target_row,target_column)
                print(Game.get_top(target_row,target_column).size)
                rc+=1
                if(rc>3):
                   rc=0 
                print(Game.get_valid_moves()) 
            if  Game.winner != "":
                return Game.winner                        
            Game.set_winner()   
            if Game.current == "b":
                Game.current = "w"
            elif Game.current == "w":
                Game.current = "b"
         return Game.winner


game = Game()
winner = game.play()
print(winner)