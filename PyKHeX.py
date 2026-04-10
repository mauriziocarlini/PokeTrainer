# -*- coding: utf-8 -*-
import struct
import os
import signal
import sys

# Colori stats
HP = "\u001b[38;5;$196m"
ATK = "\u001b[38;5;$208m"
DEF = "\u001b[38;5;$220m"
SPA = "\u001b[38;5;$75m"
SPD = "\u001b[38;5;$118m"
SPE = "\u001b[38;5;$204m"

# Colori testi di dettaglio
TEXT = "\u001b[38;5;$245m"

# Colori natura
UP = "\u001b[38;5;$196m"
DOWN = "\u001b[38;5;$75m"

# Colori semantici
ERROR = "\033[0;31m"
WARNING = "\033[0;33m"
SUCCESS = "\033[0;32m"
INFO = "\u001b[38;5;$39m"

# Color reset
RESET = "\033[0m"

# Definisci i colori per ogni stat
stat_color = {'HP': HP, 'Atk': ATK, 'Def': DEF, 'Spe': SPE, 'SpA': SPA, 'SpD': SPD}

# Definizione funzione per gestire l'interruzione da tastiera (CTRL+C)
saluto = f"\n\n{SPE}Grazie per aver usato {DEF}PyKHeX{RESET}!\n"

def sigint_handler(signal_received, frame):
    print(saluto)
    sys.exit(0)

# Impostazione del gestore di interruzione da tastiera
signal.signal(signal.SIGINT, sigint_handler)

# Stampa il titolo
title = f"{SPE}╔═════════════════════════════════════╗\n"
title += f"║  {DEF}PyKHeX {SPA}v1.0.0{DEF} by Maurizio Carlini  {SPE}║\n"
title += f"╚═════════════════════════════════════╝{RESET}"
print(f"\n{title}\n")

filename = input(f"Digita nome file PK9 {TEXT}(es: pikachu): {RESET}")

# Controllo sul nome del file
while True:
    if filename.strip() == "":
        filename = input(f"{ERROR}Devi inserire un nome di file: {RESET}")
        continue
    if not filename.endswith('.pk9'):
        filename += '.pk9'
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"{ERROR}File non trovato.{RESET}\n")
        filename = input(f"Digita nome file PK9 {TEXT}(es: pikachu): {RESET}")
        continue
    break

# Converte i byte in una stringa leggibile
data_string = file_data.decode("ISO-8859-1")
data_string = ''.join(chr(b) for b in file_data if b != b'\x00').strip()  # rimuovi i byte 0x00


# Dizionario che associa ad ogni tipo il suo numero corrispondente
type_dict = {
    "Normal": 0,
    "Fighting": 1,
    "Flying": 2,
    "Poison": 3,
    "Ground": 4,
    "Rock": 5,
    "Bug": 6,
    "Ghost": 7,
    "Steel": 8,
    "Fire": 9,
    "Water": 10,
    "Grass": 11,
    "Electric": 12,
    "Psychic": 13,
    "Ice": 14,
    "Dragon": 15,
    "Dark": 16,
    "Fairy": 17,
    "Default": 19
}

# Dizionario che associa ad ogni natura il suo numero corrispondente
nat_dict = {
    f"Adamant ({UP}+Atk{RESET} / {DOWN}-SpA{RESET})": 3,
    f"Bold ({UP}+Def{RESET} / {DOWN}-Atk{RESET})": 5,
    f"Brave ({UP}+Atk{RESET} / {DOWN}-Spe{RESET})": 2,
    f"Calm ({UP}+SpD{RESET} / {DOWN}-Atk{RESET})": 20,
    f"Careful ({UP}+SpD{RESET} / {DOWN}-SpA{RESET})": 23,
    f"Gentle ({UP}+SpD{RESET} / {DOWN}-Def{RESET})": 21,
    f"Hasty ({UP}+Spe{RESET} / {DOWN}-Def{RESET})": 11,
    f"Impish ({UP}+Def{RESET} / {DOWN}-SpA{RESET})": 8,
    f"Jolly ({UP}+Spe{RESET} / {DOWN}-SpA{RESET})": 13,
    f"Lax ({UP}+Def{RESET} / {DOWN}-SpD{RESET})": 9,
    f"Lonely ({UP}+Atk{RESET} / {DOWN}-Def{RESET})": 1,
    f"Mild ({UP}+SpA{RESET} / {DOWN}-Def{RESET})": 16,
    f"Modest ({UP}+SpA{RESET} / {DOWN}-Atk{RESET})": 15,
    f"Naive ({UP}+Spe{RESET} / {DOWN}-SpD{RESET})": 14,
    f"Naughty ({UP}+Atk{RESET} / {DOWN}-SpD{RESET})": 4,
    f"Quiet ({UP}+SpA{RESET} / {DOWN}-Spe{RESET})": 17,
    f"Rash ({UP}+SpA{RESET} / {DOWN}-SpD{RESET})": 19,
    f"Relaxed ({UP}+Def{RESET} / {DOWN}-Spe{RESET})": 7,
    f"Sassy ({UP}+SpD{RESET} / {DOWN}-Spe{RESET})": 22,
    f"Serious ({TEXT}Neutrale{RESET})": 12,
    f"Timid ({UP}+Spe{RESET} / {DOWN}-Atk{RESET})": 10
}

