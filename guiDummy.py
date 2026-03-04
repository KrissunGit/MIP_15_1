import tkinter as tk
from tkinter import messagebox
import random

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spēle: Skaitļu virkne Cilvēks vs Dators (GUI Prototype)")
        self.root.geometry("777x777")
        
        
        # --- DUMMY DATA (Viltus stāvoklis) ---
        # Mēs izmantojam šos mainīgos, lai testētu dizainu,
        # kamēr Engine komanda vēl nav gatava.
        
        self.numbers = [4, 2, 3, 1, 4, 2, 3, 1, 4, 2] # Testa virkne
        self.p1_score = 0  # Testa punkti
        self.p2_score = 0   # Testa punkti
        self.current_turn = "Human" # Kurš tagad iet?
        
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Iestatījumu panelis (Augšā)
        settings_frame = tk.LabelFrame(self.root, text="Pirms Spēles Iestatījumi")
        settings_frame.pack(fill="x", padx=10, pady=5)
  
        tk.Button(settings_frame, text="Sākt Jaunu Spēli",
                  command=self.start_game, bg="#dddddd").pack(pady=5)
  
        # 2. Informācijas panelis (Vidū)
        self.info_label = tk.Label(self.root, text="Gājiens: Cilvēks", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Cilvēks: 0 | Dators: 0", font=("Arial", 12, "bold"))
        self.score_label.pack(pady=5)

        # 3. Skaitļu pogas (Galvenais laukums)
        self.numbers_frame = tk.Frame(self.root)
        self.numbers_frame.pack(pady=10)
        
        # Uzzīmējam pogas pirmo reizi
        self.update_display()

        # 4. Logu logs (Apakšā)
        self.log_text = tk.Text(self.root, height=8, width=70, state="disabled", bg="#1e1e1e", fg="#00ff00")
        self.log_text.pack(pady=10, padx=10)

    
    def log(self, message):
        """Palīgfunkcija teksta ierakstīšanai logā"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_game(self):
        """Sāk jaunu spēli (Simulācija)"""
        self.log("-" * 30)
        self.log("Jauna spēle sākta!")
        
        # Atiestatām uz sākuma stāvokli (Dummy Data)
        self.numbers = [random.randint(1, 4) for _ in range(15)]
        self.p1_score = 0
        self.p2_score = 0
        self.current_turn = "Human"
        self.update_display()

    def update_display(self):
        """Pārzīmē visu ekrānu balstoties uz self.numbers"""
        
        # 1. Atjaunojam tekstu
        self.score_label.config(text=f"Cilvēks: {self.p1_score} | Dators: {self.p2_score}")
        self.info_label.config(text=f"Gājiens: {self.current_turn}")

        # 2. Notīrām vecās pogas
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        # 3. Zīmējam jaunas pogas katram skaitlim sarakstā
        for i, num in enumerate(self.numbers):
            btn_frame = tk.Frame(self.numbers_frame, borderwidth=1, relief="solid")
            btn_frame.pack(side="left", padx=2)

            # Skaitļa attēlošana
            lbl = tk.Label(btn_frame, text=str(num), font=("Arial", 12, "bold"), width=2)
            lbl.pack()

            # Poga "P" (Paņemt) - Strādā vienmēr
            tk.Button(btn_frame, text="P",
                      command=lambda idx=i: self.human_move('P', idx),
                      font=("Calibri", 10, "bold"), bg="#45a049", fg="white", 
                      activebackground="#45a049", relief = "flat",
                      cursor = "hand2").pack(fill="x", pady = 1)

            # Poga "S" (Sadalīt) - Tikai ja skaitlis ir 2 vai 4
            if num == 2 or num == 4:
                tk.Button(btn_frame, text="S",
                          command=lambda idx=i: self.human_move('S', idx),
                          font=("Arial", 8), bg="#ffccaa").pack(fill="x", pady = 1)

    def human_move(self, action, idx):
        """
        Šī funkcija tiek izsaukta, kad cilvēks nospiež pogu.
        Tā kā Engine vēl nav gatavs, mēs simulējam loģiku šeit.
        """
        val = self.numbers[idx]
        self.log(f"Cilvēks izvēlējās: {action} uz skaitli {val} (indekss {idx})")

        # --- DUMMY LOGIC (Vēlāk šo aizstās Engine izsaukums) ---
        if action == 'P':
            self.p1_score += val
            self.numbers.pop(idx) # Izdzēšam skaitli
        elif action == 'S':
            self.numbers.pop(idx)
            if val == 2:
                self.numbers.insert(idx, 1)
                self.numbers.insert(idx, 1)
            elif val == 4:
                self.numbers.insert(idx, 2)
                self.numbers.insert(idx, 2)
                self.p1_score += 1

        # Pārslēdzam gājienu uz datoru
        self.current_turn = "Computer"
        self.update_display()

        # Simulējam datora domāšanu (pēc 1 sekundes)
        self.root.after(1000, self.computer_move_dummy)
        
    def computer_move_dummy(self):
        """
        Viltus AI. Tas vienmēr paņem pirmo pieejamo skaitli.  
        Vēlāk šeit būs: move = ai.get_best_move_smth(...)  
        """
        if not self.numbers:
            messagebox.showinfo("Beigas", "Spēle beigusies!")
            return

        # Dators "domā"...
        self.log("Dators domā...")

        # Dators vienkārši paņem pirmo skaitli (Dummy Logic)
        val = self.numbers[0]
        self.numbers.pop(0)
        self.p2_score += val
        self.log(f"Dators paņēma {val}")

        self.current_turn = "Human"
        self.update_display()

# --- Palaišana ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()