# Spēles Noteikumu un GUI Vadības Dokumentācija

Šajā versijā ir ieviesti vairāki stratēģiski mehānismi, lai padarītu spēli līdzsvarotāku un aizraujošāku.

## 1. Balanss: Komi +1 ⚖️
Lai kompensētu pirmā gājiena priekšrocību, **2. spēlētājs (Dators) sāk spēli ar +1 punktu**. 
AI simulācijas apstiprināja, ka šis ir optimālais punkts godīgai cīņai.

## 2. Papildu gājiens un ierobežojums 🔄
Kad spēlētājs veic **sadalīšanu ("SPLIT")**, viņš saņem **vienu papildu gājienu**. 
- Pēc šī papildu gājiena (neatkarīgi vai tas ir TAKE vai vēl viens SPLIT) turns obligāti pāriet otram spēlētājam. 
- Tas neļauj veikt bezgalīgas sadalīšanas vienā turnā.

## 3. Pirmā gājiena ierobežojums 🚫
Pirmajā gājienā **1. spēlētājs (Cilvēks) nevar izmantot "SPLIT" (Sadalīšanu)**. Ir atļauta tikai skaitļa paņemšana ("TAKE").

## 3. Aizsardzības Vairogs (Shield) 🛡️
Kad skaitlis tiek sadalīts (SPLIT), jaunizveidotie skaitļi saņem **vairogu uz 2 gājieniem**.
- Vairogs aizsargā **kaimiņu skaitļus**.
- Neviens spēlētājs nevar paņemt ("TAKE") skaitli, kam blakus atrodas vairogs.
- GUI tas tiek apzīmēts ar `🛡️` virs skaitļa, kas rada vairogu, un `🔒` virs bloķētajiem kaimiņiem.

## 4. Slazda (Trap) sods 🪤
Ja spēlētājam turna sākumā nav **neviena derīga "TAKE" gājiena** (visi skaitļi ir bloķēti ar vairogiem), viņš saņem **-2 punktu sodu**.
Šādā situācijā spēlētājam ir jāizmanto "PASS" gājiens, lai pārietu pie nākamā turna un gaidītu vairogu izbeigšanos.

## 5. GUI Vadība 🖥️
- **P (Paņemt)**: Paņem skaitli un pieskaita punktus.
- **S (Sadalīt)**: Sadala 2 -> (1,1) vai 4 -> (2,2 + 1 punkts).
- **Ritināšana**: Tā kā virkne var kļūt gara, ir pievienota horizontālā ritjosla (scroll).
