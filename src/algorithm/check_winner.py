def count_pieces_in_line(state, line):
    w_count, b_count = 0, 0
    for row, col in line:
        piece = state.get_top_piece(row, col)
        if not piece:
            continue
        elif piece.player == "w":
            w_count += 1
        else:
            b_count += 1
    return w_count, b_count


def check_winner(state):
    def check_color(w, b):
        if w == 4:
            return "w"
        if b == 4:
            return "b"
        return False

    for i in range(4):
        w, b = count_pieces_in_line(state, [(i, j) for j in range(4)])  # rows
        winner = check_color(w, b)
        if winner:
            print("row win : ", winner)
            return winner
        w, b = count_pieces_in_line(state, [(j, i) for j in range(4)])  # cols
        winner = check_color(w, b)
        if winner:
            print("col win : ", winner)
            return winner
    w, b = count_pieces_in_line(state, [(i, i) for i in range(4)])  # left diag
    winner = check_color(w, b)
    if winner:
        print("left diag win : ", winner)
        return winner
    w, b = count_pieces_in_line(state, [(i, 3 - i) for i in range(4)])  # right_diag
    winner = check_color(w, b)
    if winner:
        print("right diag win : ", winner)
        return winner

    return False
