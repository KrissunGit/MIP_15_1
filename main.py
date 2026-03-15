from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position, generate_list
def main():
    seq = generate_sequence(20, seed=None)
    state = GameState(seq)
    movelist = generate_list(2)
    print("Sākums:", state.numbers, "Punkti:", state.get_points(), "Turn:", state.turn)
    move_index = 0
    # testam: vienkārši vienmēr izvēlas pirmo iespējamo gājienu
    while not state.is_empty():
        move = evaluate_position(state, depth=3, movelist=movelist, move_index=move_index)
        print(move, state.numbers) #- testam, tiri intereses pec  lai redzetu ko musu MI dara :)
        state = state.apply_move(move)

        move_index += 1
        if move_index >= 15:
            move_index = 0

    print("Beigas:", state.numbers, "Punkti:", state.get_points(), "Winner:", state.check_winner())

if __name__ == "__main__":
    main()
