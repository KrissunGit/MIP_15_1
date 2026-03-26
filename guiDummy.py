import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time

# --- REĀLIE IMPORTI (Engine + AI) ---
from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position_simple as evaluate_position

# Cilvēks vienmēr ir spēlētājs 1, Dators — spēlētājs 2
HUMAN = 1
COMPUTER = 2

class GameGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Skaitļu virknes spēle — Cilvēks vs Dators")
        self.geometry("860x620")
        self.resizable(False, False)

        # Spēles stāvoklis (GameState objekts)
        self.game_state = None

        # Iestatījumu mainīgie
        self.starter_var = tk.StringVar(value="Cilvēks")   # kurš sāk
        self.algo_var    = tk.StringVar(value="alphabeta") # algoritms
        self.diff_var = tk.StringVar(value="Vidēji") # grūtība

        # Uzbūvē visus widgetus VIENU REIZI
        self._build_widgets()

    # =========================================================
    # 1. WIDGETU IZVEIDE (tikai __init__ izsauc šo)
    # =========================================================
    def _build_widgets(self):
        # --- Augšējais panelis: iestatījumi (3 bloki + poga) ---
        top = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15, border_width=1, border_color="#333333")
        top.pack(fill="x", padx=10, pady=10, ipady=4)

        # Bloks 1: Kurš sāk?

        f1 = ctk.CTkFrame(top, fg_color="transparent")
        f1.pack(side="left", padx=8, pady=4, fill="y", ipady=5)

        f1_label = ctk.CTkLabel(f1, text="Kurš sāk?", font=("Monospace", 12, "bold"), text_color="#3b8ed0")
        f1_label.pack(anchor="w", padx=15, pady=(10,5))

        cilveks_rb = ctk.CTkRadioButton(f1, text="Cilvēks 👤", variable=self.starter_var,
                       value="Cilvēks",
                       font=("Monospace", 10))
        cilveks_rb.pack(anchor="w", padx = 15, pady=2)
        dators_rb = ctk.CTkRadioButton(f1, text="Dators 🤖", variable=self.starter_var,
                       value="Computer",
                       font=("Monospace", 10))
        dators_rb.pack(anchor="w", padx=15, pady=(2, 10))

        # Bloks 2: Algoritms
        f2 = ctk.CTkFrame(top, fg_color="transparent")
        f2.pack(side="left", padx=8, pady=4, fill="y", ipady=5)

        f2_label = ctk.CTkLabel(f2, text="Algoritms", font=("Monospace", 12, "bold"), text_color="#3b8ed0")
        f2_label.pack(anchor="w", padx=15, pady=(10,5))

        ctk.CTkRadioButton(f2, text="Minimax", variable=self.algo_var,
                       value="minimax",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f2, text="Alpha-Beta", variable=self.algo_var,
                       value="alphabeta",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=(2, 10))

        # Bloks 3: Grūtības izvēle(dziļuma izvēle)
        f3 = ctk.CTkFrame(top, fg_color="transparent")
        f3.pack(side="left", padx=8, pady=4, fill="y", ipady=5)

        f3_label = ctk.CTkLabel(f3, text="Grūtība", font=("Monospace", 12, "bold"), text_color="#3b8ed0")
        f3_label.pack(anchor="w", padx=15, pady=(10,5))

        ctk.CTkRadioButton(f3, text="Viegli", variable=self.diff_var,
                       value="Viegli",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f3, text="Vidēji", variable=self.diff_var,
                       value="Vidēji",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f3, text="Grūti", variable=self.diff_var,
                           value="Grūti",
                           font=("Monospace", 10)).pack(anchor="w", padx=15, pady=(2, 10))

        # Poga "Sākt" - labajā pusē, liela un zaļa
        ctk.CTkButton(top, text="▶  Sākt jaunu spēli", command=self.start_game, font=("Monospace", 13, "bold"), cursor="hand2",
                  width=160, height=45, corner_radius=10).pack(side="right", padx=15, pady=4)

        # --- Vidējais panelis: gājiena info + punkti ---
        mid = ctk.CTkFrame(self, fg_color="transparent")
        mid.pack(fill="x", padx=10, pady=4)

        self.info_label  = ctk.CTkLabel(mid, text="Nospied 'Sākt jaunu spēli'",
                                    font=("Monospace", 13), text_color="#bbbbbb")
        self.info_label.pack(side="left", padx=(15, 0))

        self.score_label = ctk.CTkLabel(mid, text="Cilvēks: 0  |  Dators: 0",
                                    font=("Monospace", 13, "bold"), text_color="#bbbbbb")
        self.score_label.pack(side="right", padx=(15, 0))

        # --- Galvenais laukums: skaitļu pogas ---
        self.numbers_frame = ctk.CTkFrame(self, fg_color="#0a0a0a",
                                      corner_radius=15, border_width=1, border_color="#252525")
        self.numbers_frame.pack(fill="x", padx=10, pady=5, ipady=15)

        # --- Apakšējais panelis: logs ---
        log_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        log_label = ctk.CTkLabel(log_frame, text="Spēles žurnāls", font=("Monospace", 11), text_color="#bbbbbb")
        log_label.pack(anchor="w", padx=15, pady=(8,4))

        self.log_text = ctk.CTkTextbox(log_frame, height=10, fg_color="#000000", text_color="#00dd00",
                                font=("Courier", 12), wrap="word", border_width=1, border_color="#333333")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0,10))

    # =========================================================
    # 2. SPĒLES SĀKŠANA (atiestata datus, neveido jaunus widgetus)
    # =========================================================
    def start_game(self):
        self.log_text.configure(state="normal")  
        self.log_text.delete("1.0", "end")   # terminal cleaner
        self.log_text.configure(state="disabled")

        diff = self.diff_var.get()

        if diff == "Viegli":
            self.depth = 2
        elif diff == "Vidēji":
            self.depth = 3
        else:
            self.depth = 4

        seq = generate_sequence(15)
        self.game_state = GameState(seq)

        # Ja dators sāk — viņš ir spēlētājs 1
        if self.starter_var.get() == "Computer":
            self.game_state = GameState(seq, turn=COMPUTER)

        self.log("=" * 40)
        self.log(f"Jauna spēle! Virkne: {self.game_state.numbers}")
        self.log(f"Sāk: {self.starter_var.get()} | Algoritms: {self.algo_var.get()} | Grūtība: {self.diff_var.get()} | Dziļums: {self.depth}")

        self._refresh()

        # Ja dators sāk — uzreiz viņa gājiens
        if self.starter_var.get() == "Computer":
            self.after(800, self._computer_move)

    # =========================================================
    # 3. DISPLEJA ATJAUNOŠANA
    # =========================================================
    def _refresh(self):
        """Atjauno score, info un pogas pēc katra gājiena."""
        if self.game_state is None:
            return

        p1, p2 = self.game_state.get_points()
        self.score_label.configure(text=f"Cilvēks: {p1}  |  Dators: {p2}")

        turn_text = "Tavs gājiens ✋" if self.game_state.turn == HUMAN else "Dators domā... 🤖"
        if self.game_state.turn == HUMAN:
            color = "#3b8ed0" 
        else:
            color = "#e74c3c"
        self.info_label.configure(text=turn_text, text_color=color)

        # Notīrām vecās pogas
        for w in self.numbers_frame.winfo_children():
            w.destroy()

        # Zīmējam jaunas pogas
        for i, num in enumerate(self.game_state.numbers):
            col_frame = ctk.CTkFrame(self.numbers_frame, fg_color="#1a1a1a", corner_radius=8)
            col_frame.pack(side="left", padx=4, pady=10)

            # Skaitlis
            ctk.CTkLabel(col_frame, text=str(num),
                     font=("Monospace", 18, "bold"), width=40, height=40,
                     fg_color="#2b2b2b", text_color="#ffffff", corner_radius=6).pack(pady=4, padx=4)

            # Poga P (Paņemt) — vienmēr aktīva cilvēka gājienā
            state_p = "normal" if self.game_state.turn == HUMAN else "disabled"
            
            ctk.CTkButton(col_frame, text="P", width=40, height=40,
                      command=lambda idx=i: self._human_move("TAKE", idx),
                      fg_color="#2eb086", hover_color="#1e7a5d",text_color="white", font=("Monospace", 10, "bold"), cursor="hand2",
                      state=state_p).pack(pady=2)

            # Poga S (Sadalīt) — tikai 2 vai 4
            if num in (2, 4):
                ctk.CTkButton(col_frame, text="S", width=40, height=40,
                          command=lambda idx=i, n=num: self._human_move(
                              "SPLIT2" if n == 2 else "SPLIT4", idx),
                          fg_color="#f6995c", hover_color="#c47a4a",text_color="white", font=("Monospace", 10, "bold"), cursor="hand2",
                          state=state_p).pack(pady=2)
            else:
                ctk.CTkLabel(col_frame, text="", width=40, height=40).pack(pady=2)
    # =========================================================
    # 4. CILVĒKA GĀJIENS
    # =========================================================
    def _human_move(self, action, idx):
        if self.game_state is None or self.game_state.turn != HUMAN:
            return

        val = self.game_state.numbers[idx]
        self.log(f"Cilvēks: {action} → skaitlis {val} (indekss {idx})")

        self.game_state = self.game_state.apply_move((action, idx))
        p1, p2 = self.game_state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {self.game_state.numbers}")

        self._refresh()
        self._check_game_over()

        if not self.game_state.is_empty():
            self.after(800, self._computer_move)

    # =========================================================
    # 5. DATORA GĀJIENS
    # =========================================================
    def _computer_move(self):
        if self.game_state is None or self.game_state.is_empty():
            return
        if self.game_state.turn != COMPUTER:
            return

        self.log("Dators domā...")
        self._refresh()  # Rāda "Dators domā..." uzrakstu

        algo  = self.algo_var.get()
        depth = self.depth

        t_start = time.time()
        result  = evaluate_position(self.game_state, depth, algo)
        elapsed = time.time() - t_start

        # evaluate_position atgriež (move, nodes_gen, nodes_eval, time)
        # vai tikai move — atkarībā no AI versijas
        if isinstance(result, tuple) and len(result) == 4:
            move, nodes_gen, nodes_eval, _ = result
            self.log(f"  Laiks: {elapsed:.3f}s | Uzģenerēti: {nodes_gen} | Novērtēti: {nodes_eval}")
        else:
            move = result
            self.log(f"  Laiks: {elapsed:.3f}s")

        if move is None:
            self.log("  Dators nevar veikt gājienu!")
            return

        action, idx = move
        val = self.game_state.numbers[idx]
        self.log(f"Dators: {action} → skaitlis {val} (indekss {idx})")

        self.game_state = self.game_state.apply_move(move)
        p1, p2 = self.game_state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {self.game_state.numbers}")

        self._refresh()
        self._check_game_over()

    # =========================================================
    # 6. SPĒLES BEIGAS
    # =========================================================
    def _check_game_over(self):
        if not self.game_state.is_empty():
            return

        winner = self.game_state.check_winner()
        p1, p2 = self.game_state.get_points()

        self.log("=" * 40)
        self.log(f"SPĒLE BEIGUSIES! Cilvēks: {p1} | Dators: {p2}")

        if winner == HUMAN:
            msg = f"🎉 Tu uzvarēji!\nCilvēks: {p1}  |  Dators: {p2}"
            self.log("Uzvarēja: CILVĒKS")
        elif winner == COMPUTER:
            msg = f"🤖 Dators uzvarēja!\nCilvēks: {p1}  |  Dators: {p2}"
            self.log("Uzvarēja: DATORS")
        else:
            msg = f"🤝 Neizšķirts!\nCilvēks: {p1}  |  Dators: {p2}"
            self.log("Rezultāts: NEIZŠĶIRTS")

        messagebox.showinfo("Spēles beigas", msg)

    # =========================================================
    # 7. LOGS
    # =========================================================
    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")


# --- Palaišana ---
if __name__ == "__main__":
    app = GameGUI()
    app.mainloop()