import sys
import re
from copy import deepcopy
from queue import PriorityQueue
from state import State


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
    if empty_block < 15:
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


if __name__ == "__main__":
    # Parse arguments and convert each to list
    start_state_brd = re.search(r"\[([0-9,]+)]", sys.argv[1]).group(1).split(',')
    goal_state_brd = re.search(r"\[([0-9,]+)]", sys.argv[2]).group(1).split(',')

    # Get board length (6x3 expected) and initialize list for all expanded states and boards
    board_length = len(goal_state_brd)
    expanded_boards = []

    # Initialize empty closed list
    closed_list = []

    # Make sure the start state isn't already the goal state
    if start_state_brd != goal_state_brd:
        # Run initial heuristic and initialize start state. State ID is formatted as {level}_{level ID value}.
        # In BFS, f(n) = h(n)
        h = get_heuristic(start_state_brd, goal_state_brd, board_length)
        current_state = State('0_0', None, start_state_brd, 0, h)
        level = get_level(current_state)

        # Initialize open list
        open_list = PriorityQueue()

        # Put start state on open list and begin search. Quit if goal state is reached or 10+ levels are explored
        open_list.put((current_state.hn, deepcopy((current_state, "Start"))))
        while current_state.cbrd != goal_state_brd or level > 36:
            # Add all unique states and boards in open list to another list
            for i in range(len(open_list.queue)):
                if open_list.queue[i][1][0].cbrd not in expanded_boards:
                    expanded_boards.append(open_list.queue[i][1][0].cbrd)

            # Get expanded children state and add highest priority state in open list to closed list
            expansions = expand_all(current_state, goal_state_brd, board_length, expanded_boards)
            closed_list.append(open_list.get()[1])

            # Add expansions to open list
            for i in range(len(expansions)):
                open_list.put((expansions[i][0].fn, deepcopy(expansions[i])))

            # Update current state and level
            current_state = open_list.queue[0][1][0]
            level = get_level(current_state)

        # Add final highest-priority open list state to closed list
        closed_list.append(open_list.get()[1])

    # Print results
    if closed_list[-1][0].cbrd == goal_state_brd:
        print("Goal state found!\n")
    else:
        print("No solution found! Quit after 36 levels.\n")

    print("Path-")
    for i in range(len(closed_list)):
        print(
            "\tState ID: " + closed_list[i][0].id + ", Level: " + str(
                get_level(closed_list[i][0])) + ", Board Config and Movement: " + "[" +
            ', '.join(closed_list[i][0].cbrd) + "] - " + closed_list[i][1] + ", f(n): " + str(closed_list[i][0].fn))

    print("\nNumber of nodes added to open list: " + str(len(expanded_boards)) + " and closed list: " + str(
        len(closed_list)))
