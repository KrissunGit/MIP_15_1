from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position_simple as evaluate_position

import random as rnd


def main():
    length = rnd.randint(15,20)

    # 1. Ģenerējam secību un stāvokli
    seq = generate_sequence(length, seed=None)
    state = GameState(elements=seq)

    # Pieņemot, ka generate_list un movelist joprojām ir vajadzīgi tavam AI
    all_times = []
    total_generated = 0
    total_evaluated = 0

    print("Sākums:", [e.value for e in state.elements], "Punkti:", state.get_points(), "Turn:", state.turn)

    move_index = 0

    while not state.is_empty():        
        # Izsaucam AI
        move, nodes_gen, nodes_eval, elapsed = evaluate_position(state, 4, "alphabeta")
        
        if move:
            action, idx = move
            
            number_taken = state.elements[idx].value
            
            all_times.append(elapsed)
            total_generated += nodes_gen
            total_evaluated += nodes_eval
            
            # Veicam gājienu
            state = state.apply_move(move)
            move_index += 1
            
            p1, p2 = state.get_points()
            
            print(f"Gājiens: {action} {number_taken} at index {idx}")
            print(f"Virkne: {[e.value for e in state.elements]} | Punkti: P1:{p1}, P2:{p2}")
            print(f"--- Gājiena laiks: {elapsed:.4f}s | Virsotnes: {nodes_gen}")
        else:
            break

    avg_time = sum(all_times) / len(all_times) if all_times else 0

    print("\nSPĒLES REZULTĀTI:")
    print(f"Uzvarētājs: {state.check_winner()}")
    print(f"Punkti: {state.get_points()}")
    print(f"Vidējais laiks gājienam: {avg_time:.4f} s")
    print(f"Kopā ģenerētās virsotnes: {total_generated}")
    print(f"Kopā novērtētās virsotnes: {total_evaluated}\n")

    return state.check_winner()

def loop():
    winner = []
    winner_1 = 0
    winner_2 = 0
    draw = 0
    for i in range(100):
        winner.append(main())
    for j in winner:
        if j == 1:
            winner_1 += 1
        elif j == 2:
            winner_2 += 1
        else:
            draw += 1
    print(f"Player 1 won: {winner_1} times\nPlayer 2 won: {winner_2} times\nIt was a draw {draw} times")

if __name__ == "__main__":
    loop()