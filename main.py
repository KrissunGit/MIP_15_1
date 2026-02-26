import random  
  
# Rakstu visu vienkārši pēc kārtas, bez funkcijām
print("Ievadiet skaitļu virknes garumu (15-20): ")  
ievade = input()  
n = int(ievade) # Ja ievadīs burtu, tad izmetīs erroru (nemāku vēl try-except)
  
# Taisu sarakstu ar while ciklu un lieku klāt ar append
virkne = []  
i = 0  
while i < n:  
    virkne.append(random.randint(1, 4))  
    i = i + 1  
  
# Katram spēlētājam savs mainīgais punktiem (bez vārdnīcām)
punkti_1 = 0  
punkti_2 = 0  
pasreizeja_speletaja_nr = 1  
  
while len(virkne) > 0:  
    print("\n========================================")  
    print("Spēlētājs 1 punkti:", punkti_1)  
    print("Spēlētājs 2 punkti:", punkti_2)  
    print("----------------------------------------")  
    print("Pieejamā virkne:")  
      
    # Izprintēju sarakstu ar indeksiem, izmantojot parastu while ciklu
    j = 0  
    while j < len(virkne):  
        print("[" + str(j) + "]: " + str(virkne[j]), end="  ")  
        j = j + 1  
    print("\n========================================")  
      
    print("--> Spēlētāja", pasreizeja_speletaja_nr, "gājiens.")  
    print("Rakstiet 'P indekss' vai 'S indekss'")  
      
    gajiens = input("Jūsu izvēle: ")  
      
    # Sadalu ievadi. Pirmais burts ir darbība, cipars ir indekss. 
    # (Ja ieliks 2 atstarpes, tad programma nobruks)
    darbiba = gajiens[0]  
    indekss = int(gajiens[2:])   
      
    izveletais_skaitlis = virkne[indekss]  
      
    if darbiba == 'P':  
        # Pārbaudu, kurš spēlē, un pieskaitu viņam punktus
        if pasreizeja_speletaja_nr == 1:  
            punkti_1 = punkti_1 + izveletais_skaitlis  
        if pasreizeja_speletaja_nr == 2:  
            punkti_2 = punkti_2 + izveletais_skaitlis  
              
        virkne.pop(indekss)  
        print("Spēlētājs paņēma", izveletais_skaitlis)  
          
    if darbiba == 'S':  
        if izveletais_skaitlis == 2:  
            virkne.pop(indekss)  
            virkne.insert(indekss, 1)  
            virkne.insert(indekss, 1)  
            print("Skaitlis 2 tika sadalīts uz 1 un 1.")  
        if izveletais_skaitlis == 4:  
            virkne.pop(indekss)  
            virkne.insert(indekss, 2)  
            virkne.insert(indekss, 2)  
            if pasreizeja_speletaja_nr == 1:  
                punkti_1 = punkti_1 + 1  
            if pasreizeja_speletaja_nr == 2:  
                punkti_2 = punkti_2 + 1  
            print("Skaitlis 4 tika sadalīts uz 2 un 2.")  
  
    # Nomainu spēlētāju uz nākamo ar parastu if-else
    if pasreizeja_speletaja_nr == 1:  
        pasreizeja_speletaja_nr = 2  
    else:  
        pasreizeja_speletaja_nr = 1  
  
print("SPĒLE BEIGUSIES!")  
print("Spēlētājs 1:", punkti_1)  
print("Spēlētājs 2:", punkti_2)  
  
if punkti_1 > punkti_2:  
    print("Uzvar Spēlētājs 1!")  
if punkti_2 > punkti_1:  
    print("Uzvar Spēlētājs 2!")  
if punkti_1 == punkti_2:  
    print("Rezultāts ir neizšķirts!")