# Dizionario che associa ad ogni tipo il suo colore corrispondente
type_colors = {
    "Normal": "\u001b[38;5;$248m",
    "Fighting": "\u001b[38;5;$166m",
    "Flying": "\u001b[38;5;$110m",
    "Poison": "\u001b[38;5;$163m",
    "Ground": "\u001b[38;5;$172m",
    "Rock": "\u001b[38;5;$138m",
    "Bug": "\u001b[38;5;$107m",
    "Ghost": "\u001b[38;5;$141m",
    "Steel": "\u001b[38;5;$103m",
    "Fire": "\u001b[38;5;$9m",
    "Water": "\u001b[38;5;$39m",
    "Grass": "\u001b[38;5;$47m",
    "Electric": "\u001b[38;5;$220m",
    "Psychic": "\u001b[38;5;$204m",
    "Ice": "\u001b[38;5;$122m",
    "Dragon": "\u001b[38;5;$69m",
    "Dark": "\u001b[38;5;$60m",
    "Fairy": "\u001b[38;5;$198m",
    "Default": "\u001b[38;5;$245m"
}

# Inverti il dizionario per accedere ai tipi tramite il numero
type_dict_inv = {v: k for k, v in type_dict.items()}

# Inverti il dizionario per accedere alle nature tramite il numero
nat_dict_inv = {v: k for k, v in nat_dict.items()}

# Interpreta tutti i dati del file
all_values = struct.unpack('<' + str(len(file_data)) + 'B', file_data)

teratipo = type_dict_inv[all_values[149]]
teratipo_color = type_colors.get(teratipo, "")

natura = nat_dict_inv[all_values[33]]

print(f'{TEXT}\nPokémon:{RESET}', data_string[88:110])
if all_values[10] == 70 and all_values[11] == 6:
    print(f'{TEXT}Strumento:{RESET}', "Ability Patch")
print(f'{TEXT}Natura:{RESET}', natura)
print(f'{TEXT}Tera:{RESET}', teratipo_color, teratipo, RESET, '\n')
print(f'{HP}HP :{RESET}', all_values[38])
print(f'{ATK}Atk:{RESET}', all_values[39])
print(f'{DEF}Def:{RESET}', all_values[40])
print(f'{SPE}Spe:{RESET}', all_values[41])
print(f'{SPA}SpA:{RESET}', all_values[42])
print(f'{SPD}SpD:{RESET}', all_values[43], '\n')

# Richiedi i nuovi valori all'utente
new_values = []
total = 0
remaining = 510
zero_flag = False  # Flag che indica se il residuo è 0

for i, stat in enumerate(['HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD']):
    if zero_flag:  # Se il residuo è 0, imposta il valore a 0 e continua
        new_value = 0
    else:  # Altrimenti, chiedi all'utente di inserire il valore
        while True:
            new_value_str = input(f"Inserisci il nuovo valore per {stat_color[stat]}{stat}: {RESET}")
            if new_value_str.strip() == "":
                print(f"{ERROR}Devi inserire un valore.{RESET}\n")
                continue
            try:
                new_value = int(new_value_str)
            except ValueError:
                print(f"{ERROR}Devi inserire un valore numerico.{RESET}\n")
                continue

            if new_value >= 0 and new_value <= 252:
                if total + new_value <= 510:
                    total += new_value
                    remaining -= new_value
                    break
                else:
                    print(f"{ERROR}Il totale dei valori inseriti supererebbe {RESET}510{ERROR}.{RESET}\n")
            else:
                print(f"{ERROR}Il valore deve essere compreso tra {RESET}0 {ERROR}e {RESET}252{ERROR}.{RESET}\n")

    new_values.append(new_value)
    if remaining > 0 and i < 5:  # Stampa il totale residuo solo se il residuo non è 0 e non sto impostando l'ultima statistica
        print(f"{INFO}Totale residuo: {RESET}", remaining, "\n")

    if remaining == 0:  # Se il residuo è 0, imposta il flag a True e imposta tutti i valori rimanenti a 0
        zero_flag = True
        for j in range(i+1, 6):
            new_values.append(0)
        if i < 5:  # Stampa il messaggio solo se non sto impostando l'ultima statistica
            print(f"{WARNING}Tutte le statistiche rimanenti sono state impostate a {RESET}0{WARNING}.{RESET}")
        break


