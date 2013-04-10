import pprint
import pdb

ROWS = 5 #5
COLUMNS = 3 #7
TO_WIN = 3

MAX = 1
MIN = 2

BLANK_BOARD = [[0 for i in range(COLUMNS)] for j in range(ROWS)]


def get_row(grid, col, rows):
    for i, row in enumerate(reversed(grid)):
    #if it's over a column, figure out the bottom
    #slot in the grid to put the piece
        if row[col] == 0:
            return rows-i-1
    return None

def get_winner(connected_squares):
    if len(set(connected_squares)) == 1:
        member = connected_squares.pop()
        return member

def is_row_win(grid):
    for row in reversed(grid):
        for start in range(COLUMNS - TO_WIN + 1):
            if row[start] != 0:
                connected_squares = [row[start+i] for i in range(TO_WIN)]
                winner = get_winner(connected_squares)
                if winner:
                    return winner

def is_col_win(grid):
    for col_num in range(COLUMNS):
        col = [row[col_num] for row in reversed(grid)]
        for start in range(ROWS - TO_WIN + 1):
            if col[start] != 0:
                connected_squares = [col[start+i] for i in range(TO_WIN)]
                winner = get_winner(connected_squares)
                if winner:
                    return winner

def generate_legal_diagonals(grid):
    diags = []
    #top left -> bottom right
    for row_num in range(ROWS - TO_WIN + 1):
        for col_num in range (COLUMNS - TO_WIN + 1):
            connected_squares = [grid[row_num+i][col_num+i] for i in range(TO_WIN)]
            if 0 not in connected_squares:
                diags.append(connected_squares)
    #bottom left -> top right
    for row_num in range(TO_WIN - 1, ROWS):
        for col_num in range (COLUMNS - TO_WIN + 1):
            connected_squares = [grid[row_num-i][col_num+i] for i in range(TO_WIN)]
            if 0 not in connected_squares:
                diags.append(connected_squares)
    return diags

def is_diag_win(grid):
    for diag in generate_legal_diagonals(grid):
        winner = get_winner(diag)
        if winner:
            return winner

def determine_winner(grid):
    return is_row_win(grid) or is_col_win(grid) or is_diag_win(grid)

def make_sample_board(b):
    r = ROWS
    #b[get_row(b,2,ROWS)][2] = MAX
    #b[get_row(b,1,ROWS)][1] = MIN
    #b[get_row(b,2,ROWS)][2] = MAX
    #b[get_row(b,2,ROWS)][2] = MIN
    #b[get_row(b,1,ROWS)][1] = MAX
    #b[get_row(b,3,ROWS)][3] = MIN
    return b

def make_move(b, player):
    boards = []
    for i in range(COLUMNS):
        new_b = [row[:] for row in b]
        row = get_row(b, i, ROWS)
        if row != None:
            new_b[get_row(b, i, ROWS)][i] = player
            boards.append([new_b[:],i] )
    return boards

def no_more_moves(board):
    #if there are no 0's in the top row, there are no more moves
    return not(0 in board[0])

def get_max_or_min(possible_moves, player):
    if player == MAX:
        return max(possible_moves)
    else: #player is MIN
        return min(possible_moves)

def recur_add_player_depth(board, player, memoized_board = {}, boards=[], col=0):
    #pp.pprint(board)
    #pdb.set_trace()
    if str(board) in memoized_board:
        #print "**************the board was memoized already, will result in", memoized_board[str(board)]
        return memoized_board[str(board)]

    winner = determine_winner(board)
    if winner:
        #print "************* %s is winner!" % (winner)
        if winner == MAX:
            return (1, col)
        if winner == MIN:
            return (-1, col)
    elif no_more_moves(board):
        return (0, col)
    else:
        boards = make_move(board, player)
        possible_moves = []
        for b, col in boards:
            if player == MAX:
                next_player = MIN
            else:
                next_player = MAX
            recur_result, _ = recur_add_player_depth(b, next_player, memoized_board, boards, col)
            memoized_board[str(b)] = (recur_result, col)
            #print memoized_board

            possible_moves.append((recur_result, col))
            if (player == MAX and recur_result == 1) or (player == MIN and recur_result == -1):
                #print "*************PRUNED"
                return (recur_result, col)
        return get_max_or_min(possible_moves, player)

no_moves_EXAMPLE = [[1, 2, 2], [1, 1, 1], [2, 1, 2]]

max_1_SOLUTION = [
     [[0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [2, 1, 1]]]


min_1_SOLUTION = [
    [[[0, 0, 0], [0, 0, 0], [2, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 1, 0], [0, 2, 0], [2, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 0, 0], [0, 2, 0], [2, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [0, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 1, 2], [2, 1, 1]]]]

row_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 1], [2, 1, 2]]
col_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [2, 1, 0]]
diag_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [1, 2, 0], [2, 1, 0], [2, 1, 1]]


if __name__ == '__main__':
    board = make_sample_board(BLANK_BOARD)
    pp = pprint.PrettyPrinter(width = 20)

    assert no_more_moves(board) == False
    assert no_more_moves(no_moves_EXAMPLE) == True

    #print recur_add_player_depth(board, MAX)

    assert is_row_win(row_win_EXAMPLE) == 1
    assert is_col_win(col_win_EXAMPLE) == 1
    assert is_diag_win(diag_win_EXAMPLE) == 1
