import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random

# --- REĀLIE IMPORTI (Engine + AI) ---
from game_logic import GameState, generate_sequence
from ai_solver import evaluate_position_simple as evaluate_position

# Cilvēks vienmēr ir spēlētājs 1, Dators ir spēlētājs 2
HUMAN = 1
COMPUTER = 2

class GameGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Skaitļu virknes spēle")
        
        # --- ADAPTĪVĀ MĒROGOŠANA (Responsive Scaling) ---
        screen_h = self.winfo_screenheight()
        if screen_h < 950:
            # Maziem ekrāniem (piem. Laptopiem)
            self.geometry("1100x700")
            self.canvas_h = 220
        else:
            # Lieliem monitoriem
            self.geometry("1300x850")
            self.canvas_h = 250

        self.resizable(False, False)

        # Spēles stāvoklis (GameState objekts)
        self.game_state = None

        # Iestatījumu mainīgie
        self.starter_var = tk.StringVar(value="Cilvēks")   # kurš sāk
        self.algo_var = tk.StringVar(value="alphabeta") # algoritms
        self.diff_var = tk.StringVar(value="Vidēji")    # grūtība

        # Inicializējam visus elementus
        self._build_widgets()

    def _build_widgets(self):
        # --- Augšējais panelis: iestatījumi ---
        top = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15, border_width=1, border_color="#333333")
        top.pack(fill="x", padx=10, pady=10, ipady=4)

        f1 = ctk.CTkFrame(top, fg_color="transparent")
        f1.pack(side="left", padx=8, pady=4)
        ctk.CTkLabel(f1, text="Kurš sāk?", font=("Monospace", 12, "bold"), text_color="#3b8ed0").pack(anchor="w", padx=15, pady=(10,5))
        ctk.CTkRadioButton(f1, text="Cilvēks 👤", variable=self.starter_var, value="Cilvēks", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f1, text="Dators 🤖", variable=self.starter_var, value="Computer", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=(2, 10))

        f2 = ctk.CTkFrame(top, fg_color="transparent")
        f2.pack(side="left", padx=8, pady=4)
        ctk.CTkLabel(f2, text="Algoritms", font=("Monospace", 12, "bold"), text_color="#3b8ed0").pack(anchor="w", padx=15, pady=(10,5))
        ctk.CTkRadioButton(f2, text="Minimax", variable=self.algo_var, value="minimax", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f2, text="Alpha-Beta", variable=self.algo_var, value="alphabeta", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=(2, 10))

        f3 = ctk.CTkFrame(top, fg_color="transparent")
        f3.pack(side="left", padx=8, pady=4)
        ctk.CTkLabel(f3, text="Grūtība", font=("Monospace", 12, "bold"), text_color="#3b8ed0").pack(anchor="w", padx=15, pady=(10,5))
        ctk.CTkRadioButton(f3, text="Viegli", variable=self.diff_var, value="Viegli", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f3, text="Vidēji", variable=self.diff_var, value="Vidēji", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkRadioButton(f3, text="Grūti", variable=self.diff_var, value="Grūti", font=("Monospace", 12)).pack(anchor="w", padx=15, pady=(2, 10))

        ctk.CTkButton(top, text="▶  Sākt jaunu spēli", command=self.start_game, font=("Monospace", 13, "bold"), cursor="hand2",
                  width=160, height=45, corner_radius=10).pack(side="right", padx=15, pady=4)

        # --- Vidējais panelis ---
        mid = ctk.CTkFrame(self, fg_color="transparent")
        mid.pack(fill="x", padx=10, pady=4)
        self.info_label  = ctk.CTkLabel(mid, text="Nospied 'Sākt jaunu spēli'", font=("Monospace", 13), text_color="#bbbbbb")
        self.info_label.pack(side="left", padx=(15, 0))
        self.score_label = ctk.CTkLabel(mid, text="Cilvēks: 0  |  Dators: 0", font=("Monospace", 13, "bold"), text_color="#bbbbbb")
        self.score_label.pack(side="right", padx=(15, 0))

        # --- Galvenais laukums ar Scrollbar ---
        self.container = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=15, border_width=1, border_color="#252525")
        self.container.pack(fill="x", padx=10, pady=5)

        self.canvas = tk.Canvas(self.container, bg="#0a0a0a", height=self.canvas_h, highlightthickness=0)
        self.canvas.pack(side="top", fill="x", expand=True, padx=10, pady=10)

        self.scrollbar = ctk.CTkScrollbar(self.container, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.numbers_frame = tk.Frame(self.canvas, bg="#0a0a0a")
        self.canvas.create_window((0, 0), window=self.numbers_frame, anchor="nw")

        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.numbers_frame.bind("<Configure>", _on_frame_configure)

        # --- Žurnāls ---
        log_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(log_frame, text="Spēles žurnāls", font=("Monospace", 12), text_color="#bbbbbb").pack(anchor="w", padx=15, pady=(8,4))
        self.log_text = ctk.CTkTextbox(log_frame, height=10, fg_color="#000000", text_color="#00dd00",
                                font=("Courier", 11), wrap="word", border_width=1, border_color="#333333")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def start_game(self):
        self.log_text.configure(state="normal")  
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        diff = self.diff_var.get()
        self.depth = 2 if diff == "Viegli" else (3 if diff == "Vidēji" else 4)

        # Nejaušs virknes garums 15-20
        seq_elements = generate_sequence(random.randint(15, 20)) 
        start_turn = HUMAN if self.starter_var.get() == "Cilvēks" else COMPUTER
        
        # Original state init: Komi +1 for P2
        self.game_state = GameState(elements=seq_elements, turn=start_turn, p2_points=1)

        self.log("=" * 60)
        self.log(f"Jauna spēle!")
        self.log(f"Virkne: {[e.value for e in self.game_state.elements]}")
        self.log(f"Sāk: {self.starter_var.get()} | Algoritms: {self.algo_var.get()} | Dziļums: {self.depth}")

        self._refresh()
        if self.game_state.turn == COMPUTER:
            self.after(800, self._computer_move)

    def _refresh(self):
        if self.game_state is None: return

        p1, p2 = self.game_state.get_points()
        self.score_label.configure(text=f"Cilvēks: {p1}  |  Dators: {p2}")

        turn_text = "Tavs gājiens ✋" if self.game_state.turn == HUMAN else "Dators domā...🤖"
        color = "#3b8ed0" if self.game_state.turn == HUMAN else "#e74c3c"
        self.info_label.configure(text=turn_text, text_color=color)

        # Get valid moves to handle blockers and splitting limits
        valid_moves = self.game_state.generate_moves()
        can_take = [False] * len(self.game_state.elements)
        can_split = [False] * len(self.game_state.elements)
        for act, idx in valid_moves:
            if act == "TAKE": can_take[idx] = True
            elif act.startswith("SPLIT"): can_split[idx] = True

        for w in self.numbers_frame.winfo_children(): w.destroy()

        for i, element in enumerate(self.game_state.elements):
            col_frame = tk.Frame(self.numbers_frame, bg="#0a0a0a")
            col_frame.pack(side="left", padx=5, pady=10)

            val = element.value
            timer = element.shield_timer
            blocked = not can_take[i]
            
            symbol = "🛡️" if timer > 0 else ("🔒" if blocked else " ")
            symbol_color = "#E0F7FA" if timer > 0 else "#e74c3c"

            # Cits fonts emogies, lai tās būtu precīzi nocentrēti
            ctk.CTkLabel(col_frame, text=symbol, font=("Segoe UI Emoji", 14), 
                         text_color=symbol_color, width=50, anchor="center").pack()

            num_color = "#3b8ed0" if timer > 0 else "#ffffff"
            ctk.CTkLabel(col_frame, text=str(val), font=("Monospace", 20, "bold"), width=50, height=50,
                         fg_color="#2b2b2b", text_color=num_color, corner_radius=10).pack(pady=4)

            is_human = (self.game_state.turn == HUMAN)
            
            # Poga "P" (Take) - zaļā krāsa
            p_can_press = (is_human and not blocked)
            p_state = "normal" if p_can_press else "disabled"
            p_color = "#2eb086" if p_can_press else "#253b34"
            p_text_color = "#ffffff" if p_can_press else "#666666"
            p_hover_color = "#1e7a5d"

            ctk.CTkButton(col_frame, text="P", width=50, height=35, corner_radius=8,
                          command=lambda idx=i: self._human_move("TAKE", idx),
                          fg_color=p_color, text_color=p_text_color, hover_color=p_hover_color, state=p_state).pack(pady=2)

            if val in (2, 4):
                # Poga "S" (Split) - oranža krāsa
                s_allowed = can_split[i]
                s_can_press = (is_human and s_allowed)
                s_state = "normal" if s_can_press else "disabled"
                s_color = "#f6995c" if s_can_press else "#4a3325"
                s_text_color = "#ffffff" if s_can_press else "#666666"
                s_hover_color = "#c47a4a"

                ctk.CTkButton(col_frame, text="S", width=50, height=35, corner_radius=8,
                              command=lambda idx=i, n=val: self._human_move("SPLIT2" if n==2 else "SPLIT4", idx),
                              fg_color=s_color, text_color=s_text_color, hover_color=s_hover_color, state=s_state).pack(pady=2)

    def _human_move(self, action, idx):
        if self.game_state is None or self.game_state.turn != HUMAN: return
        
        val = self.game_state.elements[idx].value
        self.log(f"Cilvēks: {action} → skaitlis {val} (indekss {idx})")
        
        self.game_state = self.game_state.apply_move((action, idx))
        
        p1, p2 = self.game_state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {[e.value for e in self.game_state.elements]}")
        
        self._refresh()
        self._check_game_over()
        
        # Triggerējam datora gājienu tikai tad, ja gājiens ir nomainījies
        if not self.game_state.is_empty() and self.game_state.turn == COMPUTER:
            self.after(800, self._computer_move)

    def _computer_move(self):
        if self.game_state is None or self.game_state.is_empty(): return
        if self.game_state.turn != COMPUTER: return

        self.log("Dators domā...")
        self._refresh()

        depth = self.depth
        algo  = self.algo_var.get()

        t_start = time.time()
        result = evaluate_position(self.game_state, depth, algo)
        elapsed = time.time() - t_start

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
        val = self.game_state.elements[idx].value if idx >= 0 else "PASS"
        self.log(f"Dators: {action} → {val}")

        self.game_state = self.game_state.apply_move(move)
        p1, p2 = self.game_state.get_points()
        self.log(f"  Punkti → Cilvēks: {p1}, Dators: {p2}")
        self.log(f"  Virkne: {[e.value for e in self.game_state.elements]}")

        self._refresh()
        self._check_game_over()

        # Ja ir papildgājiens (pēc SPLIT), izsaucam sevi rekurzīvi
        if not self.game_state.is_empty() and self.game_state.turn == COMPUTER:
            self.after(1200, self._computer_move)

    def _check_game_over(self):
        if not self.game_state.is_empty(): return
        winner = self.game_state.check_winner()
        p1, p2 = self.game_state.get_points()
        self.log("=" * 60)
        self.log(f"SPĒLE BEIGUSIES! Cilvēks: {p1} | Dators: {p2}")
        msg = "Tu uzvarēji!" if winner == HUMAN else ("Dators uzvarēja!" if winner == COMPUTER else "Neizšķirts!")
        self.log(f"Uzvarētājs: {'CILVĒKS' if winner==1 else ('DATORS' if winner==2 else 'Nav')}")
        messagebox.showinfo("Beigas", f"{msg}\n{p1} : {p2}")

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

if __name__ == "__main__":
    app = GameGUI()
    app.mainloop()
