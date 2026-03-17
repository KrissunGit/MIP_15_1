import random
import time

nodes_generated = 0
nodes_evaluated = 0

def minimax_ab(state, depth, alpha, beta, is_maximizing):
    global nodes_generated, nodes_evaluated

    """
        Rekursīva funkcija, kas aprēķina labāko iespējamo vērtību dotajai pozīcijai.
        - alpha: Labākais rezultāts, ko maksimizētājs (spēlētājs viens) jau ir garantējis sev šajā zarā.
        - beta: Labākais (mazākais) rezultāts, ko minimizētājs (spēlētājs divi) jau ir garantējis sev šajā zarā.
    """
    
    if state.is_empty() or depth == 0:
        nodes_evaluated += 1
        return state.p1_points - state.p2_points

    if is_maximizing:
        max_eval = -float('inf')
        for move in state.generate_moves():
            nodes_generated += 1
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
            nodes_generated += 1
            child_state = state.apply_move(move)
            eval = minimax_ab(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval
    
def inv_minimax_ab(state, depth, alpha, beta, is_maximizing):   
    global nodes_generated, nodes_evaluated
    if state.is_empty() or depth == 0:
        nodes_evaluated += 1
        return state.p2_points - state.p1_points

    if is_maximizing:
        max_eval = -float('inf')
        for move in state.generate_moves():
            nodes_generated += 1
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
            nodes_generated += 1
            child_state = state.apply_move(move)
            eval = inv_minimax_ab(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval

def minimax(state, depth, is_maximizing):
    global nodes_generated, nodes_evaluated
    if state.is_empty() or depth == 0:
        nodes_evaluated += 1
        return state.p1_points - state.p2_points
    if is_maximizing:
        max_eval = -float('inf')
        for move in state.generate_moves():
            nodes_generated += 1
            child_state = state.apply_move(move)
            eval = minimax(child_state, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.generate_moves():
            nodes_generated += 1
            child_state = state.apply_move(move)
            eval = minimax(child_state, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval
    
def evaluate_position(state, depth, movelist, move_index):
    global nodes_generated, nodes_evaluated

    '''
        Atdod labāko kustību izmantojot minimax funkciju ar alpha-beta atcipršanas metodi 
    '''
    nodes_generated = 1
    nodes_evaluated = 0

    start_time = time.time()
    best_move = None
    
    if state.turn == 1:
        best_value = -float('inf')
    else:
        best_value = float('inf')

    alpha = -float('inf') # Alpha definešana, kā negatīva bezgalība
    beta = float('inf') # Beta definešana, kā pozitīva bezgalība)
    
    # Nākamo pāris kustību simulēšana izmantojot generate_moves un apply_move
    for move in state.generate_moves():
        nodes_generated += 1
        child = state.apply_move(move)
        is_next_max = (child.turn == 1)
        
        val = difficulty_changer(child,movelist,move_index,alpha,beta,is_next_max,depth)
            
        if state.turn == 1:
            if val > best_value:
                best_value = val
                best_move = move
        else:
            if val < best_value:
                best_value = val
                best_move = move

    end_time = time.time()
    elapsed_time = end_time - start_time
    return {
        "move": best_move,
        "time": elapsed_time,
        "generated": nodes_generated,
        "evaluated": nodes_evaluated
    }

def difficulty_changer(child, movelist, move_index,alpha,beta,is_next_max, depth):
    match movelist[move_index]:
        case 0:
            val = minimax_ab(child, depth - 1, alpha, beta, is_next_max)
        case 1:
            if random.random() < 0.5:
                val = minimax_ab(child, depth - 1, alpha, beta, is_next_max)
            else:
                val = inv_minimax_ab(child, depth - 1, alpha, beta, is_next_max)
        case 2:
            val = inv_minimax_ab(child, depth - 1, alpha, beta, is_next_max)
        case 3:
            val = minimax(child, depth -1, is_next_max)
        case _:
            val = minimax_ab(child, depth - 1, alpha, beta, is_next_max)
    return val

def generate_list(difficulty, total_length):
    desires_DB = [
        [0.0, 1.0, 0.0],
        [0.2, 0.6, 0.2],
        [0.4, 0.2, 0.4],
        [0.2, 0.1, 0.7],
        [0.0, 0.0, 1.0],
    ]
    
    ratios = desires_DB[difficulty-1]
    movelist = []

    count_inv = int(total_length * ratios[0])
    count_ab = int(total_length * ratios[1])
    count_pure = total_length - count_inv - count_ab
    
    movelist.extend([1] * count_inv)
    movelist.extend([0] * count_ab)
    movelist.extend([3] * count_pure)
    
    random.shuffle(movelist)
    return movelist
    
def evaluate_position_simple(state, depth, algorithm="alphabeta"):
    """
    FOR GUI - izsaucas bez difficulty sistēmas.
    Atgriež: (move, nodes_generated, nodes_evaluated, elapsed)
    """
    global nodes_generated, nodes_evaluated
    nodes_generated = 1
    nodes_evaluated = 0
    start_time = time.time()
    
    best_move = None
    best_value = -float('inf') if state.turn == 1 else float('inf')
    alpha, beta = -float('inf'), float('inf')

    for move in state.generate_moves():
        nodes_generated += 1
        child = state.apply_move(move)
        is_next_max = (child.turn == 1)

        if algorithm == "alphabeta":
            val = minimax_ab(child, depth - 1, alpha, beta, is_next_max)
        else:
            val = minimax(child, depth - 1, is_next_max)

        if state.turn == 1:
            if val > best_value:
                best_value = val
                best_move = move
        else:
            if val < best_value:
                best_value = val
                best_move = move
                
    elapsed = time.time() - start_time
    return best_move, nodes_generated, nodes_evaluated, elapsed
