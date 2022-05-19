import random
import math


# use a list of numbers from 1 to 8 [ 1,2,3,4,5,6,7,8] , index = column number+1, value = row number
# successors for steepest ascent are 56 other states, for first choice and simulated annealing just another random successor
# objective function(attacks): not matching numbers in the list and (index - index != value - value)


def attacks(state: list):  # Objective function accepting list right now

    h = 0  # number of attacks
    # ls = [int(x) for x in str(state)] in case we want to pass integers
    # Horizontal
    if len(state) > len(set(state)):
        h += (len(state) - len(set(state)))
    # Diagonal
    for i in range(0, len(state)):
        for j in range(i + 1, len(state)):
            if abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h


def neighbors_min(state: list):
    current = state.copy()
    neighbors_dict = {}  # state:heuristic

    # based on book, for each state we have 8*7=56 neighbors
    for i in range(0, len(current)):
        for j in range(1, len(current) + 1):
            if j != current[i]:
                temp_neighbor = current.copy()
                temp_neighbor[i] = j

                # changing list to int for saving it in neighbors dictionary
                temp_int = int("".join(list(map(str, temp_neighbor[::]))))
                neighbors_dict[temp_int] = attacks(temp_neighbor)  # list of neighbors' evaluation value

    # finding min value from dictionary (which is the states with least num of attacks)
    m_val = min(neighbors_dict.values())
    m = list(filter(lambda x: neighbors_dict[x] == m_val, neighbors_dict))

    # saving states with minimum num of attacks in this list
    best_neighbors = []
    if len(m) > 1:
        for i in m:
            best_neighbors.append(i)

    # if there are more than one better solution then choose one of them randomly
    if len(best_neighbors) > 1:
        random_index = random.randint(0, len(best_neighbors) - 1)
        best = best_neighbors[random_index]
        best_ls = [int(x) for x in str(best)]
    elif len(best_neighbors) == 1:
        best_ls = best_neighbors[0]
    else:
        best_ls = current

    return best_ls


def neighbors_random(s):
    current = s.copy()

    while True:
        temp = [random.randint(1, 8) for i in range(8)]
        if temp == current:
            pass
        else:
            return temp


def hillclimb_sa(initial_state):
    n = 0  # num of steps to a solution
    current = initial_state.copy()
    while True:
        if attacks(current) == 0:
            print("Hurray, num of steps it took is: ", n)
            return current
        n += 1
        neighbor = neighbors_min(current)
        # for debugging...
        t = attacks(current)
        a = attacks(neighbor)
        if attacks(neighbor) >= attacks(current):
            # print("Local max or plataeu")
            return current
        current = neighbor


def hillclimb_fc(initial_state, equals=False, visited=False, max_num=False, max_n=100):
    n = 0  # num of steps to a solution
    current = initial_state.copy()
    if visited:
        visited_ls = []  # list of visited neighbors
    while True:
        if attacks(current) == 0:
            print("Hurray, num of steps it took is: ", n)
            return current

        if max_num and max_n <= 0:
            return current
        n += 1
        neighbor = neighbors_random(current)
        neighbor_int = int("".join(list(map(str, neighbor[::]))))
        # for debugging...
        t = attacks(current)
        a = attacks(neighbor)

        if visited:
            if attacks(neighbor) < attacks(current) and neighbor_int not in visited_ls:
                current = neighbor
                visited_ls.append(neighbor_int)
        else:
            if attacks(neighbor) < attacks(current):
                current = neighbor

        if equals:
            if attacks(neighbor) == attacks(current):
                return current
        elif max_num:
            max_n -= 1


def sim_anneal(initial_state, temperature):  # T= Temperature  VALUE = Objective Function
    n = 0  # num of steps to a solution
    current = initial_state
    i, t = 1, temperature
    while t > 0:
        if attacks(current) == 0:
            print("Hurray, num of steps it took is: ", n)
            return current
        n += 1
        # Different cooling functions are here as comments
        # t -= i
        # t -= 1
        # t *= 0.2
        # t = temperature + 0.8 ** i
        t = temperature / (1 + math.log(1 + i, 10))

        if t == 0:
            return current

        neighbor = neighbors_random(current)
        deltaE = attacks(current) - attacks(neighbor)
        i += 1
        if deltaE > 0 or random.random() < math.exp(deltaE / t):
            current = neighbor.copy()

    return current


# Let's create 1000 random initial states and then run each algorithm with all these random states.
# If the algorithm gets to a solution, it will print out "Hurray" along with number of steps it has taken.
for k in range(1000):
    temp = [random.randint(1, 8) for i in range(8)]
    #hillclimb_sa(temp)
    #hillclimb_fc(temp, False, True, True, 500)
    sim_anneal(temp, 500)
