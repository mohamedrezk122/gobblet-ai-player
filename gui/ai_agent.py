count = 0
flag = False

import random

from dataclasses import dataclass
from .player import Player
from .player import Piece


@dataclass
class AI_Move:
    from_outside : str
    stack : int
    piece_size : int
    piece_color : str
    row_from : int
    col_from : int
    row_to : int
    col_to : int 


class Logic:
    def __init__(self):
        # 3D gaming board list
        # 2D board with each cell represented by 1D list (stack)
        self.board = [[[] for i in range(4)] for i in range(4)]

        self.white_player = Player("w", self)
        self.black_player = Player("b", self)
        self.winner = ""  # at beginning , can be "w" or "b"
        self.current = "w"  # at beginning , can be "w" or "b"
        self.invalid_drag = []
        self.player_names = ["black", "white"]
        self.rc = 0
        self.xc = 0
        self.counter = 1
        self.create_pieces()

    def empty_cell(self):
        for row in range(4):
            for col in range(4):
                if self.get_top(row, col).size == None:
                    return True
        return False

    #############################################
    def get_valid_moves(self):
        valid_moves = []
        global siz, count
        # Iterate through the game board to find all possible valid moves
        count += 1
        if count > 3:
            count = 1
            siz -= 1
        for row in range(4):
            for col in range(4):
                if self.get_top(row, col).size == None:
                    # If the cell is empty, it's a valid move to place a piece there
                    valid_moves.append((row, col))
        return valid_moves

    def undo_move(self, mov):
        row, col = mov
        # Check if the move was valid
        if 0 <= row < 4 and 0 <= col < 4 and len(self.board[row][col]) > 0:
            # Undo the move by removing the piece placed at the specified position
            self.board[row][col].pop()

    def evaluate_state(self, p):
        # Evaluate the game state
        player_score = 0
        # Evaluate based on pieces on the board
        for row in range(4):
            for col in range(4):
                if (self.get_top(row, col).size) and (
                    self.get_top(row, col).color == p
                ):
                    player_score += self.get_top(
                        row, col
                    ).size  # Add score based on the size of the piece
        # Other evaluation factors could include controlling specific squares, board position, etc.
        return player_score

    def create_piece(self, size, color):
        return Piece(size=size, color=color, row=None, column=None, stack=None)

    def make_move(self, move, player_color):
        row, col = move
        stak = 1
        # Check if the move is within the bounds of the board
        if 0 <= row < 4 and 0 <= col < 4:
            # Perform the move if the cell is empty or the top piece size is smaller than 4
            if len(self.board[row][col]) == 0 or self.board[row][col][-1].size < 4:
                new_piece = self.create_piece(stak, player_color)
                # Place the new piece on the board at the specified position
                self.board[row][col].append(new_piece)
                return True  # Move successful
        return False

    def alphabeta(self, depth, alpha, beta, maximizing_player, p):
        if depth == 0 or self.set_winner() is not None:
            return self.evaluate_state(p)
        valid_moves = self.get_valid_moves()
        if maximizing_player:
            max_eval = float("-inf")
            for move in valid_moves:
                self.make_move(move, p)
                eval = self.alphabeta(depth - 1, alpha, beta, False, p)
                self.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                self.make_move(move, p)
                eval = self.alphabeta(depth - 1, alpha, beta, True, p)
                self.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_best_move(
        self, depth, p
    ):  ####return mov from ,best move to and flag determine either from stack or inside board
        global flag
        best_move = None
        max_eval = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        flag = False
        mov = None
        maximizing_player = True
        stak = 2
        x = 0
        y = 1
        z = 0
        valid_moves = self.get_valid_moves()
        # print(valid_moves)
        if len(valid_moves) == 0:
            y = 0
        if y == 1:
            for move in valid_moves:
                self.make_move(move, p)
                eval = self.alphabeta(depth - 1, alpha, beta, not maximizing_player, p)
                self.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            ro, co = best_move
            while self.white_player.drag_piece(stak, None, None) == False:
                if stak == -1:
                    z = 1
                    break
                stak -= 1
            if z == 0:
                mov = None
            if stak == -1:
                flag = True
                for i in range(4):
                    for j in range(4):
                        if self.get_top(i, j).color == "w" and (
                            self.get_top(i, j).size > self.get_top(ro, co).size
                        ):
                            mov = [i, j]
                            self.white_player.drag_piece(None, i, j)
                            self.white_player.drop_piece(ro, co)
                            x = 1
                        if x == 1:
                            break
            else:
                flag = False
                self.white_player.drop_piece(ro, co)
        else:
            flag = True
            for i in range(4):
                for j in range(4):
                    if self.get_top(i, j).color == "w" and (
                        self.get_top(i, j).size == 1 or self.get_top(i, j).size == 2
                    ):
                        ro = i
                        co = j
                        best_move = [ro, co]
                        break
            for i in range(4):
                for j in range(4):
                    if self.get_top(i, j).color == "w" and (
                        self.get_top(i, j).size > self.get_top(ro, co).size
                    ):
                        mov = [i, j]
                        self.white_player.drag_piece(None, i, j)
                        self.white_player.drop_piece(ro, co)

        print("ai size is: " + str(self.get_top(ro, co).size))

        return mov, best_move, flag, self.get_top(ro, co).size, stak

    def get_pieces(self, check, color):
        ai_large_pieces = []
        ai_pieces = []
        for row in range(4):
            for col in range(4):
                if (
                    self.get_top(row, col).color == color
                    and self.get_top(row, col).size == 4
                ):
                    ai_large_pieces.append((row, col))
                if self.get_top(row, col).color == color:
                    ai_pieces.append((row, col))
        # ai_pieces[0][1]
        if check == 1:
            return ai_large_pieces
        elif check == 2:
            return ai_pieces

    ########Heusristic count###########
    def moveAi(self, select_player):
        count_danger = 0  # Number of player Pieces that make AI about to lose
        count_win = 0  # Number of Ai Pieces that make AI about to win
        move = None  # The move that may Prevent AI from lose
        final_move = None  # Final decesion to move the piece to win
        win_move = None  # The move that may make AI win
        invalid = (
            False  # The position that is forbidden to drag from to Prevent AI from lose
        )
        drag_move = None  # The position that is good to drag from
        player1 = ""
        player2 = ""
        temp = 0
        h = 3
        if select_player == "w":
            player1 = "b"
            player2 = "w"
        elif select_player == "b":
            player1 = "w"
            player2 = "b"
        # Check if 3 Pieces in a row
        for row in range(4):
            for col in range(4):
                if self.get_top(row, col).color == player1:
                    count_danger += 1
                elif (
                    self.get_top(row, col).color == player1
                    and self.get_top(row, col).size < 4
                ):
                    win_move = row, col
                elif self.get_top(row, col).size == None:
                    move = row, col
                    win_move = row, col
                elif self.get_top(row, col).color == player2:
                    invalid = True
                    count_win += 1
            if count_danger == 3 and move != None:
                final_move = move
            if count_win == 3 and win_move != None:
                final_move = win_move
            if count_danger == 3 and invalid == True:
                self.invalid_drag.append((row, col))
            temp = 4 - count_win + count_danger
            if temp < h:
                h = temp
            count_danger = 0
            count_win = 0

        count_danger = 0
        count_win = 0
        move = None
        win_move = None
        invalid = False
        # Chack if 3 Pieces in a column
        for col in range(4):
            for row in range(4):
                if self.get_top(row, col).color == player1:
                    count_danger += 1
                elif (
                    self.get_top(row, col).color == player1
                    and self.get_top(row, col).size < 4
                ):
                    win_move = row, col
                elif self.get_top(row, col).size == None:
                    move = row, col
                    win_move = row, col
                elif self.get_top(row, col).color == player2:
                    invalid = True
                    count_win += 1
            if count_danger == 3 and move != None:
                final_move = move
            if count_win == 3 and win_move != None:
                final_move = win_move
            if count_danger == 3 and invalid == True:
                self.invalid_drag.append((row, col))
            temp = 4 - count_win + count_danger
            if temp < h:
                h = temp
            count_danger = 0
            count_win = 0

        count_danger = 0
        count_win = 0
        move = None
        win_move = None
        invalid = False
        # Check if 3 pieces in left diagonally
        for i in range(4):
            if self.get_top(i, i).color == player1:
                count_danger += 1
            elif (
                self.get_top(row, col).color == player1
                and self.get_top(row, col).size < 4
            ):
                win_move = row, col
            elif self.get_top(i, i).size == None:
                move = i, i
                win_move = row, col
            elif self.get_top(row, col).color == player2:
                invalid = True
                count_win += 1
        if count_danger == 3 and move != None:
            final_move = move
        if count_win == 3 and win_move != None:
            final_move = win_move
        if count_danger == 3 and invalid == True:
            self.invalid_drag.append((row, col))
        temp = 4 - count_win + count_danger
        if temp < h:
            h = temp

        count_danger = 0
        count_win = 0
        move = None
        win_move = None
        invalid = False
        # Check if 3 pieces in left diagonally
        j = 3
        for i in range(4):
            if self.get_top(i, j).color == player1:
                count_danger += 1
            elif (
                self.get_top(row, col).color == player1
                and self.get_top(row, col).size < 4
            ):
                win_move = row, col
            elif self.get_top(i, j).size == None:
                move = i, j
                win_move = row, col
            elif self.get_top(row, col).color == player2:
                invalid = True
                count_win += 1
            j -= 1
        if count_danger == 3 and move != None:
            final_move = move
        if count_win == 3 and win_move != None:
            final_move = win_move
        if count_danger == 3 and invalid == True:
            self.invalid_drag.append((row, col))
        temp = 3 - count_win + count_danger
        if temp < h:
            h = temp
        # Find the most suitable piece to Drag to avoid lose
        print("far from goal by " + str(h) + "steps")
        if self.get_pieces(1, select_player):
            valid_drag = [
                item
                for item in self.get_pieces(1, select_player)
                if item not in self.invalid_drag
            ]
            if valid_drag != []:
                drag_move = valid_drag[0]

        if final_move and not drag_move:
            return [None, final_move]

        if final_move and drag_move:
            return [drag_move, final_move]

        if final_move == None:
            return None

    def hvsaihard(self):

        print("AI turn ")
        # flg, bestmov, mov,_,_ = self.make_best_move(2, "w")
        ai_move = self.moveAi("w")
        # print("ai move == " + str(ai_move))
        # target_row, target_column = bestmov
        random_row_col = random.choice(self.get_valid_moves())
        # print("random_row_col = " + str(random_row_col))
        self.xc += 1
        if self.xc > 4 :
            self.rc += 1
            self.xc = 0 
        if self.moveAi("w") == None and self.empty_cell == False:
            drags = self.get_pieces(1, "w")
            drag_row = drags[0][0]
            drag_col = drags[0][1]
            drops = self.get_valid_moves()
            drop_row = drops[0][0]
            drop_col = drops[0][1]

            print(" AI drag from inside ", drag_row, drag_col)
            self.white_player.drag_piece(None, drag_row, drag_col)
            self.white_player.drop_piece(ai_move[1][0], ai_move[1][1])
            print("Piece color = ", self.white_player.color)
            print("AI played in " , drop_row, drop_col)
            size = self.get_top(drop_row, drop_col).size
            print("Piece Size = " , size)
            return AI_Move("N",0,size,"w",drag_row, drag_col, drop_row, drop_col)

        if self.moveAi("w") == None:
            self.white_player.drag_piece(self.rc, None, None)
            print(" AI drag from outside ")
            print("Piece color = " , self.white_player.color)
            print("stack  =  " , self.rc)
            self.white_player.drop_piece(random_row_col[0], random_row_col[1])
            print("AI played in " , random_row_col[0], random_row_col[1])
            size = self.get_top(random_row_col[0], random_row_col[1]).size
            print("Piece Size = ", size) 
            return AI_Move("Y",self.rc, size,"w",0,0, random_row_col[0], random_row_col[1])

        elif self.moveAi("w") != None and ai_move[0] == None:
            self.white_player.drag_piece(self.rc, None, None)
            print(" AI drag from outside ")
            print("Piece color = " , self.white_player.color)
            print("stack  =  " , self.rc)
            self.white_player.drop_piece(ai_move[1][0], ai_move[1][1])
            print("AI played in " , ai_move[1][0], ai_move[1][1])
            size = self.get_top(ai_move[1][0], ai_move[1][1]).size
            print("Piece Size = " , size)
            print("*************************** here**********************")
            self.rc = self.rc + 1 if self.rc < 3  else 0 
            return AI_Move("Y",self.rc, size,"w",0,0, ai_move[1][0], ai_move[1][1])

        elif self.moveAi("w") != None and ai_move[0] != None:
            print(" AI drag from inside " + str((ai_move[0][0], ai_move[0][1])))
            self.white_player.drag_piece(None, ai_move[0][0], ai_move[0][1])
            self.white_player.drop_piece(ai_move[1][0], ai_move[1][1])
            print("Piece color = " + str(self.white_player.color))
            print("AI played in " + str((ai_move[1][0], ai_move[1][1])))
            size = self.get_top(ai_move[1][0], ai_move[1][1]).size
            print("Piece Size = " , size)
            print("*************************** here**********************")
            return AI_Move("N",0,size,"w",ai_move[0][0], ai_move[0][1], ai_move[1][0], ai_move[1][1])

    ############################################

    # function to get the top piece on specific cell
    def get_top(self, row, column) -> Piece:
        if len(self.board[row][column]) != 0:
            return self.board[row][column][-1]
        else:
            # return a piece with no color
            return Piece()

    # function to create all pieces
    def create_pieces(self):
        for i in range(3):
            size = 1

            for j in range(4):
                piece1 = Piece(size, "w", None, None, i + 1)
                piece2 = Piece(size, "b", None, None, i + 1)
                self.white_player.pieces[i].append(piece1)
                self.black_player.pieces[i].append(piece2)
                size += 1

    # function to check if there is win
    def set_winner(self):
        top_colors = []

        # check row wins
        for row in range(4):
            top_colors = []

            for column in range(4):
                top_colors.append(self.get_top(row, column).color)
                if top_colors[column] == None:
                    break

            if top_colors.count(top_colors[0]) == 4:
                self.winner = top_colors[0]
                return

        # check column wins
        for column in range(4):
            top_colors = []

            for row in range(4):
                top_colors.append(self.get_top(row, column).color)
                if top_colors[row] == None:
                    break

            if top_colors.count(top_colors[0]) == 4:
                self.winner = top_colors[0]
                return

        # check diagonal wins
        # left
        top_colors = []
        for i in range(4):
            top_colors.append(self.get_top(i, i).color)
            if top_colors[i] == None:
                break

            if top_colors.count(top_colors[0]) == 4:
                self.winner = top_colors[0]
                return

        # right
        top_colors = []
        for i in range(4):
            top_colors.append(self.get_top(i, 3 - i).color)
            if top_colors[i] == None:
                break

            if top_colors.count(top_colors[0]) == 4:
                self.winner = top_colors[0]
                return

    def switch_turns(self):
        if self.current == "b":
            self.current = "w"
        elif self.current == "w":
            self.current = "b"

    def play_by_human(self, player,move_from, move_to):
        if player == "b":
            print("black player turn")
        elif player == "w":
            print("white player turn: ")

        out, start_stack, start_row, start_column = move_from

        if player == "b":
            if out.upper() == "Y":
                dragged = self.black_player.drag_piece(start_stack, None, None)
            elif out.upper() == "N":
                dragged = self.black_player.drag_piece(None, start_row, start_column)

        elif player == "w":
            if out.upper() == "Y":
                dragged = self.white_player.drag_piece(start_stack, None, None)
            elif out.upper() == "N":
                dragged = self.white_player.drag_piece(None, start_row, start_column)

        # drop
        target_row, target_column = move_to
        if player == "b":
            dropped = self.black_player.drop_piece(target_row, target_column)
        elif player == "w":
            dropped = self.white_player.drop_piece(target_row, target_column)



    def play_by_ai(self, difficulty, move_from=None, move_to=None):

        if self.current == "b":
            self.play_by_human("b", move_from, move_to)
        elif self.current == "w":
            if difficulty == "hard":
                return self.hvsaihard()
            elif difficulty == "easy":
                ai_return_move = AI_Move("N", 0,4,"w",0,0,0,0) # just a container
                print("AI turn ")
                mov, bestmov, flg, size , stack = self.make_best_move(5, "w")
                # ai_move = self.moveAi("w")
                target_row, target_column = bestmov
                ai_return_move.row_to = bestmov[0]
                ai_return_move.col_to = bestmov[1]
                ai_return_move.piece_size = size 
                if flg == False:
                    ai_return_move.from_outside = "Y"
                    ai_return_move.stack = stack
                    print("ai outside board from stack ")
                    print("ai move to: " + str(bestmov))
                else:
                    ai_return_move.ai_row_from = mov[0]
                    ai_return_move.ai_col_from = mov[1] 
                    print("ai inside board")
                    print("ai move from: " + str(mov))
                    print("ai move to: " + str(bestmov))

            return ai_return_move


    def play_by_ai_and_ai(self):

        random_row_col = random.choice(self.get_valid_moves())

        self.counter += 1
        if self.counter % 2 == 0:
            self.current = "b"
            current_player = self.black_player
        else:
            self.current = "w"
            current_player = self.white_player

        movess = self.get_valid_moves()
        if len(movess) == 0:
            if self.counter >= 32:
                drags = self.get_pieces(1, self.current)
                if drags == []:
                    print("Drag is empty")
                    # break
                drag_row = drags[0][0]
                drag_col = drags[0][1]
                drops = self.get_valid_moves()
                drop_row = drops[0][0]
                drop_col = drops[0][1]

                print("AI drag from inside " + str((drag_row, drag_col)))
                current_player.drag_piece(None, drag_row, drag_col)
                current_player.drop_piece(ai_move[1][0], ai_move[1][1])
                print("Piece color = " + str(current_player.color))
                print("AI played in " + str((drop_row, drop_col)))
                size = self.get_top(drop_row, drop_col).size
                print("Piece Size = " , size)
                print("current = " + str(self.current))
                return AI_Move("N",0,)

        else:
            if self.self.counter < 32:
                print("AI turn ")
                ai_move = self.moveAi(self.current)
                print("ai move == " + str(ai_move))

                random_row_col = random.choice(self.get_valid_moves())
                print("random_row_col = " + str(random_row_col))
                self.xc += 1
                if self.moveAi(self.current) == None:
                    current_player.drag_piece(self.rc, None, None)
                    print("AI drag from outside ")
                    print("Piece color = " + str(current_player.color))
                    print("stack  =  " + str(self.rc))
                    current_player.drop_piece(
                        random_row_col[0], random_row_col[1]
                    )
                    print(
                        "AI played in "
                        + str((random_row_col[0], random_row_col[1]))
                    )
                    print(
                        "Piece Size = "
                        + str(
                            self.get_top(
                                random_row_col[0], random_row_col[1]
                            ).size
                        )
                    )

                elif self.moveAi(self.current) != None and ai_move[0] == None:
                    current_player.drag_piece(self.rc, None, None)
                    print("AI drag from outside ")
                    print("Piece color = " + str(current_player.color))
                    print("stack  =  " + str(self.rc))
                    current_player.drop_piece(ai_move[1][0], ai_move[1][1])
                    print("AI played in " + str((ai_move[1][0], ai_move[1][1])))
                    print(
                        "Piece Size = "
                        + str(self.get_top(ai_move[1][0], ai_move[1][1]).size)
                    )

                elif self.moveAi(self.current) != None and ai_move[0] != None:
                    print(
                        "AI drag from inside "
                        + str((ai_move[0][0], ai_move[0][1]))
                    )
                    current_player.drag_piece(
                        None, ai_move[0][0], ai_move[0][1]
                    )
                    current_player.drop_piece(ai_move[1][0], ai_move[1][1])
                    print("Piece color = " + str(current_player.color))
                    print("AI played in " + str((ai_move[1][0], ai_move[1][1])))
                    print(
                        "Piece Size = "
                        + str(self.get_top(ai_move[1][0], ai_move[1][1]).size)
                    )

                self.rc += 1
                if self.rc > 2:
                    self.rc = 0
                print(self.get_valid_moves())
            # if self.winner != "":
            #     return self.winner
            # self.set_winner()
            # self.switch_turns()

            # return self.winner


if __name__ == "__main__":
    print(winner)
    game = Game()
    winner = self.play()
