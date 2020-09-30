import search_utils
from copy import deepcopy
from queue import PriorityQueue
from state import State


def add_open_list_to_expanded(open_list: PriorityQueue, expanded_boards: list):
    """Add all boards in open list to another list"""
    for i in range(len(open_list.queue)):
        if open_list.queue[i][2][0].cbrd not in expanded_boards:
            expanded_boards.append(open_list.queue[i][2][0].cbrd)


def print_state_detailed_output(closed_list: list, index: int):
    """Print state details"""
    if index == 0:
        print("\t\tRoot")
    elif index > 0 and closed_list[index][0].pid != closed_list[index - 1][0].pid:
        print("\t\tParent State ID: " + closed_list[index][0].pid)

    print("\t\t\tState ID: " + closed_list[index][0].id)
    print("\t\t\tBoard Config and Relative Movement to Parent: " + "[" +
          ', '.join(closed_list[index][0].cbrd) + "] - " + closed_list[index][1] + "\n")


def bfs(open_list: PriorityQueue, closed_list: list, expand_state: State, goal_state_brd: list, board_length: int,
        expanded_boards: list) -> bool:
    """BFS search. Return True if goal was found and False on timeout"""
    # Retrieve current level. Return false 36+ levels are explored
    level = search_utils.get_level(expand_state)

    if level > 35:
        return False

    # Get expanded children state
    expansions = search_utils.expand_all(expand_state, goal_state_brd, board_length, expanded_boards)

    # Add expansions to open list
    for i in range(len(expansions)):
        open_list.put((level, search_utils.get_id_on_level(expansions[i][0]),
                       deepcopy(expansions[i])))

    # Add boards of open list to expanded boards
    add_open_list_to_expanded(open_list, expanded_boards)

    # Check if state boards equal goal board and add analyzed states to closed list
    for i in range(len(open_list.queue)):
        closed_list.append(open_list.get()[2])
        if closed_list[-1][0].cbrd == goal_state_brd:
            return True

    # Left-most parent of next state should be expanded
    next_expansion_index = [cl[0].cbrd for cl in closed_list].index(expand_state.cbrd) + 1
    expand_state = closed_list[next_expansion_index][0]

    return bfs(open_list, closed_list, expand_state, goal_state_brd, board_length, expanded_boards)


if __name__ == "__main__":
    # Retrieve boards and length
    input_lists = search_utils.parse_input()
    start_state_brd, goal_state_brd, board_length = input_lists[0], input_lists[1], input_lists[2]

    # Initialize empty closed list and list which will keep track of all boards that go in open list
    closed_list = []
    expanded_boards = []

    # Make sure the start state isn't already the goal state
    if start_state_brd != goal_state_brd:
        # Initialize start state. State ID is formatted as {level}_{level ID value}.
        # Initialize open list and boolean for if goal state is found
        expand_state = State('0_0', None, start_state_brd, 0, 0)
        open_list = PriorityQueue()

        # Put start state on open list
        open_list.put((search_utils.get_level(expand_state), search_utils.get_id_on_level(expand_state),
                       deepcopy((expand_state, "Start"))))

        # Run BFS and print results
        if bfs(open_list, closed_list, expand_state, goal_state_brd, board_length, expanded_boards):
            print("Goal state found!\n")
        else:
            print("No solution found! Quit after 36 levels.\n")

        print("Path-")
        for i in range(len(closed_list)):
            search_utils.print_level(closed_list, i)
            print_state_detailed_output(closed_list, i)

        print("\nNumber of nodes added to each list-" + " Open list: " + str(len(expanded_boards)) + ", Closed list: " +
              str(len(closed_list)))
    else:
        print("Start state and Goal state inputs are equivalent!")
