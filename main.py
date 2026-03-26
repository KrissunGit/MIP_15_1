from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position, generate_list
import time

def main():
    length = 17 # Nedaudz garaka virkne strategijai

    seq = generate_sequence(length, seed=None)
    # Inicializējam stāvokli ar Komi (no spēles GO:)) +1 otrajam spēlētājam
    state = GameState(elements=seq, p2_points=1)

    # Iestatam grutibas limeni (5 = visgrutakais)
    difficulty = 4
    movelist = generate_list(difficulty, length)

    all_times = []
    total_generated = 0
    total_evaluated = 0

    print("Sākums (Komi +1 P2):", [e.value for e in state.elements], "Punkti:", state.get_points(), "Turn:", state.turn)

    move_index = 0

    while not state.is_empty():
        current_idx = min(move_index, len(movelist) - 1)
        result = evaluate_position(state, depth=4, movelist=movelist, move_index=current_idx)
        
        move = result["move"]
        if move:
            all_times.append(result["time"])
            total_generated += result["generated"]
            total_evaluated += result.get("evaluated", 0)
            
            state = state.apply_move(move)
            move_index += 1
            
            p1, p2 = state.get_points()
            print(f"Gājiens: {move[0]} index {move[1]}")
            print(f"Virkne: {[e.value for e in state.elements]} | Punkti: P1:{p1}, P2:{p2}")
            print(f"--- Gajiena laiks: {result['time']:.4f}s | Virsotnes: {result['generated']}")
        else:
            # Ja nav gājienu, bet spēle nav beigusies (Slazds/Trap), izmantojam PASS
            if not state.is_empty():
                state = state.apply_move(("PASS", 0))
                move_index += 1
                print("Dators izmanto PASS (iesprostots/trap)")
            else:
                break

    avg_time = sum(all_times) / len(all_times) if all_times else 0

    print("\nSPELES REZULTATI:")
    print(f"Uzvaretajs: {state.check_winner()}")
    print(f"Punkti: {state.get_points()}")
    print(f"Videjais laiks gajienam: {avg_time:.4f} s")
    print(f"Kopa generetas virsotnes: {total_generated}")
    print(f"Kopa novertetas virsotnes: {total_evaluated}\n")

    return state.check_winner()

if __name__ == "__main__":
    main()
