from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position

def main():
    seq = generate_sequence(15, seed=1)
    state = GameState(seq)

    print("Sākums:", state.numbers, "Punkti:", state.get_points(), "Turn:", state.turn)

    # testam: vienkārši vienmēr izvēlas pirmo iespējamo gājienu
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

def main1():
    loops = 10
    winners = []
    wins_1 = 0
    wins_2 = 0
    draw = 0
    while loops != 0:
        winners.append(main1())
        loops-=1
    for i in winners:
        if i == 1:
            wins_1 += 1
        elif i == 2:
            wins_2 += 1
        elif i == 0:
            draw += 1
        else:
            break
    print(f"P1 won: {wins_1} times\n P2 won: {wins_2} times\n It was a draw {draw} times") 

if __name__ == "__main__":
    main()