# Codifica i nuovi valori nel formato originario
all_values_list = list(all_values)
for i, new_value in enumerate(new_values):
    all_values_list[38+i] = new_value


# Chiedi se modificare il teratipo
while True:
    choice = input(f"\n{WARNING}Vuoi cambiare il teratipo?{RESET} [S/N] ")
    if choice.upper() == "S":
        # Stampa la lista dei teratipi con i rispettivi colori
        print(f"\nScegli un teratipo:\n")
        for t in type_dict:
            color = type_colors.get(t, "white")
            print(f"\033[38;2;{color}\033m{type_dict[t]} - {t}\033[m")
        # Chiedi all'utente di inserire il teratipo
        while True:
            teratipo_str = input(f"\nInserisci il numero o il nome del teratipo: ")
            if teratipo_str.isdigit():
                teratipo = int(teratipo_str)
                if teratipo in type_dict.values():
                    all_values_list[149] = teratipo
                    print(f"{SUCCESS}Teratipo modificato.{RESET}")
                    break
                else:
                    print(f"{ERROR}Teratipo non valido.{RESET}")
            else:
                teratipo = type_dict.get(teratipo_str.title())
                if teratipo is not None:
                    all_values_list[149] = teratipo
                    print(f"{SUCCESS}Teratipo modificato.{RESET}")
                    break
                else:
                    print(f"{ERROR}Teratipo non valido.{RESET}")
        break
    elif choice.upper() == "N":
        print(f"{INFO}Teratipo non modificato.{RESET}")
        break
    else:
        print(f"{ERROR}Scelta non valida.{RESET}")


# Chiedi se modificare la natura
while True:
    choice = input(f"\n{WARNING}Vuoi cambiare la natura?{RESET} [S/N] ")
    if choice.upper() == "S":
        # Stampa la lista delle nature
        print(f"\nScegli la natura:\n")
        for t in nat_dict:
            print(f"{nat_dict[t]} - {t}")
        # Chiedi all'utente di inserire la natura
        while True:
            natura_str = input(f"\nInserisci il numero o il nome della natura: ")
            if natura_str.isdigit():
                natura = int(natura_str)
                if natura in nat_dict.values():
                    all_values_list[33] = natura
                    print(f"{SUCCESS}Natura modificata.{RESET}")
                    break
                else:
                    print(f"{ERROR}Natura non valida.{RESET}")
            else:
                natura = nat_dict.get(natura_str.title())
                if natura is not None:
                    all_values_list[33] = natura
                    print(f"{SUCCESS}Natura modificata.{RESET}")
                    break
                else:
                    print(f"{ERROR}Natura non valida.{RESET}")
        break
    elif choice.upper() == "N":
        print(f"{INFO}Natura non modificata.{RESET}")
        break
    else:
        print(f"{ERROR}Scelta non valida.{RESET}")


# Chiedi se assegnare Ability Patch, se non è già assegnata
if (all_values_list[10] != 70 and all_values_list[11] != 6) or (all_values_list[10] != 70 or all_values_list[11] != 6):
    while True:
        choice = input(f"\n{WARNING}Vuoi assegnare Ability Patch? {TEXT}(se il pokémon ha giò uno strumento, verrà sostituito) {RESET} [S/N] ")
        if choice.upper() == "S":
            all_values_list[10] = 70
            all_values_list[11] = 6
            print(f"{SUCCESS}Ability Patch assegnata.{RESET}")
            break
        elif choice.upper() == "N":
            print(f"{INFO}Ability Patch non assegnata.{RESET}")
            break
        else:
            print(f"{ERROR}Scelta non valida.{RESET}")


# Chiedi con che nome salvare il nuovo file
new_file_data = struct.pack('<' + str(len(file_data)) + 'B', *tuple(all_values_list))

new_filename = input(f"\nInserisci il nome del file di output {TEXT}(es: pikachu_trained): {RESET}")
while True:
    if new_filename.strip() == "":
        new_filename = input(f"{ERROR}Devi inserire un nome di file: {RESET}")
        continue
    if not new_filename.endswith('.pk9'):
        new_filename += '.pk9'
    break

with open(new_filename, 'wb') as f:
    f.write(new_file_data)

print(f"{SUCCESS}File salvato correttamente!{RESET}\n")
