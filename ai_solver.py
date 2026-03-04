def minimax_ab(state, depth, alpha, beta, is_maximizing):
    """
        Rekursīva funkcija, kas aprēķina labāko iespējamo vērtību dotajai pozīcijai.
        - alpha: Labākais rezultāts, ko maksimizētājs (spēlētājs viens) jau ir garantējis sev šajā zarā.
        - beta: Labākais (mazākais) rezultāts, ko minimizētājs (spēlētājs divi) jau ir garantējis sev šajā zarā.
    """
    if state.is_empty() or depth == 0:
        return state.p1_points - state.p2_points

    if is_maximizing:
        max_eval = -float('inf')
        for move in state.generate_moves():
            child_state = state.apply_move(move)
            eval = minimax_ab(child_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.generate_moves():
            child_state = state.apply_move(move)
            eval = minimax_ab(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval
    
def evaluate_postition(state, depth):
    '''
        Atdod labāko kustību izmantojot minimax funkciju ar alpha-beta atcipršanas metodi 
    '''

    best_move = None
    best_value = -float('inf') if state.turn == 1 else float('inf')
    
    alpha = -float('inf')
    beta = float('inf')

    for move in state.generate_moves():
        child = state.apply_move(move)
        is_next_max = (child.turn == 1)
        val = minimax_ab(child, depth - 1, alpha, beta, is_next_max)

        if state.turn == 1:
            if val > best_value:
                best_value = val
                best_move = move
        else:
            if val < best_value:
                best_value = val
                best_move = move
    return best_move