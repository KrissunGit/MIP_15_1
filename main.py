from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position, generate_list

def main():
    length = 15

    seq = generate_sequence(length, seed=1)
    state = GameState(seq)

    movelist = generate_list(5,length)

    all_times = []
    total_generated = 0
    total_evaluated = 0

    print("Sākums:", state.numbers, "Punkti:", state.get_points(), "Turn:", state.turn)

    move_index = 0

    while not state.is_empty():
        current_idx = min(move_index, len(movelist) - 1)
        result = evaluate_position(state, depth=4,movelist=movelist,move_index=current_idx)
        move = result["move"]
        if move:
            all_times.append(result["time"])
            total_generated += result["generated"]
            total_evaluated += result["evaluated"]
            state = state.apply_move(move)
            move_index+=1
            p1, p2 = state.get_points()
            print(f"Gājiens: {move[0]} index {move[1]}")
            print(f"Virkne: {state.numbers} | Punkti: P1:{p1}, P2:{p2}")
            print(f"--- Gājiena laiks: {result['time']:.4f}s | Virsotnes: {result['generated']}")
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

if __name__ == "__main__":
    main()

