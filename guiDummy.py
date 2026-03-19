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
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        self.title("Skaitļu virknes spēle — Cilvēks vs Dators")
        self.geometry("860x620")
        self.resizable(False, False)

        # Spēles stāvoklis (GameState objekts)
        self.game_state = None

        # Iestatījumu mainīgie
        self.starter_var = tk.StringVar(value="Human")   # kurš sāk
        self.algo_var    = tk.StringVar(value="alphabeta") # algoritms
        self.depth_var   = tk.IntVar(value=4)             # dziļums

        # Uzbūvē visus widgetus VIENU REIZI
        self._build_widgets()

    # =========================================================
    # 1. WIDGETU IZVEIDE (tikai __init__ izsauc šo)
    # =========================================================
    def _build_widgets(self):
        # --- Augšējais panelis: iestatījumi (3 bloki + poga) ---
        top = ctk.CTkFrame(self, fg_color="#e8e8e8", corner_radius=10)
        top.pack(fill="x", padx=10, pady=6, ipady=4)

        # Bloks 1: Kurš sāk?
        
        f1 = ctk.CTkFrame(top, corner_radius=10)
        f1.pack(side="left", ipadx=20, fill="y", ipady=5)
        
        f1_label = ctk.CTkLabel(f1, text="Algoritms", font=("Monospace", 12, "bold"))
        f1_label.pack(anchor="w", padx=15, pady=(10,5))
        
        cilveks_rb = ctk.CTkRadioButton(f1, text="Cilvēks 👤", variable=self.starter_var,
                       value="Human",
                       font=("Monospace", 10))
        cilveks_rb.pack(anchor="w", padx = 15, pady=2)
        dators_rb = ctk.CTkRadioButton(f1, text="Dators 🤖", variable=self.starter_var,
                       value="Computer",
                       font=("Monospace", 10))
        dators_rb.pack(anchor="w", padx=15, pady=(2, 10))

        # Bloks 2: Algoritms
        f2 = ctk.CTkFrame(top, corner_radius=10)
        f2.pack(side="left", padx=8, pady=4, fill="y", ipady=5)

        f2_label = ctk.CTkLabel(f2, text="Kurš sāk?", font=("Monospace", 12, "bold"))
        f2_label.pack(anchor="w", padx=15, pady=(6,2))

        ctk.CTkRadioButton(f2, text="Minimax", variable=self.algo_var,
                       value="minimax",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f2, text="Alpha-Beta", variable=self.algo_var,
                       value="alphabeta",
                       font=("Monospace", 10)).pack(anchor="w", padx=15, pady=(2, 10))

        # Bloks 3: Dziļums
        f3 = ctk.CTkFrame(top, corner_radius=10)
        f3.pack(side="left", padx=8, pady=4, fill="y")

        f3_label = ctk.CTkLabel(f3, text="Dziļums?", font=("Monospace", 12, "bold"))
        f3_label.pack(anchor="w", padx=12, pady=(6,2))

        tk.Spinbox(f3, from_=1, to=8, textvariable=self.depth_var,
                   width=4, font=("Monospace", 12, "bold"),
                   justify="center").pack(pady=4)

        # Poga "Sākt" - labajā pusē, liela un zaļa
        ctk.CTkButton(top, text="▶  Sākt jaunu spēli", command=self.start_game, font=("Monospace", 14, "bold"), cursor="hand2",
                  width=16, height=40).pack(side="right", padx=12, pady=4)

        # --- Vidējais panelis: gājiena info + punkti ---
        mid = ctk.CTkFrame(self)
        mid.pack(fill="x", padx=10, pady=4)

        self.info_label  = ctk.CTkLabel(mid, text="Nospied 'Sākt jaunu spēli'",
                                    font=("Monospace", 13), text_color="#333")
        self.info_label.pack(side="left", padx=(15, 0))

        self.score_label = ctk.CTkLabel(mid, text="Cilvēks: 0  |  Dators: 0",
                                    font=("Monospace", 13, "bold"), text_color="#222")
        self.score_label.pack(side="right", padx=(0, 15))

        # --- Galvenais laukums: skaitļu pogas ---
        self.numbers_frame = ctk.CTkFrame(self, fg_color="#f0f0f0",
                                      corner_radius=10)
        self.numbers_frame.pack(fill="x", padx=10, pady=2, ipady=10)

        # --- Apakšējais panelis: logs ---
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=4)

        log_label = ctk.CTkLabel(log_frame, text="Spēles Žurnāls", font=("Monospace", 11, "bold"))
        log_label.pack(anchor="w", padx=12, pady=(8,4))

        self.log_text = ctk.CTkTextbox(log_frame, height=10, fg_color="#1e1e1e", text_color="#00ff00",
                                font=("Courier", 12), wrap="word")
        self.log_text.pack(fill="both", expand=True)

    # =========================================================
    # 2. SPĒLES SĀKŠANA (atiestata datus, neveido jaunus widgetus)
    # =========================================================
    def start_game(self):
        self.log_text.configure(state="normal")  
        self.log_text.delete("1.0", "end")   # terminal cleaner
        self.log_text.configure(state="disabled")
        
        seq = generate_sequence(15)
        self.game_state = GameState(seq)

        # Ja dators sāk — viņš ir spēlētājs 1
        if self.starter_var.get() == "Computer":
            self.game_state = GameState(seq, turn=COMPUTER)

        self.log("=" * 40)
        self.log(f"Jauna spēle! Virkne: {self.game_state.numbers}")
        self.log(f"Sāk: {self.starter_var.get()} | Algoritms: {self.algo_var.get()} | Dziļums: {self.depth_var.get()}")

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
        self.info_label.configure(text=turn_text)

        # Notīrām vecās pogas
        for w in self.numbers_frame.winfo_children():
            w.destroy()

        # Zīmējam jaunas pogas
        for i, num in enumerate(self.game_state.numbers):
            col_frame = ctk.CTkFrame(self.numbers_frame, fg_color="#f0f0f0")
            col_frame.pack(side="left", padx=3)

            # Skaitlis
            ctk.CTkLabel(col_frame, text=str(num),
                     font=("Monospace", 14, "bold"), width=2,
                     fg_color="#2b2b2b", text_color="white", corner_radius=6).pack(pady=2)

            # Poga P (Paņemt) — vienmēr aktīva cilvēka gājienā
            state_p = "normal" if self.game_state.turn == HUMAN else "disabled"
            ctk.CTkButton(col_frame, text="P", width=2,
                      command=lambda idx=i: self._human_move("TAKE", idx),
                      fg_color="#4CAF50", text_color="white", font=("Monospace", 9, "bold"), cursor="hand2",
                      state=state_p).pack(pady=1)

            # Poga S (Sadalīt) — tikai 2 vai 4
            if num in (2, 4):
                ctk.CTkButton(col_frame, text="S", width=2,
                          command=lambda idx=i, n=num: self._human_move(
                              "SPLIT2" if n == 2 else "SPLIT4", idx),
                          fg_color="#FF9800", text_color="white", font=("Monospace", 9, "bold"), cursor="hand2",
                          state=state_p).pack(pady=1)

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

        depth = self.depth_var.get()
        algo  = self.algo_var.get()

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
