import tkinter as tk
from tkinter import messagebox
import time

# --- REĀLIE IMPORTI (Engine + AI) ---
from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position_simple as evaluate_position

# Cilvēks vienmēr ir spēlētājs 1, Dators — spēlētājs 2
HUMAN = 1
COMPUTER = 2

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skaitļu virknes spēle — Cilvēks vs Dators")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Spēles stāvoklis (GameState objekts)
        self.state = None

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
        top = tk.Frame(self.root, bg="#e8e8e8", relief="groove", bd=1)
        top.pack(fill="x", padx=10, pady=6, ipady=4)

        # Bloks 1: Kurš sāk?
        f1 = tk.LabelFrame(top, text=" Kurš sāk? ", font=("Monospace", 9, "bold"),
                           bg="#e8e8e8", fg="#333", padx=20, pady=4)
        f1.pack(side="left", padx=8, pady=4)
        tk.Radiobutton(f1, text="Cilvēks 👤", variable=self.starter_var,
                       value="Human", bg="#e8e8e8",
                       font=("Monospace", 9)).pack(anchor="w")
        tk.Radiobutton(f1, text="Dators 🤖", variable=self.starter_var,
                       value="Computer", bg="#e8e8e8",
                       font=("Monospace", 9)).pack(anchor="w")

        # Bloks 2: Algoritms
        f2 = tk.LabelFrame(top, text=" Algoritms ", font=("Monospace", 9, "bold"),
                           bg="#e8e8e8", fg="#333", padx=20, pady=4)
        f2.pack(side="left", padx=8, pady=4)
        tk.Radiobutton(f2, text="Minimax", variable=self.algo_var,
                       value="minimax", bg="#e8e8e8",
                       font=("Monospace", 9)).pack(anchor="w")
        tk.Radiobutton(f2, text="Alpha-Beta", variable=self.algo_var,
                       value="alphabeta", bg="#e8e8e8",
                       font=("Monospace", 9)).pack(anchor="w")

        # Bloks 3: Dziļums
        f3 = tk.LabelFrame(top, text=" Dziļums ", font=("Monospace", 9, "bold"),
                           bg="#e8e8e8", fg="#333", padx=20, pady=4)
        f3.pack(side="left", padx=8, pady=4)
        tk.Spinbox(f3, from_=1, to=8, textvariable=self.depth_var,
                   width=4, font=("Monospace", 12, "bold"),
                   justify="center").pack(pady=4)

        # Poga "Sākt" - labajā pusē, liela un zaļa
        tk.Button(top, text="▶  Sākt jaunu spēli", command=self.start_game,
                  bg="#4CAF50", fg="white", font=("Monospace", 11, "bold"),
                  relief="flat", cursor="hand2",
                  width=16, height=2).pack(side="right", padx=12, pady=4)

        # --- Vidējais panelis: gājiena info + punkti ---
        mid = tk.Frame(self.root)
        mid.pack(fill="x", padx=10, pady=4)

        self.info_label  = tk.Label(mid, text="Nospied 'Sākt jaunu spēli'",
                                    font=("Monospace", 13), fg="#333")
        self.info_label.pack(side="left")

        self.score_label = tk.Label(mid, text="Cilvēks: 0  |  Dators: 0",
                                    font=("Monospace", 13, "bold"), fg="#222")
        self.score_label.pack(side="right")

        # --- Galvenais laukums: skaitļu pogas (ar scrollbar) ---
        container = tk.Frame(self.root, bg="#f0f0f0", relief="sunken", bd=2)
        container.pack(fill="x", padx=10, pady=6)

        self.canvas = tk.Canvas(container, bg="#f0f0f0", height=140, highlightthickness=0)
        self.canvas.pack(side="top", fill="x", expand=True)

        self.scrollbar = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.numbers_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.numbers_frame, anchor="nw")

        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.numbers_frame.bind("<Configure>", _on_frame_configure)

        # --- Apakšējais panelis: logs ---
        log_frame = tk.LabelFrame(self.root, text="Spēles žurnāls", font=("Monospace", 9))
        log_frame.pack(fill="both", expand=True, padx=10, pady=4)

        self.log_text = tk.Text(log_frame, height=10, state="disabled",
                                bg="#1e1e1e", fg="#00ff00",
                                font=("Courier", 9), wrap="word")
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)

    # =========================================================
    # 2. SPĒLES SĀKŠANA (atiestata datus, neveido jaunus widgetus)
    # =========================================================
    def start_game(self):
        self.log_text.config(state="normal")  
        self.log_text.delete("1.0", tk.END)   # terminal cleaner
        self.log_text.config(state="disabled")

        seq = generate_sequence(15)
        self.state = GameState(seq)

        # Ja dators sāk — viņš ir spēlētājs 1
        if self.starter_var.get() == "Computer":
            self.state = GameState(seq, turn=COMPUTER)

        self.log("=" * 40)
        self.log(f"Jauna spēle! Virkne: {self.state.numbers}")
        self.log(f"Sāk: {self.starter_var.get()} | Algoritms: {self.algo_var.get()} | Dziļums: {self.depth_var.get()}")

        self._refresh()

        # Ja dators sāk — uzreiz viņa gājiens
        if self.starter_var.get() == "Computer":
            self.root.after(800, self._computer_move)

    # =========================================================
    # 3. DISPLEJA ATJAUNOŠANA
    # =========================================================
    def _refresh(self):
        """Atjauno score, info un pogas pēc katra gājiena."""
        if self.state is None:
            return

        p1, p2 = self.state.get_points()
        self.score_label.config(text=f"Cilvēks: {p1}  |  Dators: {p2}")

        turn_text = "Tavs gājiens ✋" if self.state.turn == HUMAN else "Dators domā... 🤖"
        self.info_label.config(text=turn_text)

        # Iegūstam visus iespējamos gājienus, lai zinātu, kas ir bloķēts
        valid_moves = self.state.generate_moves()
        can_take = [False] * len(self.state.numbers)
        for act, idx in valid_moves:
            if act == "TAKE":
                can_take[idx] = True

        # Notīrām vecās pogas
        for w in self.numbers_frame.winfo_children():
            w.destroy()

        # Zīmējam jaunas pogas
        for i, num in enumerate(self.state.numbers):
            col_frame = tk.Frame(self.numbers_frame, bg="#f0f0f0")
            col_frame.pack(side="left", padx=3)

            # Skaitlis - krāsa mainās, ja tas ir Vairogs (Shield)
            timer = self.state.shield_timers[i]
            bg_color = "#ffffff"
            fg_color = "#000000"
            num_text = str(num)
            symbol_text = ""
            
            # Pārbaudām vai TAKE ir bloķēts
            blocked = not can_take[i]
            
            if timer > 0:
                bg_color = "#E0F7FA" # Cyan/Blue (Shield)
                fg_color = "#006064" 
                symbol_text = "🛡️"
            elif blocked:
                bg_color = "#ECEFF1" # Pelēks-zils (Blocked)
                fg_color = "#546E7A"
                symbol_text = "🔒"
            
            # Simbola labelis (virs skaitļa)
            tk.Label(col_frame, text=symbol_text if symbol_text else " ",
                     font=("Monospace", 10), bg="#f0f0f0", fg=fg_color).pack()

            # Skaitļa labelis
            tk.Label(col_frame, text=num_text,
                     font=("Monospace", 12, "bold"), width=3,
                     bg=bg_color, fg=fg_color, relief="ridge").pack(pady=1)

            # Poga Take — aktīva tikai ja nav bloķēts un ir cilvēka gājiens
            is_human = (self.state.turn == HUMAN)
            state_p = "normal" if (is_human and not blocked) else "disabled"
            
            tk.Button(col_frame, text="Take", width=5,
                      command=lambda idx=i: self._human_move("TAKE", idx),
                      bg="#4CAF50" if state_p=="normal" else "#C8E6C9", 
                      fg="white", font=("Monospace", 8, "bold"),
                      relief="flat", cursor="hand2" if state_p=="normal" else "arrow",
                      state=state_p).pack(pady=1)

            # Poga Split — tikai 2 vai 4
            if num in (2, 4):
                state_s = "normal" if is_human else "disabled"
                tk.Button(col_frame, text="Split", width=5,
                          command=lambda idx=i, n=num: self._human_move(
                              "SPLIT2" if n == 2 else "SPLIT4", idx),
                          bg="#FF9800" if state_s=="normal" else "#FFE0B2", 
                          fg="white", font=("Monospace", 8, "bold"),
                          relief="flat", cursor="hand2" if state_s=="normal" else "arrow",
                          state=state_s).pack(pady=1)

    # =========================================================
    # 4. CILVĒKA GĀJIENS
    # =========================================================
    def _human_move(self, action, idx):
        if self.state is None or self.state.turn != HUMAN:
            return

        val = self.state.numbers[idx]
        self.log(f"Cilvēks: {action} → skaitlis {val} (indekss {idx})")

        self.state = self.state.apply_move((action, idx))
        p1, p2 = self.state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {self.state.numbers}")

        self._refresh()
        self._check_game_over()

        # Ja gājiens joprojām ir cilvēkam (pēc SPLIT), neizsaucam datoru
        if not self.state.is_empty() and self.state.turn == COMPUTER:
            self.root.after(800, self._computer_move)

    # =========================================================
    # 5. DATORA GĀJIENS
    # =========================================================
    def _computer_move(self):
        if self.state is None or self.state.is_empty():
            return
        if self.state.turn != COMPUTER:
            return

        self.log("Dators domā...")
        self._refresh()  # Rāda "Dators domā..." uzrakstu

        depth = self.depth_var.get()
        algo  = self.algo_var.get()

        t_start = time.time()
        result = evaluate_position(self.state, depth, algo)
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
        val = self.state.numbers[idx]
        self.log(f"Dators: {action} → skaitlis {val} (indekss {idx})")

        self.state = self.state.apply_move(move)
        p1, p2 = self.state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {self.state.numbers}")

        self._refresh()
        self._check_game_over()

        # Ja gājiens joprojām ir datoram (pēc SPLIT), izsaucam sevi vēlreiz pēc pauzes
        if not self.state.is_empty() and self.state.turn == COMPUTER:
            self.root.after(1200, self._computer_move)

    # =========================================================
    # 6. SPĒLES BEIGAS
    # =========================================================
    def _check_game_over(self):
        if not self.state.is_empty():
            return

        winner = self.state.check_winner()
        p1, p2 = self.state.get_points()

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
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")


# --- Palaišana ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()