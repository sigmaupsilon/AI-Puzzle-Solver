import sys
import copy
from queue import PriorityQueue


class State:
    def __init__(self, id, pid, cbrd, gn, hn, lvl):
        self.id = id
        self.pid = pid
        self.cbrd = cbrd
        self.gn = gn
        self.hn = hn
        self.fn = gn + hn
        self.lvl = lvl


def swapPositions(list: list, empty_block: int, offset: int) -> list:
    list[empty_block], list[empty_block+offset] = list[empty_block+offset], list[empty_block]


def expandAll(current_state: State, goal_state_brd: list, board_length: int) -> tuple:
    empty_block = current_state.cbrd.index(0)
    current_level = current_state.lvl + 1
    left_switch = current_state.cbrd.copy()
    right_switch = current_state.cbrd.copy()
    up_switch = current_state.cbrd.copy()
    down_switch =  current_state.cbrd.copy()

    swapPositions(left_switch, empty_block, -1)
    swapPositions(right_switch, empty_block, 1)
    swapPositions(up_switch, empty_block, -3)
    swapPositions(down_switch, empty_block, 3)

    lh = getHeuristic(left_switch, goal_state_brd, board_length)
    left_state = State(current_state.id + 1, current_state.id, left_switch, board_length - lh, lh, current_level)
    rh = getHeuristic(right_switch, goal_state_brd, board_length)
    right_state = State(current_state.id + 2, current_state.id, right_switch, board_length - rh, rh, current_level)
    uh = getHeuristic(up_switch, goal_state_brd, board_length)
    up_state = State(current_state.id + 3, current_state.id, up_switch, board_length - uh, uh, current_level)
    dh = getHeuristic(down_switch, goal_state_brd, board_length)
    down_state = State(current_state.id + 4, current_state.id, down_switch, board_length - dh, dh, current_level)

    expansions = (left_state, right_state, up_state, down_state)

    return expansions


def getHeuristic(target_state_brd: list, goal_state_brd: list, board_length: int) -> int:
    count = 0

    for i in range(board_length):
        if target_state_brd[i] != goal_state_brd[i]:
            count += 1

    return count

if __name__ == "__main__":
    start_state_brd = sys.argv[1].split(',') 
    goal_state_brd = sys.argv[2].split(',')
    board_length = len(goal_state_brd)

    if start_state_brd != goal_state_brd:
        heuristic = getHeuristic(start_state_brd, goal_state_brd, board_length)
        current_state = State(0, None, start_state_brd, board_length - heuristic, heuristic, 0)
        open_list = PriorityQueue()
        closed_list = []
        open_list.put((copy.copy(current_state.hn), copy.deepcopy(current_state)))
        while current_state.cbrd != goal_state_brd:
            expansions = expandAll(current_state, goal_state_brd, board_length)
            closed_list.append(open_list.get()[1])
            for i in range(len(expansions)):
                open_list.put((copy.copy(expansions[i].hn), copy.deepcopy(expansions[i])))
            current_state = open_list.queue[0][1]
        closed_list.append(open_list.get()[1])
