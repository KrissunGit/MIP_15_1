# Mākslīgā intelekta pamatu pirmais labaratorijas darbs
## Spēles izveide

Izveidotās funkcijas:

generate_row(length) - rekursīva funkcija ar kuru uzģenerēju skaitļu virkni noteiktā garumā

player_take_num(player, taken_index) - funkcija, kura dotajam spēlētājam pievieno to punktu vērtību, cik skaitlim ar norādīto indexu, un šo skaitli izņem no virknes

player_split_num(player, split_index) - fja, kurā nosaka vai dalītais skaitlis norādītā indexā ir 2 vai 4, tā vietā ievieto 1,1 vai 2,2, ja 4 tad pieskaita 1 punktu spēlētājam kurš veica gājienu

end_game() un end_game_check() - pašsaprotami, nosaka vai spēle beigusies, ja jā izvada kurš uzvarēja

 player_take_turn() - spēlētājam jāizvēlas gājiens, šis izveido vaicājumu ko vēlies darīt, apstrādā ievadi, ja TAKE vai SPLIT2, SPLIT4 tad šīs funkcijas izsauc

 Player_Decide_Which_Goddamn_Number_To_Take() - pašsaprotami :D Izveido vaicājumu tekstu "kurus var izvēlēties", spēlētājs izvēlas kuru skaitli ņemt, tad izsauc player_take_num funkciju ar šā skaitļa indexu

 get_possible_actions() - parastas pārbaudes, kuras darbības ir pieejamas. "Take" vienmēr ir, bet "SPLIT2" un "SPLIT4" jābūt tikai ja ir pieejama 2 vai 4 respektīvi

 ai_take_turn() - Šis būtu jāizvieto ar kārtīgu MI, bet pagaidām tas ir tikai random choice starp iespējamajām darbībām

 Vēl būtu jāapstrādā spēlļetāja ievades teksts, bet to uzreiz neizdarīju, tāpēc, piemēram, ja iespējams paņemt tikai 1, bet spēlētājs ieraksta 4, spēle izmet error.
 protams, jāizvieto arī random checki ar kaut ko kārtīgāku, arī gājienu uzskaite un spēles koks
 Kā arī, protams, grafiskā daļa.
