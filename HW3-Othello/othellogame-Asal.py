'''
othellogame module

I have put my RandomPlayer, MinimaxPlayer and AlphabetaPlayer all in the same module.

I have added 2 different evaluation functions: Basic and Mobility
Basic evaluation function would just count the colors on the board
Mobility evaluation function besides counting colors, it would also consider mobility and corners
which are explained inside the function.
The mobility evaluation function works really well but it will take more time than basic.

I have put utility function outside the evaluation function for terminal states. It will return
a very big/low numbers for win/loss situations.

I have also put some helper functions like count_corners, count_colors as well to make things cleaner.

'''

import random
import copy
import time

WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 8
SKIP = "SKIP"
CORNERS = [(0, 0), (7, 0), (0, 7), (7, 7)]


class OthelloPlayerTemplate:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''

    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''
        return None


class HumanPlayer:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move == None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]

            if move == SKIP and SKIP in legals:
                return move

            try:
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move


class RandomPlayer:
    '''This would just return a random move from all legal moves '''
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move is None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))

            move = random.choice(legals)
            curr_move = move
            print("Random chosen move is: ", move)

        return curr_move


class OthelloState:
    '''A class to represent an othello game state'''

    def __init__(self, currentplayer, otherplayer, board_array=None, num_skips=0):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer


def player(state):
    return state.current


def actions(state):
    '''Return a list of possible actions given the current state
    '''
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i, j)) != None:
                legal_actions.append((i, j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions


def result(state, action):
    '''Returns the resulting state after taking the given action

    (This is the workhorse function for checking legal moves as well as making moves)

    If the given action is not legal, returns None

    '''
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    if action == SKIP:
        newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY:  # already we have a token on that square
        return None

    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array)) # num of skips is resetting here

    newstate.board_array[action[0]][action[1]] = color

    flipped = False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:  # make sure we are in the range of board
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:  # count tokens from other player
                count += 1
            elif newstate.board_array[x][y] == color:  # same player color at the end of line
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i + 1) * d[0]
            y = action[1] + (i + 1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        return newstate
    else:
        # if no pieces are flipped, it's not a legal move
        return None


def terminal_test(state):
    '''Simple terminal test
    '''
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False


def display(state):
    '''Displays the current state in the terminal window
    '''
    print('  ', end='')
    for i in range(SIZE):
        print(i, end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            else:
                print('-', end='')
        print()


def display_final(state):
    '''Displays the score and declares a winner (or tie)
    '''
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
    elif wcount < bcount:
        print("Black wins")
    else:
        print("Tie")


def count_colors(state, p):
    '''
    Helper function to count colors/discs of each player
    '''
    color = p.get_color()
    pcount, ocount = 0, 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == color:
                pcount += 1
            elif state.board_array[i][j] == -1 * color:
                ocount += 1
    return pcount, ocount


def count_corners(state, p):
    '''
    Helper function to see if there is any player in the corner
    '''
    color = p.get_color()
    player_corner, opponent_corner = 0, 0  #player corner, opponent corner
    for i in CORNERS:
        if state.board_array[i[0]][i[1]] == color:
            player_corner += 1
        elif state.board_array[i[0]][i[1]] == -1 * color:
            opponent_corner += 1
    return player_corner - opponent_corner


def mobility(state):
    '''
    this functions returns the mobility for each player
    mobility is the number of legal moves
    '''
    player_legal_actions = actions(state)
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array))
    opponent_legal_actions = actions(newstate)
    return len(player_legal_actions) - len(opponent_legal_actions)


def utility(state, p):
    '''
    Utility funciton is used on terminal states only
    it will return very big value if it is a win state, and very low value when it is a loss state
    '''
    pcount, ocount = count_colors(state, p)
    if pcount > ocount:
        return 1000  # win
    else:
        return -1000  # loss


def basic_eval(state, p):
    '''
    This is just a basic eval function that subtract opponent's discs from player discs
    '''
    if terminal_test(state):
        return utility(state, p)
    else:
        pcount, ocount = count_colors(state, p)
        return pcount - ocount


