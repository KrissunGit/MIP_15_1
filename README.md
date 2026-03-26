# Spēles Noteikumu un GUI Vadības Dokumentācija

Šajā versijā ir ieviesti vairāki stratēģiski mehānismi, lai padarītu spēli līdzsvarotāku un aizraujošāku.

---

## 1. Balanss: Komi +1
Lai kompensētu pirmā gājiena priekšrocību, **2. spēlētājs (Dators) sāk spēli ar +1 punktu**. 
AI simulācijas apstiprināja, ka šis ir optimālais punkts godīgai cīņai.

## 2. Papildu gājiens un ierobežojums
Kad spēlētājs veic **sadalīšanu ("SPLIT")**, viņš saņem **vienu papildu gājienu**. 
* Pēc šī papildu gājiena (neatkarīgi vai tas ir TAKE vai vēl viens SPLIT) gājiens obligāti pāriet otram spēlētājam. 
* Tas neļauj veikt bezgalīgas sadalīšanas vienā gājienā.

## 3. Pirmā gājiena ierobežojums
Pirmajā gājienā **1. spēlētājs (Cilvēks) nevar izmantot "SPLIT" (Sadalīšanu)**. Ir atļauta tikai skaitļa paņemšana ("TAKE").

## 4. Aizsardzības Vairogs (Shield)
Kad skaitlis tiek sadalīts (SPLIT), jaunizveidotie skaitļi saņem **vairogu uz 2 gājieniem**.
* Vairogs aizsargā **kaimiņu skaitļus**.
* Neviens spēlētājs nevar paņemt ("TAKE") skaitli, kam blakus atrodas vairogs.
* GUI tas tiek apzīmēts ar tekstu virs skaitļa, kas rada vairogu, un bloķēšanas simbolu virs kaimiņiem.

## 5. Slazda (Trap) sods
Ja spēlētājam gājiena sākumā nav **neviena derīga "TAKE" gājiena** (visi skaitļi ir bloķēti ar vairogiem), viņš saņem **-2 punktu sodu**.
Šādā situācijā spēlētājam ir jāizmanto "PASS" gājiens, lai pārietu pie nākamā turna un gaidītu vairogu izbeigšanos.

---

# Tehniskā Realizācija: AI un Algoritmi

Spēle izmanto vairākas Minimax variācijas, lai nodrošinātu dažādas grūtības pakāpes.

### Algoritmi (ai_solver.py)
* **Minimax ar Alpha-Beta atcirpšanu**: Optimizēts meklēšanas algoritms, kas neizskata zarus, kuri nevar ietekmēt gala lēmumu.
* **Inv-Minimax**: "Apgrieztais" algoritms, ko izmanto vieglākās grūtības pakāpēs, kur dators pieņem apzināti vājākus lēmumus.
* **Dinamiskā grūtība**: Funkcija `generate_list` izveido gājienu stratēģiju sarakstu visai spēlei, miksējot viedos (AB) un kļūdainos (Inv) gājienus atkarībā no izvēlētā līmeņa.

### Sistēmas Arhitektūra
* **game_logic.py**: Spēles dzinējs. Satur `GameState` klasi, kas ir imūtā (katrs gājiens rada jaunu stāvokli), atvieglojot AI meklēšanas koku.
* **gui.py**: Lietotāja saskarne, veidota ar `customtkinter`. Atbalsta adaptīvu mērogošanu un spēles žurnālu (log).
* **main.py**: Izmantojams AI efektivitātes testēšanai (simulē tūkstošiem spēļu bez GUI).

---

## GUI Vadība
* **Poga "P"**: Veikt "TAKE" darbību (Paņemt skaitli un pieskaitīt punktus).
* **Poga "S"**: Veikt "SPLIT" darbību (Sadala 2 -> 1,1 vai 4 -> 2,2 + 1 punkts). Parādās tikai skaitļiem 2 un 4.
* **Ritināšana**: Tā kā virkne var kļūt gara, ir pievienota horizontālā ritjosla (scroll) vai iespēja izmantot peles ritenīti.
* **Iestatījumi**: Pirms spēles sākšanas var izvēlēties, kurš sāk, algoritma tipu un meklēšanas dziļumu (Viegli, Vidēji vai Grūti).

# Uzstādīšana un palaišana
1. Pārliecinies, ka ir installēts Python 3.10+
2. Instalējat customtkinter ar **pip install customtkinter**
3. Palaidiet spēli ar **python gui.py**
