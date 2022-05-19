# psuedocode for alpha-beta pruning

def ab_search(game, state):
    global PLAYER
    PLAYER = game.to_move(state)
    value, move = ab_max_value(game, state, -inf, inf)
    return move

def ab_max_value(game, state, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, PLAYER), None
    v, move = -inf, None
    for a in game.actions(state):
        v2, a2 = ab_min_value(game, game.result(state, a), alpha, beta)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta: return v, move
    return v, move

def ab_min_value(game, state, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, PLAYER), None
    v, move = inf, None
    for a in game.actions(state):
        v2, a2 = ab_max_value(game, game.result(state, a), alpha, beta)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha: return v, move
    return v, move
