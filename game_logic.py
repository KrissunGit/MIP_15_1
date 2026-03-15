import random

# Gājiens (Move) formāts: (action, index)
# action: "TAKE" | "SPLIT2" | "SPLIT4"
# index: indekss self.numbers sarakstā
Move = tuple[str, int]


def generate_sequence(length: int, seed: int | None = None) -> list[int]:
    """
    Uzģenerē sākuma virkni ar garumu 15..20 un vērtībām 1..4.
    """
    if not (15 <= length <= 20):
        raise ValueError("Virknes garumam jābūt diapazonā 15..20")

    rng = random.Random(seed)
    return [rng.randint(1, 4) for _ in range(length)]

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

    # ---------- PALĪGFUNKCIJAS (tās, ko tu prasīji) ----------

    def is_empty(self) -> bool:
        """Pārbauda vai virkne ir tukša."""
        return len(self.numbers) == 0

    def get_points(self) -> tuple[int, int]:
        """Atgriež (p1_points, p2_points)."""
        return self.p1_points, self.p2_points

    # ---------- SPĒLES LOĢIKA ----------

    def generate_moves(self) -> list[Move]:
        """
        Ģenerē visus gājienus pēc noteikumiem:
        - TAKE: var paņemt jebkuru skaitli no virknes (jebkurš indekss)
        - SPLIT2: ja izvēlētais skaitlis ir 2 -> aizvieto ar 1,1 (punkti +0)
        - SPLIT4: ja izvēlētais skaitlis ir 4 -> aizvieto ar 2,2 (punkti +1)
        """
        if self.is_empty():
            return []

        moves: list[Move] = []
        for i, x in enumerate(self.numbers):
            moves.append(("TAKE", i))
            if x == 2:
                moves.append(("SPLIT2", i))
            elif x == 4:
                moves.append(("SPLIT4", i))
        return moves

    def apply_move(self, move: Move) -> "GameState":
        """
        Pielieto gājienu un atgriež JAUNU GameState (nemainot esošo).
        """
        if self.is_empty():
            raise ValueError("Nevar veikt gājienu: virkne ir tukša.")

        action, idx = move
        if not (0 <= idx < len(self.numbers)):
            raise IndexError("Indekss ārpus virknes robežām.")

        new_numbers = list(self.numbers)
        current = new_numbers[idx]

        p1 = self.p1_points
        p2 = self.p2_points

        # --- TAKE ---
        if action == "TAKE":
            taken = new_numbers.pop(idx)
            if self.turn == 1:
                p1 += taken
                next_turn = 2
            else:
                p2 += taken
                next_turn = 1

        # --- SPLIT 2 -> 1,1 (0 punkti) ---
        elif action == "SPLIT2":
            if current != 2:
                raise ValueError("SPLIT2 drīkst tikai, ja izvēlētais skaitlis ir 2.")
            new_numbers[idx:idx+1] = [1, 1]
            next_turn = 2 if self.turn == 1 else 1

        # --- SPLIT 4 -> 2,2 (+1 punkts) ---
        elif action == "SPLIT4":
            if current != 4:
                raise ValueError("SPLIT4 drīkst tikai, ja izvēlētais skaitlis ir 4.")
            new_numbers[idx:idx+1] = [2, 2]
            if self.turn == 1:
                p1 += 1
                next_turn = 2
            else:
                p2 += 1
                next_turn = 1

        else:
            raise ValueError("Nezināma darbība. Atļauts: TAKE, SPLIT2, SPLIT4.")

        # saglabājam konsekventi sakārtotu virkni (jo __init__ tā dara)
        new_numbers = sorted(new_numbers)

        return GameState(
            numbers=new_numbers,
            p1_points=p1,
            p2_points=p2,
            parent=self,
            turn=next_turn,
            move_made=move,
            value=0
        )

    def check_winner(self) -> int | None:
        """
        Return:
        - 1 ja uzvar 1. spēlētājs
        - 2 ja uzvar 2. spēlētājs
        - 0 ja neizšķirts
        - None ja spēle vēl nav beigusies
        """
        if not self.is_empty():
            return None

        if self.p1_points > self.p2_points:
            return 1
        if self.p2_points > self.p1_points:
            return 2
        return 0
