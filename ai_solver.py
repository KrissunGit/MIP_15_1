import random

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
    
def inv_minimax_ab(state, depth, alpha, beta, is_maximizing):   
    if state.is_empty() or depth == 0:
        return state.p2_points - state.p1_points

    if is_maximizing:
        max_eval = -float('inf')
        for move in state.generate_moves():
            child_state = state.apply_move(move)
            eval = inv_minimax_ab(child_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.generate_moves():
            child_state = state.apply_move(move)
            eval = inv_minimax_ab(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval

def evaluate_position(state, depth, movelist, move_index):

    '''
        Atdod labāko kustību izmantojot minimax funkciju ar alpha-beta atcipršanas metodi 
    '''
    best_move = None
    if state.turn == 1:
        best_value = -float('inf')
    else:
        best_value = float('inf')
    alpha = -float('inf') # Alpha definešana, kā negatīva bezgalība
    beta = float('inf') # Beta definešana, kā pozitīva bezgalība)
    
    # Nākamo pāris kustību simulēšana izmantojot generate_moves un apply_move
    for move in state.generate_moves():
        child = state.apply_move(move)
        is_next_max = (child.turn == 1)
        val = calc_move(child,movelist, move_index, alpha,beta,is_next_max,depth)
        if state.turn == 1:
            if val > best_value:
                best_value = val
                best_move = move
        else:
            if val < best_value:
                best_value = val
                best_move = move
    return best_move

def calc_move(child, movelist, move_index, alpha,beta,is_next_max, depth):
    match movelist[move_index]:
        case 1:
            val = inv_minimax_ab(child, depth-1, alpha, beta, is_next_max)
        case 2:
            val = minimax_ab(child, depth-1, alpha, beta, is_next_max)
        case 0:
            if random.random() < 0.5:
                val = minimax_ab(child, depth-1, alpha, beta, is_next_max)
            else:
                val = inv_minimax_ab(child, depth-1, alpha, beta, is_next_max)
    return val

def generate_list(difficulty):
    desires_DB = [[15,0], [8,2], [5,5], [2,8], [0,15]]
    desired_inv = desires_DB[difficulty-1][0]
    desired_minmax = desires_DB[difficulty-1][1]
    movelist = []
    amount_of_inv = 0
    amount_of_minmax = 0
    for i in range(15):
        if amount_of_inv < desired_inv:
            movelist.append(1)
            amount_of_inv += 1
        elif amount_of_minmax < desired_minmax:
            movelist.append(2)
            amount_of_minmax += 1
        else:
            movelist.append(0)
    random.shuffle(movelist)
    return list(movelist)
