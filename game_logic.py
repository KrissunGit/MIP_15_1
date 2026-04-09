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
    return [GameElement(rng.randint(1, 4), 0) for _ in range(length)]

class GameState:
    def __init__(self, p1_points=0, p2_points=0, parent=None, turn=1, move_made=None, value=0, moves_in_turn=0, elements = None):
        self.p1_points = p1_points # 1. spēlētāja punkti
        self.p2_points = p2_points # 2. spēlētāja punkti
        self.turn = turn # kurš spēlētājs veic gājienu (1 vai 2)
        self.parent = parent # vecāka virsotne
        self.children = [] # pēcnācēju virsotnes
        self.move_made = move_made # veiktais gājiens
        self.value = value # datora vērtējums (izmantojam padoto vērtību)
        self.moves_in_turn = moves_in_turn # cik gājieni jau veikti šajā gājienā
        self.elements = list(elements) if elements is not None else []

    # ---------- PALĪGFUNKCIJAS ----------

    def is_empty(self) -> bool:
        """Pārbauda vai virkne ir tukša."""
        return len(self.elements) == 0

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
        for i, x in enumerate(self.elements):
            # TAKE drīkst tikai tad, ja kaimiņiem NAV aktīvs vairogs
            has_shield_neighbor = False
            if i > 0 and self.elements[i-1].shield_timer > 0:
                has_shield_neighbor = True
            if i < len(self.elements) - 1 and self.elements[i+1].shield_timer > 0:
                has_shield_neighbor = True
            
            if not has_shield_neighbor:
                moves.append(("TAKE", i))
                
            # 1. spēlētāja pirmā gājiena ierobežojums (nedrīkst SPLIT pirmajā gājienā)
            if self.parent is None:
                continue

            if x.value == 2:
                moves.append(("SPLIT2", i))
            elif x.value == 4:
                moves.append(("SPLIT4", i))

        if not moves and not self.is_empty():
            moves.append(("PASS",-1))

        return moves

    def apply_move(self, move: Move) -> "GameState":
        """
        Pielieto gājienu un atgriež JAUNU GameState (nemainot esošo).
        """
        if self.is_empty():
            raise ValueError("Nevar veikt gājienu: virkne ir tukša.")

        action, idx = move

        if action == "PASS":
            new_elements = [GameElement(e.value, max(0, e.shield_timer - 1)) for e in self.elements]
            return GameState(
                p1_points=self.p1_points,
                p2_points=self.p2_points,
                parent=self,
                turn=3 - self.turn,
                move_made=move,
                value=0,
                moves_in_turn=0,
                elements=new_elements
            )

        if not (0 <= idx < len(self.elements)):
            raise IndexError("Indekss ārpus virknes robežām.")

        new_elements = [GameElement(e.value,e.shield_timer) for e in self.elements]
        current_element = new_elements[idx]
        p1 = self.p1_points
        p2 = self.p2_points
        next_turn = self.turn
        next_moves_in_turn = self.moves_in_turn

        # --- TAKE ---
        if action == "TAKE":
            taken = new_elements.pop(idx)
            
            if self.turn == 1:
                p1 += taken.value
            else:
                p2 += taken.value

        # --- SPLIT 2 -> 1,1 (+0 punkti, Extra Move, Shield) ---
        elif action == "SPLIT2":
            if current_element.value != 2:
                raise ValueError("SPLIT2 drīkst tikai, ja izvēlētais skaitlis ir 2.")
            new_elements[idx:idx+1] = [GameElement(1, 2), GameElement(1, 2)]
            # Pievienojam 0 punktus (balansam)
            
            # Limitam: ja šis jau bija papildgājiens, tad mainām turn
            if self.moves_in_turn >= 1:
                next_turn = 3 - self.turn
                next_moves_in_turn = 0
            else:
                next_turn = self.turn
                next_moves_in_turn = self.moves_in_turn + 1

        # --- SPLIT 4 -> 2,2 (+1 punkts, papildgājiens, vairogs) ---
        elif action == "SPLIT4":
            if current_element.value != 4:
                raise ValueError("SPLIT4 drīkst tikai, ja izvēlētais skaitlis ir 4.")
            new_elements[idx:idx+1] = [GameElement(value=2,shield_timer=2), GameElement(value=2,shield_timer=2)]
            if self.turn == 1:
                p1 += 1
            else:
                p2 += 1
            
            # Limitam: ja šis jau bija papildgājiens, tad mainām turn
            if self.moves_in_turn >= 1:
                next_turn = 3 - self.turn
                next_moves_in_turn = 0
            else:
                next_turn = self.turn
                next_moves_in_turn = self.moves_in_turn + 1

        else:
            raise ValueError("Nezināma darbība. Atļauts: TAKE, SPLIT2, SPLIT4.")

        # Gājiena maiņa un taimeru apstrāde
        if action == "TAKE":
            next_turn = 3 - self.turn
            next_moves_in_turn = 0
        
        newly_created = []
        if action in ["SPLIT2", "SPLIT4"]:
            # Identificējam jaunizveidotos elementus, lai tiem nesamazinātu taimeri uzreiz
            newly_created = new_elements[idx : idx + 2]
            
        # Ja gājiens ir nomainījies -> samazinām visus taimerus
        if next_turn != self.turn:
            for e in new_elements:
                if e.shield_timer > 0 and e not in newly_created:
                    e.shield_timer -= 1

        temp_state_for_check = GameState(p1_points=p1, p2_points=p2, turn=next_turn, elements=new_elements)    

        if not temp_state_for_check.is_empty():
            all_possible = temp_state_for_check.generate_moves()
            has_any_take = any(m[0] == "TAKE" for m in all_possible)

            if not has_any_take:
                penalty = 2
                if next_turn == 1:
                    p1 -= penalty
                else: 
                    p2 -= penalty
                next_turn += 1

        return GameState(
            p1_points=p1,
            p2_points=p2,
            parent=self,
            turn=next_turn,
            move_made=move,
            value=0,
            moves_in_turn=next_moves_in_turn,
            elements=new_elements
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

class GameElement:
    def __init__(self,value,shield_timer):
        self.value = value
        self.shield_timer = shield_timer

    def __repr__(self):
        return f"[{self.value} S:{self.shield_timer}]"
