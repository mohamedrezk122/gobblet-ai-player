class GobbletGameState:
    def __init__(self):
        # Initialize the game state
        self.player_pieces = {
            "white": [[], [], [],[]],  # Four stacks for each player color
            "black": [[], [], [],[]]
        }
    def create_piece(self, size):
            # Create a new piece with the specified attributes
        return Piece(size)
    def evaluate_state(self):
        # Implement an evaluation function to score the game state
        # This function should return a score indicating the desirability of the state
        # Higher scores represent more favorable states for the current player
        score = 0  # Initialize the score
        
        # Example: Evaluate the board based on pieces' sizes and positions
        for row in range(4):
            for col in range(4):
                stack = self.board[row][col]
                if stack:  # Check if the stack is not empty
                    top_piece = stack[-1]
                    if top_piece.size == 4:
                        score += 10  # Higher score for having the largest piece in a cell
                    elif top_piece.size == 3:
                        score += 7
                    # Add more conditions and adjust scoring based on your game's strategy
                    # You might consider controlling the center, forming lines, etc.
        
        return score
    def get_valid_moves(self):
        # Return all valid moves for the current state
        
        valid_moves = []
        color="white"
        for row in range(4):
            for col in range(4):
                # Check if the cell is empty
                if not self.board[row][col]:
                    # If the cell is empty, consider placing a piece from the player's stack
                    for stack in range(3):
                        # Check if the player has a piece in the stack
                        if self.player_has_piece(color,stack):
                            # Add the move to place the piece from the stack to the empty cell
                            valid_moves.append((stack, row, col))

                else:
                    # If the cell is not empty, consider moving the top piece to an empty cell
                    top_piece = self.board[row][col][-1]
                    for dest_row in range(4):
                        for dest_col in range(4):
                            # Check if the destination cell is empty and valid
                            if not self.board[dest_row][dest_col]:
                                # Add the move to move the piece to the empty cell
                                valid_moves.append((row, col, dest_row, dest_col))

        return valid_moves
    def player_has_piece(self, player_color, stack):
        # Check if the player has a piece in the specified stack
        for piece in self.player_pieces[player_color][stack - 1]:
            if piece.size > 0:  # Assuming piece.size > 0 indicates a valid piece
                return True  # Player has a piece in the stack
        return False  # Player doesn't have a piece in the stack
    def make_move(self, move):
        # Make a move and update the game state
        
      if self.is_valid_move(move):
        row, column, size = move  # Assuming move is a tuple representing (row, column, size)
        
        if len(self.board[row][column]) < 3:  # Check if the cell isn't already full
            new_piece = Piece(size)  # Create a new piece with the specified size
            self.board[row][column].append(new_piece)  # Place the piece on the board
            
            # Update any necessary game state after making the move
            # For example, switch player turns or perform other updates
            
            return True  # Return True to indicate a successful move
      return False  
            # Implement the logic to place the piece at the specified row and column
            # Update self.board[row][column] accordingly based on the game rules
            
            # After making the move, update other necessary attributes or states
            
            # Example: Switch player turn or perform other necessary updates
            
    def is_valid_move(self, move):
        row, column, size = move  # Assuming move is a tuple representing (row, column, size)
    
    # Check if the coordinates (row, column) are within the board boundaries
        if 0 <= row < 4 and 0 <= column < 4:
        # Check if the selected cell is empty or can accept another piece (up to 3 pieces per cell)
         if len(self.board[row][column]) < 3:
            return True  # Return True if the move is valid
        return False 
def hill_climbing(game_state, dept):
    current_state = game_state
    if(dept=="easy"):
     depth=2
    else:
     depth=128
    while depth > 0:
        valid_moves = current_state.get_valid_moves()
        best_move = None
        best_score = float('-inf')  # Initialize with negative infinity
        
        for move in valid_moves:
            # Make a copy of the current state to simulate making the move
            new_state = current_state.clone()
            new_state.make_move(move)
            
            # Evaluate the new state after making the move
            score = new_state.evaluate_state()
            
            # Check if the score of this move is better than the best score found so far
            if score > best_score:
                best_score = score
                best_move = move
        
        # Check if no better move was found
        if best_move is None:
            break
        
        # Make the best move found
        current_state.make_move(best_move)
        depth -= 1
    
    return current_state

# Example usage
game = GobbletGameState()
difficulty_level = input("enter difficulity(easy,hard):") 
result_state = hill_climbing(game, difficulty_level)
