class GobbletGameState:
    def get_valid_moves(self):
        valid_moves = []
        # Iterate through the game board to find all possible valid moves
        for row in range(4):
            for col in range(4):
                if len(self.board[row][col]) == 0:
                    # If the cell is empty, it's a valid move to place a piece there
                    valid_moves.append((row, col))
                elif self.board[row][col][-1].size < 4:
                    # If the cell has a stack but the top piece size is less than 4,
                    # placing a piece with a larger size is a valid move
                    valid_moves.append((row, col))
        return valid_moves
    def make_move(self, move, player_color):
        row, col = move
        # Check if the move is within the bounds of the board
        if 0 <= row < 4 and 0 <= col < 4:
            # Perform the move if the cell is empty or the top piece size is smaller than 4
            if len(self.board[row][col]) == 0 or self.board[row][col][-1].size < 4:
                # Create a new piece with size 1
                new_piece = self.create_piece(1, player_color)
                # Place the new piece on the board at the specified position
                self.board[row][col].append(new_piece)
                return True  # Move successful
        return False 
    def undo_move(self, move):
        row, col = move
        # Check if the move was valid
        if 0 <= row < 4 and 0 <= col < 4 and len(self.board[row][col]) > 0:
            # Undo the move by removing the piece placed at the specified position
            self.board[row][col].pop()
    def evaluate_state(self):
        # Evaluate the game state
        player_score = 0

        # Evaluate based on pieces on the board
        for row in self.board:
            for cell in row:
                if len(cell) > 0:
                    # Check if the top piece is owned by the player
                    if cell[-1].color == 'player_color':
                        player_score += cell[-1].size  # Add score based on the size of the piece

        # Other evaluation factors could include controlling specific squares, board position, etc.

        return player_score
    def check_winner(self):
        # Check for a winning condition
        # Check rows
        for row in self.board:
            if row[0] and row.count(row[0]) == 4:
                return row[0][-1].color  # Return the color of the winning player
        # Check columns
        for i in range(4):
            if self.board[0][i] and [self.board[j][i] for j in range(4)].count(self.board[0][i]) == 4:
                return self.board[0][i][-1].color  # Return the color of the winning player

        # Check diagonals
        if self.board[0][0] and [self.board[i][i] for i in range(4)].count(self.board[0][0]) == 4:
            return self.board[0][0][-1].color  # Return the color of the winning player

        if self.board[0][3] and [self.board[i][3 - i] for i in range(4)].count(self.board[0][3]) == 4:
            return self.board[0][3][-1].color  # Return the color of the winning player

        # Check for a draw
        if all(cell for row in self.board for cell in row):
            return 'Draw'

        # If no winner or draw yet, return None to indicate the game is ongoing
        return None            
    def alphabeta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_state()

        valid_moves = self.get_valid_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                self.make_move(move)
                eval = self.alphabeta(depth - 1, alpha, beta, False)
                self.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                self.make_move(move)
                eval = self.alphabeta(depth - 1, alpha, beta, True)
                self.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_best_move(self, depth):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True

        valid_moves = self.get_valid_moves()
        for move in valid_moves:
            self.make_move(move)
            eval = self.alphabeta(depth - 1, alpha, beta, not maximizing_player)
            self.undo_move(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move
