import search_utils
from copy import deepcopy
from queue import PriorityQueue
from state import State


def a_star(open_list: PriorityQueue, closed_list: list, current_state: State, goal_state_brd: list, board_length: int,
           expanded_boards: list, h_type: int) -> bool:
    """A* Search. Return boolean depending on whether or not goal state is found"""
    # Retrieve current level. Return false 36+ levels are explored
    level = search_utils.get_level(current_state)

    if level > 35:
        return False

    # Add boards of open list to expanded boards
    search_utils.add_open_list_to_expanded(open_list, expanded_boards, 3)

    # Get expanded children state and add highest priority state in open list to closed list
    expansions = search_utils.expand_all(current_state, goal_state_brd, board_length, expanded_boards, True, h_type)
    closed_list.append(open_list.get()[3])

    # Add expansions to open list
    for i in range(len(expansions)):
        open_list.put((expansions[i][0].fn, search_utils.get_level(expansions[i][0]),
                       search_utils.get_id_on_level(expansions[i][0]), deepcopy(expansions[i])))

    # Return True if goal state is found
    if closed_list[-1][0].cbrd == goal_state_brd:
        return True

    # Update current state and level
    current_state = open_list.queue[0][3][0]

    return a_star(open_list, closed_list, current_state, goal_state_brd, board_length, expanded_boards, h_type)


def a_star_wrapper(h_type: int, first_arg: str, second_arg: str):
    """A* Search Wrapper"""
    # Retrieve boards and length
    input_lists = search_utils.parse_input(first_arg, second_arg)
    start_state_brd, goal_state_brd, board_length = input_lists[0], input_lists[1], input_lists[2]

    # Initialize empty closed list and list which will keep track of all boards that go in open list
    closed_list = []
    expanded_boards = []

    # Make sure the start state isn't already the goal state
    if start_state_brd != goal_state_brd:
        # Run initial heuristic and initialize start state. State ID is formatted as {level}_{level ID value}.
        # In A*, f(n) = h(n) + g(n)
        h = search_utils.get_hn(start_state_brd, goal_state_brd, board_length, h_type)
        current_state = State("0_0", "", start_state_brd, 0, h)

        # Initialize open list
        open_list = PriorityQueue()

        # Put start state on open list and begin search. Quit if goal state is reached or 36+ levels are explored
        open_list.put((current_state.fn, search_utils.get_level(current_state),
                       search_utils.get_id_on_level(current_state), deepcopy((current_state, "Start"))))

        # Run A* and Print results
        if a_star(open_list, closed_list, current_state, goal_state_brd, board_length, expanded_boards, h_type):
            print("Goal state found!\n")
        else:
            print("No solution found! Quit after 36 levels.\n")

        search_utils.print_output(closed_list, expanded_boards, True)
    else:
        print("Start state and Goal state inputs are equivalent!")
