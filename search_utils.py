import sys
from re import search
from state import State


def parse_input() -> list:
    """Parse input arguments and return [start_state_brd, goal_state_brd, board_length (6x3 configuration)]"""
    start_state_brd = search(r"\[([0-9,]+)]", sys.argv[1]).group(1).split(',')
    goal_state_brd = search(r"\[([0-9,]+)]", sys.argv[2]).group(1).split(',')
    return [start_state_brd, goal_state_brd, len(goal_state_brd)]


def swap_positions(list: list, empty_block: int, offset: int):
    """Swap position of two elements in a list"""
    pos2 = empty_block + offset
    list[empty_block], list[pos2] = list[pos2], list[empty_block]


def expand_all(current_state: State, goal_state_brd: list, board_length: int, expanded_boards: list) -> list:
    """Expand child states and return them"""
    # Initialize empty block and possible board movements
    empty_block = current_state.cbrd.index('0')
    left_board = current_state.cbrd.copy()
    right_board = current_state.cbrd.copy()
    up_board = current_state.cbrd.copy()
    down_board = current_state.cbrd.copy()

    # Initialize current level and ID for specific state for level
    current_level = get_level(current_state) + 1
    id = 0

    # Initialize empty list of all expansion possibilities
    expansions = []

    # Move left if we can
    if empty_block % 3 != 0:
        swap_positions(left_board, empty_block, -1)

        if left_board not in expanded_boards:
            lh = get_heuristic(left_board, goal_state_brd, board_length)
            left_state = State(str(current_level) + '_' + str(id), current_state.id, left_board, 0, lh)
            expansions.append((left_state, "Left"))
            id += 1

    # Move up if we can
    if empty_block > 2:
        swap_positions(up_board, empty_block, -3)

        if up_board not in expanded_boards:
            uh = get_heuristic(up_board, goal_state_brd, board_length)
            up_state = State(str(current_level) + '_' + str(id), current_state.id, up_board, 0, uh)
            expansions.append((up_state, "Up"))
            id += 1

    # Move right if we can
    if empty_block % 3 != 2:
        swap_positions(right_board, empty_block, 1)

        if right_board not in expanded_boards:
            rh = get_heuristic(right_board, goal_state_brd, board_length)
            right_state = State(str(current_level) + '_' + str(id), current_state.id, right_board, 0, rh)
            expansions.append((right_state, "Right"))
            id += 1

    # Move down if we can
    if empty_block < board_length - 3:
        swap_positions(down_board, empty_block, 3)

        if down_board not in expanded_boards:
            dh = get_heuristic(down_board, goal_state_brd, board_length)
            down_state = State(str(current_level) + '_' + str(id), current_state.id, down_board, 0, dh)
            expansions.append((down_state, "Down"))

    return expansions


def get_heuristic(target_state_brd: list, goal_state_brd: list, board_length: int) -> int:
    """Get h(n) (equal to number of mismatches)"""
    count = 0

    for i in range(board_length):
        if target_state_brd[i] != goal_state_brd[i]:
            count += 1

    return count


def get_level(current_state: State) -> int:
    """Return current state level"""
    return int(current_state.id.split('_')[0])


def get_id_on_level(current_state: State) -> int:
    """Return id of current state based on level"""
    return int(current_state.id.split('_')[1])


def print_level(closed_list: list, index: int):
    """Print current level"""
    current_level = get_level(closed_list[index][0])
    previous_level = get_level(closed_list[index - 1][0])

    if index == 0 or current_level - previous_level != 0:
        print("\tLevel: " + str(current_level))
