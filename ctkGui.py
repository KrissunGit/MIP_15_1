import tkinter as tk
import customtkinter
from tkinter import messagebox
import random

class GameGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        

        self.title("Spēle: Skaitļu virkne Cilvēks vs Dators (GUI Prototype)")
        self.geometry("777x777")
        
        # --- DUMMY DATA (Viltus stāvoklis) ---
        # Mēs izmantojam šos mainīgos, lai testētu dizainu,
        # kamēr Engine komanda vēl nav gatava.
        
        self.numbers = [4, 2, 3, 1, 4, 2, 3, 1, 4, 2] # Testa virkne
        self.p1_score = 0  # Testa punkti
        self.p2_score = 0   # Testa punkti
        self.current_turn = "Human" # Kurš tagad iet?

        self.game_options()
        
    def game_options(self):
        # 1. Iestatījumu panelis (Augšā)
        self.settings_frame = customtkinter.CTkFrame(self)
        self.settings_frame.pack(fill="both", padx=10, pady=5, expand=True)

        self.frame2 = customtkinter.CTkFrame(master=self.settings_frame, fg_color="transparent")
        self.frame2.pack(expand=True)

        settings_frame_label = customtkinter.CTkLabel(
            self.frame2,
            text="Pirms Spēles Iestatījumi",
            font=("Arial", 16, "bold")
        )
        settings_frame_label.pack(pady=(10,5))

        customtkinter.CTkButton(self.frame2, text="Sākt jaunu spēli",
                  command=self.setup_ui).pack(padx=20, pady=(20, 0))
        
        self.chooseAiButton = customtkinter.CTkButton(self.frame2, text="Algoritma izvēle",
                  command=self.choose_ai)
        self.chooseAiButton.pack(padx=20, pady=(20, 0))
        
        customtkinter.CTkButton(self.frame2, text="Exit", command=self.destroy).pack(padx=20, pady=(20, 0))

        self.radio_var = tk.IntVar(value=1)

    def radiobutton_event(self):
        if self.radio_var.get() == 1:
            algorithm = "AlphaBeta"
        else:
            algorithm = "Minimax"
        print("Chosen algorithm: ", algorithm)

    def choose_ai(self):
        self.chooseAiButton.forget()

        self.algorithm_options_frame = customtkinter.CTkFrame(self.frame2, fg_color="transparent")
        self.algorithm_options_frame.pack(pady=10)

        customtkinter.CTkLabel(self.algorithm_options_frame, text="Izvēlies algoritmu:", font=("Arial", 12)).pack()

        alphabeta = customtkinter.CTkRadioButton(
            self.algorithm_options_frame, text="AlphaBeta",
            variable=self.radio_var, value = 1,
            command = self.radiobutton_event
        )
        alphabeta.pack(pady=5)

        minimax = customtkinter.CTkRadioButton(
            self.algorithm_options_frame, text="Minimax",
            variable=self.radio_var, value=2,
            command=self.radiobutton_event
        )
        minimax.pack(pady=5)

        customtkinter.CTkButton(self.algorithm_options_frame, text="Confirm", )

    def setup_ui(self):
        self.settings_frame.destroy()
        # 2. Informācijas panelis (Vidū)
        self.info_label = customtkinter.CTkLabel(self, text="Gājiens: Cilvēks", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.score_label = customtkinter.CTkLabel(self, text="Cilvēks: 0 | Dators: 0", font=("Arial", 12, "bold"))
        self.score_label.pack(pady=5)

        # 3. Skaitļu pogas (Galvenais laukums)
        self.numbers_frame = customtkinter.CTkScrollableFrame(self, orientation="horizontal", height=150, label_text="Skaitļu virkne", width=450)
        self.numbers_frame.pack(pady=10)
        
        # Uzzīmējam pogas pirmo reizi
        self.update_display()

        # 4. Logu logs (Apakšā)
        self.log_text = customtkinter.CTkTextbox(self, height=200, width=600, state="disabled", fg_color="#1a1a1a", text_color="#00ff00", border_color="#444444", border_width=2,)
        self.log_text.pack(pady=20, padx=20, fill="both", expand=True)

        self.start_game()

    
    def log(self, message):
        """Palīgfunkcija teksta ierakstīšanai logā"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

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
        self.score_label.configure(text=f"Cilvēks: {self.p1_score} | Dators: {self.p2_score}")
        self.info_label.configure(text=f"Gājiens: {self.current_turn}")

        # 2. Notīrām vecās pogas
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        # 3. Zīmējam jaunas pogas katram skaitlim sarakstā
        for i, num in enumerate(self.numbers):
            btn_frame = customtkinter.CTkFrame(self.numbers_frame, border_width=2, border_color="white")
            btn_frame.pack(side="left", pady=5, padx=5)

            # Skaitļa attēlošana
            lbl = customtkinter.CTkLabel(btn_frame, text=str(num), font=("Arial", 12, "bold"), width=55, fg_color="transparent")
            lbl.pack(pady=(5,2))

            if num not in [2, 4]:
                bot_padding_y = 8
            else:
                bot_padding_y = 4

            # Poga "P" (Paņemt) - Strādā vienmēr
            customtkinter.CTkButton(btn_frame, text="P",
                      command=lambda idx=i: self.human_move('P', idx),
                      font=("Calibri", 10, "bold"), hover_color="#3d8f41",
                      width=55, height=28,
                      text_color="white", fg_color="#45a049",
                      cursor = "hand2").pack(fill="x", pady = (2, bot_padding_y), padx=5)

            # Poga "S" (Sadalīt) - Tikai ja skaitlis ir 2 vai 4
            if num == 2 or num == 4:
                customtkinter.CTkButton(btn_frame, text="S",
                          command=lambda idx=i: self.human_move('S', idx),
                          width=55, height=28,
                          font=("Arial", 8), fg_color="#ffccaa", hover_color="#e79b69" , text_color="black").pack(fill="x", pady = (2,8), padx=5)

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
        self.after(1000, self.computer_move_dummy)
        
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
    app = GameGUI()
    app.mainloop()