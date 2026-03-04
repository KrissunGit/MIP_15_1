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
        new_numbers = list(self.numbers)
        new_p1 = self.p1_points
        new_p2 = self.p2_points
        move_type, value = move

        if move_type == 'take':
            new_numbers.remove(value)
            if self.turn == 1:
                new_p1 += value
            else:
                new_p2 += value
        elif move_type == 'split':
            if value == 2:
                new_numbers.remove(2)
                new_numbers.extend([1, 1])
            elif value == 4:
                new_numbers.remove(4)
                new_numbers.extend([2, 2])
                if self.turn == 1:
                    new_p1 += 1
                else:
                    new_p2 += 1
        
        child_node = GameState(
            numbers=new_numbers,
            p1_points=new_p1,
            p2_points=new_p2,
            turn=3 - self.turn, # 3-1 -> pirmais spēlētājs, 3-2 -> 2. spēlētājs
            parent=self,
            move_made=move
        )
        return child_node

    def check_winner(self):
        pass