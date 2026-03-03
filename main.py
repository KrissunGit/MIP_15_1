from game_logic import GameState, generate_sequence

def main():
    seq = generate_sequence(15, seed=1)
    state = GameState(seq)

    print("Sākums:", state.numbers, "Punkti:", state.get_points(), "Turn:", state.turn)

    # testam: vienkārši vienmēr izvēlas pirmo iespējamo gājienu
    while not state.is_empty():
        move = state.generate_moves()[0]
        state = state.apply_move(move)

    print("Beigas:", state.numbers, "Punkti:", state.get_points(), "Winner:", state.check_winner())

if __name__ == "__main__":
    main()