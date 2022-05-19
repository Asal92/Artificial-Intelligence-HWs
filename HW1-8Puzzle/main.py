import sys
import copy
import time
import heapq
from queue import LifoQueue

# Global Variables
goal_state = 123804765
goal_ls = [int(x) for x in str(goal_state)]

'''
I am passing states as an integer then I will convert them to a list to run my actions on,
Thus I had to be careful when the position of 0 is index(0). 
while comparing to goal or getting the children of a node, I will check the length of my state list, 
if it is less than 9, I will insert 0 at index(0) and then will implement actions.
'''


class Node:
    def __init__(self, state: int = 0, parent: int = 0, action="", path_cost: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def Node_State(self):
        return self.state

    def Node_IsGoal(self):
        #converting self (int) to list to compare
        sl = [int(x) for x in str(self.state)]
        # Taking care of 0 when it is in index 0
        if len(sl) < 9:
            sl.insert(0, 0)
        if sl == goal_ls:
            return True
        else:
            return False

'''
8-Puzzle

0 | 2 | 3
8 | - | 4
7 | 6 | 5

internal state representation of the grid above is : 123405678  

'''


def visualize(state):
    i = 0  # for iterating through the list
    a = [int(x) for x in str(state)]

    if len(a) < 9:  # meaning the first digit is 0
        a.insert(0, 0)

    while i < len(a):
        print(" | ".join(map(str, a[i:i + 3])), "|")
        i += 3


def child_node(node: Node, action: str):
    child = Node()

    # saving input state as a list
    n = [int(x) for x in str(node.Node_State())]

    # Taking care of 0 when it is in index 0
    if len(n) < 9:
        n.insert(0, 0)

    # copying list of input state into another list to keep parent state while swapping values
    new_n = copy.deepcopy(n)

    zero_ind = n.index(0)  # finding the index of the empty tile

    # I am limiting my actions based on the position of the 0 index,
    # so e.g. if 0 is at index 0, it can only perform Left and Up
    if action == "Right":
        if (zero_ind == 0) or (zero_ind == 3) or (zero_ind == 6):
            return
        else:
            new_n[zero_ind], new_n[zero_ind - 1] = new_n[zero_ind - 1], new_n[zero_ind]

    elif action == "Left":
        if (zero_ind == 2) or (zero_ind == 5) or (zero_ind == 8):
            return
        else:
            new_n[zero_ind], new_n[zero_ind + 1] = new_n[zero_ind + 1], new_n[zero_ind]

    elif action == "Up":
        if (zero_ind == 6) or (zero_ind == 7) or (zero_ind == 8):
            return
        else:
            new_n[zero_ind], new_n[zero_ind + 3] = new_n[zero_ind + 3], new_n[zero_ind]

    elif action == "Down":
        if (zero_ind == 0) or (zero_ind == 1) or (zero_ind == 2):
            return
        else:
            new_n[zero_ind], new_n[zero_ind - 3] = new_n[zero_ind - 3], new_n[zero_ind]

    # converting my lists to integer again to update my child node
    child.parent = int("".join(list(map(str, n[::]))))
    child.state = int("".join(list(map(str, new_n[::]))))
    child.path_cost = node.path_cost + 1
    child.action = action

    return child


# Getting the frontiers from expand function
def expand(node: Node):
    neighbor = Node()
    children = []
    my_actions = ["Right", "Left", "Up", "Down"]

    state = [int(x) for x in str(node.Node_State())]

    if len(state) < 9:
        state.insert(0, 0)

    zero_ind = state.index(0)

    # in child_node, I am limiting my actions based on the index of 0
    # but here I am being extra cautious with the actions I shall do
    if zero_ind == 0:
        my_actions.remove("Right")
        my_actions.remove("Down")
    elif zero_ind == 1:
        my_actions.remove("Down")
    elif zero_ind == 2:
        my_actions.remove("Left")
        my_actions.remove("Down")
    elif zero_ind == 3:
        my_actions.remove("Right")
    elif zero_ind == 5:
        my_actions.remove("Left")
    elif zero_ind == 6:
        my_actions.remove("Right")
        my_actions.remove("Up")
    elif zero_ind == 7:
        my_actions.remove("Up")
    elif zero_ind == 8:
        my_actions.remove("Left")
        my_actions.remove("Up")

    for actions in my_actions:
        neighbor = child_node(node, actions)
        children.append(neighbor)

    return children


'''
    *******************
    Uninformed Searches 
    *******************
'''


# Depth-First Search
def dfs(initial_state: int):

    start_time = time.time()
    start_node = Node(initial_state, 0, "", 0)
    # using LIFO Queue for my frontier to pop the last node
    # and using dictionary{state: node} for my visited nodes
    frontier = LifoQueue(maxsize=60000)
    frontier.put(start_node)
    visited = {initial_state: start_node}
    children = []
    depth = 0

    while not frontier.empty():
        x = Node(0, 0, "", 0)
        x = frontier.get()
        print(x.Node_State())

        if x.Node_IsGoal():
            result = True
            end_time = time.time()
            print(f'Time taken for Depth-First Search is {end_time - start_time} seconds')
            print("Hurray, Goal is found")
            print(f'Depth is {depth}')
            return True

        depth += 1
        children = expand(x)

        for child in children:
            s = child.state
            if s not in visited.keys():
                visited[child.state] = child
                frontier.put(child, block=False)

    return False


# Depth-Limited Search
def dls(initial_state: int, limit: int):

    start_node = Node(initial_state, 0, "", 0)
    # using regular list for my frontier and then will pop the last element
    # and using dictionary{node: node.path_cost} for my visited nodes
    frontier = [start_node]
    visited = {}
    children = []
    act_ls = []

    while len(frontier) > 0:

        x = frontier.pop()
        act_ls.append(x.action)

        if x.Node_IsGoal():
            print("Hurray, Goal is found")
            act_ls.pop(0)
            print(act_ls)
            return True

        if x.path_cost <= limit:
            visited[x] = x.path_cost
            children = expand(x)
            for child in children:
                if child not in visited.keys() or child.path_cost < visited[child]:
                    frontier.append(child)

    return False


# Iterative Deepening Search
def ids(initial_state: int):

    depth: int = 1
    result = False

    while result is False:

        start_node = Node(initial_state, 0, "", 0)
        result = dls(start_node.state, depth)
        depth += 1

    return result


'''
    *******************
    Informed Searches 
    *******************
'''


# Heuristic Functions ( num of wrong tiles & Manhattan Distance )
def num_wrong_tiles(state: int):
    n = 0

    current_state = state
    cur_ls = [int(x) for x in str(current_state)]

    if len(cur_ls) < 9:
        cur_ls.insert(0, 0)

    for i in range(len(cur_ls)):  # what is current state starts with 0?
        if cur_ls[i] != goal_ls[i]:
            n += 1

    return n


def manhattan_distance(state: int):
    cur_ls = [int(x) for x in str(state)]
    if len(cur_ls) < 9:
        cur_ls.insert(0, 0)

    return sum(abs((b // 3) - (g // 3)) + abs((b % 3) - (g % 3))
               for b, g in ((cur_ls.index(i), goal_ls.index(i)) for i in range(len(cur_ls))))


# A* Search Algorithm -> cost f(n) = g(n) + h(n) -> g(n) = path cost, h(n) = heuristic cost
def astar(*args):

    initial_state = args[0]
    h = args[1]
    cnt = 0
    start_node = Node(initial_state, 0, "", 0)
    # using heapq as a priority queue for my frontier
    # and using dictionary{state: node} for my visited nodes
    frontier = []
    # cnt as counter for states with same heuristic and node
    heapq.heappush(frontier, (h(initial_state), cnt, start_node))
    visited = {initial_state: start_node}
    children = []
    act_ls = []

    while len(frontier) > 0:

        y = heapq.heappop(frontier)
        x = y[2]
        act_ls.append(x.action)

        if x.Node_IsGoal():
            print("Hurray, Goal is found")
            act_ls.pop(0)
            print(act_ls)
            return True

        visited[x.state] = x
        children = expand(x)
        for child in children:
            s = child.state
            if s not in visited.keys():
                cost = h(child.state) + child.path_cost
                # this cnt helps to save a node with better heuristic even if the node already exists in priority queue
                cnt += 1
                heapq.heappush(frontier, (cost, cnt, child))

    return False


def main():

    # command line arguments
    # only accepting one argument from command line
    if len(sys.argv) > 2:
        print(" Sorry, I can only accept one argument! :) ")
    elif len(sys.argv) == 2:
        arg = int(sys.argv[1])  # argv[0] = main.py so argv[1] = initial state

        print("\n")
        print(f'>>>initial state is: {arg}')
        print("\n")
        
        print("Iterative Deepening Search begins...")
        start_time = time.time()
        result = ids(arg)
        end_time = time.time()
        print(f'Time taken for Iterative Deepening Search is {end_time - start_time} seconds')
        
        print("\n")
        print("\n")

        print("AStar Search with num_wrong_tiles begins...")
        start_time = time.time()
        result = astar(arg, num_wrong_tiles)
        end_time = time.time()
        print(f'Time taken for AStar Search with num_wrong_tiles is {end_time - start_time} seconds')

        print("\n")
        print("\n")
        
        print("AStar Search with manhattan_distance begins...")
        start_time = time.time()
        result = astar(arg, manhattan_distance)
        end_time = time.time()
        print(f'Time taken for AStar Search with manhattan_distance is {end_time - start_time} seconds')

        print("\n")

if __name__ == "__main__":
    main()