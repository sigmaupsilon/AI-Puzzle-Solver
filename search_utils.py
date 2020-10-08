import sys
from re import search
from queue import PriorityQueue
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
        swap_index = -1
        swap_positions(left_board, empty_block, swap_index)

        if left_board not in expanded_boards:
            hn = get_hn(left_board, goal_state_brd, board_length)
            gn = get_gn(current_state, empty_block, swap_index)
            left_state = State(str(current_level) + '_' + str(id), current_state.id, left_board, gn, hn)
            expansions.append((left_state, "Left"))
            id += 1

    # Move up if we can
    if empty_block > 2:
        swap_index = -3
        swap_positions(up_board, empty_block, swap_index)

        if up_board not in expanded_boards:
            hn = get_hn(up_board, goal_state_brd, board_length)
            gn = get_gn(current_state, empty_block, swap_index)
            up_state = State(str(current_level) + '_' + str(id), current_state.id, up_board, gn, hn)
            expansions.append((up_state, "Up"))
            id += 1

    # Move right if we can
    if empty_block % 3 != 2:
        swap_index = 1
        swap_positions(right_board, empty_block, swap_index)

        if right_board not in expanded_boards:
            hn = get_hn(right_board, goal_state_brd, board_length)
            gn = get_gn(current_state, empty_block, swap_index)
            right_state = State(str(current_level) + '_' + str(id), current_state.id, right_board, gn, hn)
            expansions.append((right_state, "Right"))
            id += 1

    # Move down if we can
    if empty_block < board_length - 3:
        swap_index = 3
        swap_positions(down_board, empty_block, swap_index)

        if down_board not in expanded_boards:
            hn = get_hn(down_board, goal_state_brd, board_length)
            gn = get_gn(current_state, empty_block, swap_index)
            down_state = State(str(current_level) + '_' + str(id), current_state.id, down_board, gn, hn)
            expansions.append((down_state, "Down"))

    return expansions


def get_hn(target_state_brd: list, goal_state_brd: list, board_length: int) -> int:
    """Get h1(n) (equal to number of mismatches)"""
    count = 0

    for i in range(board_length):
        if target_state_brd[i] != goal_state_brd[i]:
            count += 1

    return count


def get_gn(current_state: State, empty_block: int, offset: int) -> int:
    """Return gn"""
    swap_val = int(current_state.cbrd[empty_block + offset])
    gn = current_state.gn

    if swap_val < 6:
        gn += 1
    elif swap_val < 16:
        gn += 3
    else:
        gn += 5

    return gn


def get_level(current_state: State) -> int:
    """Return current state level"""
    return int(current_state.id.split('_')[0])


def get_id_on_level(current_state: State) -> int:
    """Return id of current state based on level"""
    return int(current_state.id.split('_')[1])


def add_open_list_to_expanded(open_list: PriorityQueue, expanded_boards: list, index: int):
    """Add all boards in open list to another list"""
    for i in range(len(open_list.queue)):
        if open_list.queue[i][index][0].cbrd not in expanded_boards:
            expanded_boards.append(open_list.queue[i][index][0].cbrd)


def print_level(closed_list: list, index: int):
    """Print current level"""
    current_level = get_level(closed_list[index][0])
    previous_level = get_level(closed_list[index - 1][0])

    if index == 0 or current_level - previous_level != 0:
        print("\tLevel: " + str(current_level))


def print_state_detailed_output(closed_list: list, index: int, is_astar: bool):
    """Print state details"""
    if index == 0:
        print("\t\tRoot")
    elif index > 0 and closed_list[index][0].pid != closed_list[index - 1][0].pid:
        print("\t\tParent State ID: " + closed_list[index][0].pid)

    print("\t\t\tState ID: " + closed_list[index][0].id)
    print("\t\t\tBoard Config and Relative Movement to Parent: " + "[" +
          ', '.join(closed_list[index][0].cbrd) + "] - " + closed_list[index][1])

    if is_astar:
        print("\t\t\tg(n) = " + str(closed_list[index][0].gn) + ", h(n) = " + str(closed_list[index][0].hn) +
              ", f(n) = " + str(closed_list[index][0].fn) + "\n")


def print_output(closed_list: list, expanded_boards: list, is_astar: bool):
    """Print complete output"""
    print("Path-")
    for i in range(len(closed_list)):
        print_level(closed_list, i)
        print_state_detailed_output(closed_list, i, is_astar)

    print("\nNumber of nodes added to each list-" + " Open list: " + str(len(expanded_boards)) + ", Closed list: " +
          str(len(closed_list)))
