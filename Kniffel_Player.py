# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:22:07 2024

@author: nguyn
"""
#Kniffel player


class Kniffel_Player():
    def __init__(self, name):
        "Name should be a string"
        self.name = name

    def decide_which_dices_to_hold(self, scoreboard, kept_dices, dice_rolls, roll):
        ''' The player's choice on what dices to keep.
        Input:
        - scoreboard: A copy of the scoreboard with information about the game. (see Kniffel_Game.py file)
        Type: dict
        - kept_dices: A copy of the dice values, that are already kept from previous rolls
        Type: list
        - dice_rolls: A copy of the dice values just rolled, that have to be decided on, whether to keep or not to keep.
        Type: list
        - roll: The number of the roll. Either 0 (first roll) or 1 (second roll). After the third roll the dices are automatically kept
        Type: int

        Output:
        A list of the dice values, that want to be kept. Can also be an empty list.
        Beware: The list needs to only include valid sublists of dice_rolls. Otherwise no dices will be kept.
        '''
        pass
    
    def decide_which_field_to_enter(self, scoreboard, dice_values):
        ''' The player's choice on the field, they want to enter the points in.
        Input:
        - scoreboard: A copy of the scoreboard with information about the game. (see Kniffel_Game.py file)
        Type: dict
        - dice_values: A copy of the dice values, that are in front of you.
        Type: list

        Output:
        One of the following strings:
        "Einser"
        "Zweier"
        "Dreier"
        "Vierer"
        "Fünfer"
        "Sechser"
        "Dreierpasch"
        "Viererpasch"
        "Full House"
        "Kleine Straße"
        "Große Straße"
        "Kniffel"
        "Chance"
        If the field is already taken, or the output is not one of the following strings, 
        a random field that is not yet taken will be occupied with the number 0.
        '''
        pass

# Hilfsklasse mit nützlichen Funktionen
class KniffelHilfe:
    def calculate_possible_scores(self, dice_values):
        ''' Berechnet mögliche Punktzahlen, die der Spieler erzielen kann. '''
        # Zählt, wie oft jede Zahl geworfen wurde
        counts = {dice: dice_values.count(dice) for dice in range(1, 7)}
        
        possible_scores = {
            "Einser": counts[1] * 1,
            "Zweier": counts[2] * 2, 
            "Dreier": counts[3] * 3, 
            "Vierer": counts[4] * 4, 
            "Fünfer": counts[5] * 5, 
            "Sechser": counts[6] * 6,  
            "Dreierpasch": sum(dice_values) if max(counts.values()) >= 3 else 0,
            "Viererpasch": sum(dice_values) if max(counts.values()) >= 4 else 0,
            "Full House": 25 if sorted(counts.values()) == [2, 3] else 0,
            "Kleine Straße": 30 if self.has_straight(dice_values, 4) else 0,   
            "Große Straße": 40 if self.has_straight(dice_values, 5) else 0,   
            "Kniffel": 50 if max(counts.values()) == 5 else 0,  
            "Chance": sum(dice_values), 
        }
        return possible_scores  # Gibt die möglichen Punktzahlen zurück

    def has_straight(self, dice_values, length):
        ''' Überprüft, ob es eine Straße gibt. Eine Straße sind aufeinanderfolgende Zahlen. '''
        dice_set = sorted(set(dice_values))  # Entfernt doppelte Zahlen und sortiert die Werte
        for start in range(1, 8 - length):
            # Überprüft, ob eine Straße von der aktuellen Zahl aus gebildet werden kann
            if list(range(start, start + length)) == dice_set[start - 1: start - 1 + length]:
                return True
        return False  # Wenn keine Straße gefunden wurde, gibt es keine

class Sam(Kniffel_Player):
    def decide_which_dices_to_hold(self, scoreboard, kept_dices, dice_rolls, roll):
        ''' Sam wählt Würfel basierend auf der Häufigkeit von Zahlen. '''
        if not dice_rolls:  # Falls keine Würfel geworfen wurden
            return []  # Keine Würfel zu behalten

        counts = {dice: dice_rolls.count(dice) for dice in dice_rolls}  # Zählt die Häufigkeit jeder Zahl
        if not counts:  # Falls die Zählung leer ist
            return []  # Keine Würfel zu behalten

        target = max(counts, key=counts.get)  # Wählt die Zahl, die am häufigsten vorkommt

        # Behalte alle Würfel dieser Zahl für ein Pasch oder ein Zahlenfeld
        return [dice for dice in dice_rolls if dice == target]

    def decide_which_field_to_enter(self, scoreboard, dice_values):
        ''' Sam wählt das Feld mit den höchsten Punkten, das noch nicht ausgefüllt ist. '''
        kniffel_hilfe = KniffelHilfe()  # Ein Objekt von KniffelHilfe erstellen
        possible_scores = kniffel_hilfe.calculate_possible_scores(dice_values)  # Berechnet die möglichen Punktzahlen

        # Sortiert die Felder nach der höchsten Punktzahl und wählt das erste freie Feld
        for field, score in sorted(possible_scores.items(), key=lambda x: -x[1]):
            if scoreboard[self.name].get(field) is None:  # Wenn das Feld noch nicht ausgefüllt ist
                return field

        # Wenn kein Feld mehr frei ist, wählt Sam "Chance"
        return "Chance"


class Bob(Kniffel_Player):
    def decide_which_dices_to_hold(self, scoreboard, kept_dices, dice_rolls, roll):
        ''' Bob wählt Würfel basierend auf Kniffel oder Full House. '''
        if not dice_rolls:  # Falls keine Würfel geworfen wurden
            return []  # Keine Würfel zu behalten

        counts = {dice: dice_rolls.count(dice) for dice in dice_rolls}  # Zählt die Häufigkeit der geworfenen Zahlen
        if not counts:  # Falls die Zählung leer ist
            return []  # Keine Würfel zu behalten

        target = max(counts, key=counts.get)  # Wählt die häufigste Zahl

        # Behalte Würfel, die zu Kniffel oder Full House führen
        return [dice for dice in dice_rolls if dice == target]

    def decide_which_field_to_enter(self, scoreboard, dice_values):
        ''' Bob wählt ebenfalls das Feld mit der höchsten Punktzahl. '''
        kniffel_hilfe = KniffelHilfe()  # Ein Objekt von KniffelHilfe erstellen
        possible_scores = kniffel_hilfe.calculate_possible_scores(dice_values)  # Berechnet die möglichen Punktzahlen

        # Sortiert die Felder nach der höchsten Punktzahl und wählt das erste freie Feld
        for field, score in sorted(possible_scores.items(), key=lambda x: -x[1]):
            if scoreboard[self.name].get(field) is None:  # Wenn das Feld noch nicht ausgefüllt ist
                return field

        # Wenn kein Feld mehr frei ist, wählt Bob "Chance"
        return "Chance"
