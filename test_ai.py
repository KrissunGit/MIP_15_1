from game_logic import GameState
from ai_solver import evaluate_position_simple as evaluate_position
import time

def test_ai_selection():
    # Testing Shielded neighbor
    # State: [1, 2(S), 4], AI's turn (P2). 
    # Index 1 is a shield. 
    # Neighbors (0 and 2) should be blocked for TAKE.
    state = GameState([1, 2, 4], p1_points=0, p2_points=0, turn=2, shield_timers=[0, 2, 0])
    print(f"--- Testing Shield (AI is P2) ---")
    print(f"State: {state.numbers}, Turn: {state.turn}, Shields: {state.shield_timers}")
    
    moves = state.generate_moves()
    print(f"Available moves: {moves}")
    
    # TAKE 0 and TAKE 2 should NOT be in moves
    for move in moves:
        if move[0] == "TAKE" and move[1] in (0, 2):
            print(f"FAILURE: Blocked move {move} is available!")
            
    res = evaluate_position(state, 4, "alphabeta")
    print(f"Final choice (Should be SPLIT or TAKE Shield): {res[0]}\n")

if __name__ == "__main__":
    test_ai_selection()
