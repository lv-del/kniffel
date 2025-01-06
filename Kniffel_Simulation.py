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
    player_1 = Kniffel_Player.Sam("Sam")
    # Player 2
    player_2 = Kniffel_Player.Bob("Bob")

    wincounter = [0,0]
    # Create Game
    game = Kniffel_Game.Kniffel_Game([player_1, player_2])
    for game_iteration in range(2000):
        scoreboard = game.simulate_one_game()
        
        # Bewertung der Punktzahlen
        player_1_score = sum(value for value in scoreboard[player_1.name].values() if value is not None)
        player_2_score = sum(value for value in scoreboard[player_2.name].values() if value is not None)
        
        print(f"Game {game_iteration + 1}:")
        print(f"{player_1.name} scored {player_1_score} points.")
        print(f"{player_2.name} scored {player_2_score} points.\n")
        
        if game.evaluate_score(scoreboard, player_1) > game.evaluate_score(scoreboard, player_2):
            wincounter[0] += 1
        elif game.evaluate_score(scoreboard, player_1) < game.evaluate_score(scoreboard, player_2):
            wincounter[1] += 1
        else:
            print('We have a tie')
    print(f'{player_1.name} won {wincounter[0]} times while {player_2.name} won {wincounter[1]} times!')
    
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
    plt.title("Gewonnene Spiele für jeden Bot")
    plt.xlabel("Bot")
    plt.ylabel("Anzahl der gewonnenen Spiele")
    
    # Diagramm anzeigen
    plt.show()
