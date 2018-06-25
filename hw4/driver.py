import sys
from heapq import heappush, heappop


"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""
'''
1. board : make it global or not?
2. backtracking returns boolean
3. forward_checking
'''


sys.setrecursionlimit(10000)
ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'

remain_value = [] # heap points: remain_value
remain_value_lookup = {}
domain = {}


def print_board(board):
    """Helper function to print board in a square."""
    print "-----------------"
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print row


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """

    board2rv(board)
    result = backtracking(board)
    print(result)

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result


def get_arc(idx):
    """Get constraint related positions"""

    row_arc = [(idx[0] + COL[c]) for c in range(9)]
    col_arc = [(ROW[r] + idx[1]) for r in range(9)]

    i = ROW.index(idx[0]) / 3 * 3
    j = COL.index(idx[1]) / 3 * 3

    box_arc = [(ROW[r] + COL[c]) for r in range(i, i + 3) for c in range(j, j + 3)]
    return set(row_arc + col_arc + box_arc) - set([idx])


def board2rv(board):
    for r in range(9):
        for c in range(9):
            index = ROW[r] + COL[c]
            value = board[index]

            if value == 0:
                used_values = set([board[unit] for unit in get_arc(index)])
                set_domain(index, set(range(1, 10)) - used_values)
            else:
                domain[index] = set([value])


def set_value(board, idx, val):
    """set a value for one position and delete remaining value in heap"""
    board[idx] = val
    domain[idx] = set([val])
    if idx in remain_value_lookup:
        remain_value_lookup[idx][1] = None
        del remain_value_lookup[idx]


def set_domain(idx, dom):
    """Set domain for one position and update remaining value in heap"""
    domain[idx] = dom
    rv_entry = [len(dom), idx]
    if idx in remain_value_lookup:
        remain_value_lookup[idx][1] = None
    remain_value_lookup[idx] = rv_entry

    heappush(remain_value, rv_entry)


def forward_checking(idx, val):
    """Forward checking when assign a value for one position"""
    changed = []

    for target in get_arc(idx):
        target_domain = domain[target]
        if val in target_domain:
            if len(target_domain) == 1:
                return False, changed
            target_domain.remove(val)
            set_domain(target, target_domain)
            changed.append(target)
    return True, changed



def backtracking(board):
    """Takes a board and returns solved board."""

    idx = None
    while remain_value:
        rv, idx = heappop(remain_value)
        if idx is not None:
            break
    if not remain_value and idx is None:
        return board_to_string(board)

    old_domain = domain[idx]

    for val in old_domain:
        set_value(board, idx, val)
        consistent, changed = forward_checking(idx, val)
        if consistent and backtracking(board) is not None:
            return board_to_string(board)
        for target in changed:
            domain[target].add(val)
            set_domain(target, domain[target])

    board[idx] = 0
    set_domain(idx, old_domain)
    return None


if __name__ == '__main__':

    if len(sys.argv) > 1:  # Run a single board, as done during grading

        board = string_to_board(sys.argv[1])
        write_solved(board)


    else:
        print "Running all from sudokus_start"

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print "Error reading the sudoku file %s" % src_filename
            exit()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue
            print(line)
            # Parse boards to dict representation
            board = string_to_board(line)
            # print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')

        print "Finished all boards in file."

