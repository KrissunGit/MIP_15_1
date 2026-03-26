from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position, generate_list

def main(depth):
    length = 20 

    seq = generate_sequence(length, seed=None)
    state = GameState(elements=seq, p2_points=1)

    difficulty = 4
    movelist = generate_list(difficulty, length)

    all_times = []
    total_generated = 0
    total_evaluated = 0

    move_index = 0

    while not state.is_empty():
        current_idx = min(move_index, len(movelist) - 1)
        result = evaluate_position(state, depth=depth, movelist=movelist, move_index=current_idx)
        
        move = result["move"]
        if move:
            all_times.append(result["time"])
            total_generated += result["generated"]
            total_evaluated += result.get("evaluated", 0)
            
            state = state.apply_move(move)
            move_index += 1
            
            p1, p2 = state.get_points()
        else:
            if not state.is_empty():
                state = state.apply_move(("PASS", 0))
                move_index += 1
                print("Dators izmanto PASS (iesprostots/trap)")
            else:
                break

    avg_time = sum(all_times) / len(all_times) if all_times else 0

    return state.check_winner(), avg_time, total_generated, total_evaluated

def loop():
    games_per_depth = 10  

    for depth in range(2, 6):  # 2, 3, 4, 5
        print(f"\nDziļums: {depth}")

        winner_1 = 0
        winner_2 = 0
        draw = 0
        average_time = 0
        average_generated = 0
        average_eval = 0

        for i in range(games_per_depth):
            w, t, g, e = main(depth)

            average_time += t
            average_generated += g
            average_eval += e

            if w == 1:
                winner_1 += 1
            elif w == 2:
                winner_2 += 1
            else:
                draw += 1

        print(f"AI 1 uzvarēja: {winner_1}")
        print(f"AI 2 uzvarēja: {winner_2}")
        print(f"Neišķirts: {draw}")
        print(f"Vidējais gājiena laiks: {average_time/games_per_depth:.4f}")
        print(f"Virsotnes izveidotas: {average_generated/games_per_depth:.0f}")
        print(f"Virsotnes pārskatītas: {average_eval/games_per_depth:.0f}")

if __name__ == "__main__":
    loop()
