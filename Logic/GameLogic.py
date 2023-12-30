class Piece:
    def __init__(self, size, color):
        self.color = color
        self.size = size


class Game:
    def __init__(self):
        self.winner = None
        self.player_names = ['black', 'white']
        

    # 3D gaming board list
    # 2D board with each cell represented by 1D list (stack)
    board = [ [ [] for i in range(4)] for i in range(4) ]
    
    # pieces lists 
    white_pieces = [ [] for i in range(4)]
    black_pieces = [ [] for i in range(4)]
    
    

    # function to get the top piece on specific cell
    def get_top (row, column):
        return Game.board[row][column][ - 1]
    
    
    # function to create all pieces
    def create_pieces() :
        for i in range(4):
            size = 1
            for j in range(3):
                piece1 = Piece(size, "w")
                piece2 = Piece(size, "b")
                
                Game.white_pieces[i].append(piece1)
                Game.black_pieces[i].append(piece2)
 
            size += 1
        return 
            
            
                
            
            
    # function to check if there is win
    def check_win() :
        winner = ""
        
        # check row wins
        for row in range(4):
            row_top_colors = []
            
            for column in range(4):
                row_top_colors.append(Game.get_top(row, column).color)
                
            if row_top_colors[0] == row_top_colors[1] == row_top_colors[2] == row_top_colors[3] :
                winner = row_top_colors[0]
                return winner
            
        # check column wins
        for column in range(4):
            column_top_colors = []
            
            for row in range(4):
                column_top_colors.append(Game.get_top(row, column))
                
            if column_top_colors[0] == column_top_colors[1] == column_top_colors[2] == column_top_colors[3] :
                winner = column_top_colors[0]
                return winner
            
        # check diagonal wins
        left_diagonal_top_colors = []
        right_diagonal_top_colors = []
        
        for i in range(4):
            left_diagonal_top_colors.append(Game.get_top(i,i).color)
            right_diagonal_top_colors.append(Game.get_top(i, 3 - i).color)
            
        if left_diagonal_top_colors[0] == left_diagonal_top_colors[1] == left_diagonal_top_colors[2] == left_diagonal_top_colors[3] :
            winner = left_diagonal_top_colors[0]
            return winner
        
        elif right_diagonal_top_colors[0] == right_diagonal_top_colors[1] == right_diagonal_top_colors[2] == right_diagonal_top_colors[3] :
            winner = right_diagonal_top_colors[0]
        
            return winner
        
        
    # move piece from one cell to another
    def move_piece(start_row, start_column, final_row, final_column):
        
        # if the cell is empty put it immediately        
        if len(Game.board[final_row][final_column]) == 0 :
            Game.board[final_row][final_column].append(Game.board[start_row][start_column].pop())
            return True
            
        # if the cell is not empty, check if the moved piece is bigger than the standing piece
        else :
            if Game.board[start_row][start_column][-1].size > Game.board[final_row][final_column][-1].size :
                Game.board[final_row][final_column].append(Game.board[start_row][start_column].pop())
                return True
            
            else :
                return False

    
    # place piece from outside the board
    # !!! لسه تحت الانشاء و التعديل
    def place_piece(color, size, row, column):
        if color == "w":
            pieces = Game.white_pieces
            
        elif color == "b":
            pieces = Game.black_pieces
            
        # check if there are left pieces with this size outside the board
        if len(pieces[size - 1]) != 0 :
            p = pieces[size - 1].pop()
            
        else :
            return "no pieces left with this size"
        
        # if the cell is empty put it immediately
        if len(Game.board[row][column]) == 0 :
            Game.board[row][column].append(p)
            return True
        
        # if cell is not empty
        # check if there are 3 opponent pieces 
        else :
            pass
            
        
            

