from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position

def main():
    seq = generate_sequence(15, seed=1)
    state = GameState(seq)

    print("Sākums:", state.numbers, "Punkti:", state.get_points(), "Turn:", state.turn)

    while not state.is_empty():
        move = evaluate_position(state, depth=4,difficulty=1)
        if move:
            state = state.apply_move(move)
            p1, p2 = state.get_points()
            print(f"Gājiens: {move[0]} index {move[1]}")
            print(f"Virkne: {state.numbers} | Punkti: P1:{p1}, P2:{p2}")
        else:
            break

    print("Beigas:", state.numbers, "Punkti:", state.get_points(), "Winner:", state.check_winner())
    return state.check_winner()

if __name__ == "__main__":
    main()

