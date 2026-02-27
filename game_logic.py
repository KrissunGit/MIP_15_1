class GameState:
    def __init__(self, numbers, p1_points=0, p2_points=0, parent=None, turn=1, move_made=None, value = 0):
            self.numbers = sorted(numbers) #skaitļu virkne
            self.p1_points = p1_points # 1. spēlētāja punkti
            self.p2_points = p2_points # 2. spēlētāja punkti
            self.turn = turn #kurš spēlētājs veic gājienu (1 vai 2)
            self.parent = parent #vecāka virsotne
            self.children = [] #pēcnācēju virsotnes
            self.move_made = move_made #veiktais gājiens
            self.value = 0 #datora vērtējums

    def generate_moves(self):
        pass

    def apply_move(self, move):
        pass

    def check_winner(self):
        pass