def mobility_eval(state, p):
    ''' Mobility technique : The more the mobility, the higher chance for winning
        count players & opponents num of moves
        additionaly I am also considering corners in my evaluation technique
    '''
    if terminal_test(state):
        return utility(state, p)
    else:
        pcount, ocount = count_colors(state, p)  # counting colors for each player
        corners = count_corners(state, p)  # counting corners for each player
        mobilities = mobility(state)  # mobility for player & opponent
        return (pcount - ocount) + 2 * mobilities + corners


class MinimaxPlayer:

    def __init__(self, mycolor, depth_limit=4):
        self.color = mycolor
        self.depth_limit = depth_limit

    def get_color(self):
        return self.color

    def get_limit(self):
        return self.depth_limit

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state'''
        display(state)
        if self.color == 1:
            p_str = "White"
            print("White ", end='')
        else:
            p_str = "Black"
            print("Black ", end='')
        print(" to play.")
        legals = actions(state)
        print("Legal moves are " + str(legals))

        move = minimax_search(state, self.get_limit())
        print(p_str + " move is: ", move)
        return move


def minimax_search(state, depth):
    global_player = player(state)
    val, move = max_value(global_player, state, depth)
    return move


def max_value(global_p, state, depth):
    if depth == 0 or terminal_test(state):
        return basic_eval(state, global_p), None  # you can change evaluation function here

    v, move = float("-inf"), None
    for a in actions(state):
        d = depth
        v2, a2 = min_value(global_p, result(state, a), d-1)
        if v2 > v:
            v, move = v2, a
    return v, move


def min_value(global_p, state, depth):
    if depth == 0 or terminal_test(state):
        return basic_eval(state, global_p), None  # you can change evaluation function here

    v, move = float("inf"), None
    for a in actions(state):
        d = depth
        v2, a2 = max_value(global_p, result(state, a), d-1)
        if v2 < v:
            v, move = v2, a
    return v, move


class AlphabetaPlayer:

    def __init__(self, mycolor, depth_limit=4):
        self.color = mycolor
        self.depth_limit = depth_limit

    def get_color(self):
        return self.color

    def get_limit(self):
        return self.depth_limit

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state'''
        display(state)
        if self.color == 1:
            p_str = "White"
            print("White ", end='')
        else:
            p_str = "Black"
            print("Black ", end='')
        print(" to play.")
        legals = actions(state)
        print("Legal moves are " + str(legals))

        move = ab_search(state, self.get_limit())
        print(p_str + " move is: ", move)
        return move


def ab_search(state, depth):
    global_player = player(state)
    val, move = ab_max_value(global_player, state, depth, float("-inf"), float("inf"))
    return move


def ab_max_value(global_p, state, depth, alpha, beta):
    if depth == 0 or terminal_test(state):
        return mobility_eval(state, global_p), None  # you can change evaluation function here

    v, move = float("-inf"), None
    for a in actions(state):
        d = depth
        v2, a2 = ab_min_value(global_p, result(state, a), d-1, alpha, beta)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move


def ab_min_value(global_p, state, depth, alpha, beta):
    if depth == 0 or terminal_test(state):
        return mobility_eval(state, global_p), None  # you can change evaluation function here

    v, move = float("inf"), None
    for a in actions(state):
        d = depth
        v2, a2 = ab_max_value(global_p, result(state, a), d - 1, alpha, beta)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move


def play_game(p1=None, p2=None):
    '''Plays a game with two players. By default, uses two humans
    '''
    if p1 == None:
        p1 = AlphabetaPlayer(BLACK, 4)
    if p2 == None:
        p2 = RandomPlayer(WHITE)

    s = OthelloState(p1, p2)
    while True:
        action = p1.make_move(s)
        if action not in actions(s):
            print("Illegal move made by Black")
            print("White wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        if action not in actions(s):
            print("Illegal move made by White")
            print("Black wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return



def main():
    start_time = time.time()
    play_game()
    print("The search took ", time.time() - start_time, " seconds")

if __name__ == '__main__':
    main()
