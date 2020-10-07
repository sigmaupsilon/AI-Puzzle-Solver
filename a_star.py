import search_utils
from copy import deepcopy
from queue import PriorityQueue
from state import State


def add_open_list_to_expanded(open_list: PriorityQueue, expanded_boards: list):
    """Add all boards in open list to another list"""
    for i in range(len(open_list.queue)):
        if open_list.queue[i][1][0].cbrd not in expanded_boards:
            expanded_boards.append(open_list.queue[i][1][0].cbrd)


if __name__ == "__main__":
    # Retrieve boards and length
    input_lists = search_utils.parse_input()
    start_state_brd, goal_state_brd, board_length = input_lists[0], input_lists[1], input_lists[2]

    # Initialize empty closed list and list which will keep track of all boards that go in open list
    closed_list = []
    expanded_boards = []

    # Make sure the start state isn't already the goal state
    if start_state_brd != goal_state_brd:
        # Run initial heuristic and initialize start state. State ID is formatted as {level}_{level ID value}.
        # In BFSIS, f(n) = h(n)
        h = search_utils.get_hn(start_state_brd, goal_state_brd, board_length)
        current_state = State('0_0', None, start_state_brd, 0, h)
        level = search_utils.get_level(current_state)

        # Initialize open list
        open_list = PriorityQueue()

        # Put start state on open list and begin search. Quit if goal state is reached or 36+ levels are explored
        open_list.put((current_state.hn, deepcopy((current_state, "Start"))))
        while current_state.cbrd != goal_state_brd and level < 36:
            # Add boards of open list to expanded boards
            add_open_list_to_expanded(open_list, expanded_boards)

            # Get expanded children state and add highest priority state in open list to closed list
            expansions = search_utils.expand_all(current_state, goal_state_brd, board_length, expanded_boards)
            closed_list.append(open_list.get()[1])

            # Add expansions to open list
            for i in range(len(expansions)):
                open_list.put((expansions[i][0].fn, deepcopy(expansions[i])))

            # Update current state and level
            current_state = open_list.queue[0][1][0]
            level = search_utils.get_level(current_state)

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
                    search_utils.get_level(closed_list[i][0])) + ", Board Config and Movement: " + "[" +
                ', '.join(closed_list[i][0].cbrd) + "] - " + closed_list[i][1] + ", f(n): " + str(closed_list[i][0].fn))

        print("\nNumber of nodes added to open list: " + str(len(expanded_boards)) + " and closed list: " + str(
            len(closed_list)))
    else:
        print("Start state and Goal state inputs are equivalent!")
