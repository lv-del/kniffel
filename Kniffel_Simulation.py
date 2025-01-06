# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:24:17 2024

@author: nguyn
"""

import sys
sys.path.append(r'C:\Users\nguyn\Documents\Python Kurs\Kniffel')  # Pfad anpassen, wenn nötig
import matplotlib.pyplot as plt  
import Kniffel_Game
import Kniffel_Player


if __name__ == '__main__':
    # Player 1
    player_1 = Kniffel_Player.Sam('Seb')
    # Player 2
    player_2 = Kniffel_Player.Bob('Tom')

    # Vorbereitung der Spielstatistiken
    wincounter = [0,0]
    player_1_total_score = 0
    player_2_total_score = 0
    total_rounds = 0
    
    # Spiel erstellen
    game = Kniffel_Game.Kniffel_Game([player_1, player_2])
    
    for game_iteration in range(100):
        
        scoreboard = game.simulate_one_game()
        
        # Punktzahlen der einzelnen Runden addieren
        player_1_score = sum(value for value in scoreboard[player_1.name].values() if value is not None)
        player_2_score = sum(value for value in scoreboard[player_2.name].values() if value is not None)
        player_1_total_score += player_1_score
        player_2_total_score += player_2_score      
        
        total_rounds+=1
        
        # Identifiziert den Sieger der Runde
        if game.evaluate_score(scoreboard, player_1) > game.evaluate_score(scoreboard, player_2):
            wincounter[0] += 1
        elif game.evaluate_score(scoreboard, player_1) < game.evaluate_score(scoreboard, player_2):
            wincounter[1] += 1
        else:
        
    # Anzahl der Siege und der durchschnittlichen Punktzahlen   
    if total_rounds > 0:
        player_1_average_score = player_1_total_score / total_rounds
        player_2_average_score = player_2_total_score / total_rounds
        
        print(f'{player_1.name} hat {wincounter[0]} Mal gewonnen und dabei durchschnittlich {player_1_average_score} Punkte pro Spiel erzielt!')
        print(f'{player_2.name} hat {wincounter[1]} Mal gewonnen und dabei durchschnittlich {player_2_average_score} Punkte pro Spiel erzielt!')
    else:
        print("No games were played.")
   
        
    # Visualisierung der Ergebnisse
    bot_names = [player_1.name, player_2.name]
        
    # Bestimme, wer gewonnen hat
    if wincounter[0] > wincounter[1]:
            colors = ['#e42d1f', 'gray']  # Player 1 (Sam) hat gewonnen
    elif wincounter[0] < wincounter[1]:
            colors = ['gray', '#e42d1f']  # Player 2 (Bob) hat gewonnen
    else:
            colors = ['gray', 'gray']  # Unentschieden
        
    # Balkendiagramm für die gewonnenen Spiele
    plt.bar(bot_names, wincounter, color=colors)
        
    # Titel und Achsenbeschriftungen hinzufügen
    plt.title("Und der Gewinner ist...")
    plt.xlabel("Bot")
    plt.ylabel("Anzahl der gewonnenen Spiele")
        
    # Diagramm anzeigen
    plt.show()
        
