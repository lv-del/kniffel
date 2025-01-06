# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:24:17 2024

@author: nguyn
"""

#Kniffel_Game
import random
import copy

class Kniffel_Game():
    def __init__(self, player_list):
        self.player_list = player_list

    def simulate_one_game(self):
        ''' This function simulates one game and returns a scoreboard '''
        scoreboard = self.initialize_scoreboard()

        # 12 mal Würfeln
        for turn in range(13):
            for player in self.player_list:
                number_of_dices_to_roll = 5
                kept_dices = []
                for roll in range(3):
                    dice_rolls = self.roll_dices(number_of_dices_to_roll)
                    if roll in [0, 1]:
                        additionally_kept_dices = player.decide_which_dices_to_hold(copy.deepcopy(scoreboard), copy.copy(kept_dices), copy.copy(dice_rolls), roll)
                        if self.player_makes_valid_dice_choice(additionally_kept_dices, dice_rolls):
                            kept_dices += additionally_kept_dices
                        number_of_dices_to_roll = 5 - len(kept_dices)
                    else:
                        kept_dices += dice_rolls
                chosen_field = player.decide_which_field_to_enter(copy.deepcopy(scoreboard), copy.copy(kept_dices))
                if self.player_makes_valid_field_choice(scoreboard, player, chosen_field):
                    scoreboard = self.update_scoreboard(scoreboard, player, chosen_field, kept_dices)
                else:
                    scoreboard = self.write_zero_in_a_random_field(scoreboard, player)
        return scoreboard
    
    def evaluate_score(self, scoreboard, player):
        ''' Evaluates the score of a particular player in the end of the game.
        Input:
        - scoreboard: The scoreboard
        Type: dict
        - player: The player, whichs score should be evalulated
        Type: player
        
        Output:
        score: The score of the player
        Type: int'''
        player_scoreboard = scoreboard[player.name]
        score = 0
        for field in ["Einser", "Zweier", "Dreier", "Vierer", "Fünfer", "Sechser"]:
            score += player_scoreboard[field]
        if score >= 63:
            score += 35
        for field in ["Dreierpasch", "Viererpasch", "Full House", "Kleine Straße", "Große Straße", "Kniffel", "Chance"]:
            score += player_scoreboard[field]
        return score

    def write_zero_in_a_random_field(self, scoreboard, player):
        ''' This function writes overrides a single None type value in the dict
        scoreboard[player.name]. Only None type values can be overridden
        
        Input:
        - scoreboard: Scoreboard for the game
        Type: dict
        - player: The player that gets a random scratch
        Type: player
        
        Output:
        - scoreboard: The updated scoreboeard
        Type: dict
        '''
        # Get the player's scoreboard (a dictionary of fields)
        player_scores = scoreboard.get(player.name)
        if player_scores is None:
            raise ValueError(f"Player {player.name} not found in the scoreboard.")
        
        # Find all fields that are still None
        available_fields = [field for field, value in player_scores.items() if value is None]
        
        if not available_fields:
            raise ValueError(f"No available fields to override for player {player.name}.")
        
        # Select a random field from the available fields
        random_field = random.choice(available_fields)
        
        # Set the chosen field to 0
        player_scores[random_field] = 0
        
        print(f"{player.name} scratched the field '{random_field}' with a value of 0.")
        
        # Update the scoreboard
        scoreboard[player.name] = player_scores
        return scoreboard

    def player_makes_valid_field_choice(self, scoreboard, player, chosen_field):
        ''' Checks whether the chosen_field is empty or exists at all
        Input:
        - scoreboard: Scoreboard
        Type: dict
        - player: The player that chose the field
        Type: player
        - chosen_field: The chosen field
        Type: str

        Output:
        Boolean: True if the field was valid and False if not
        '''
        try:
            if scoreboard[player.name][chosen_field] == None:
                return True
            else:
                return False
        except KeyError:
            return False

    def player_makes_valid_dice_choice(self, additionally_kept_dices, dice_rolls):
        ''' Check whether the choice about additionally kept dices is valid 
        Input:
        - additionally_kept_dices: Dice values, that additionally want to be kept
        Type: list
        - dice_rolls: The actual dice rolls that have been observed
        Type: list
        
        Output:
        - Boolean: True if the choice is valid and False if not
        '''
        freq2 = {}
        for item in dice_rolls:
            freq2[item] = freq2.get(item, 0) + 1

        for item in additionally_kept_dices:
            if freq2.get(item, 0) == 0:  # If item is not in list2 or exhausted
                return False
            freq2[item] -= 1  # Reduce the count in list2
        return True
    
    def roll_dices(self, number_of_dices_to_roll):
        ''' Rolls some dices!
        Input:
        - number_of_dices_to_roll: Number of dice-rolls to perform
        Type: int
        
        Output:
        - dice_rolls: Outcomes of the dice-rolls
        Type: list'''
        dice_rolls = [random.randint(1,6) for _ in range(number_of_dices_to_roll)]
        return dice_rolls

    def update_scoreboard(self, scoreboard, player, chosen_field, kept_dices):
        ''' This function updates and returns the scoreboard according to the player's choice
        Input:
        - scoreboard: The current scoreboard
        Type: dict
        - player: The player, whichs scoreboard should be updated
        Type: player
        - chosen_field: The field that should be updated
        Type: str
        - kept_dices: The dices that the player kept
        Type: list

        Output:
        - scoreboard: The updated scoreboard
        Type: dict
        '''  
        player_name = player.name

        match chosen_field:
            case "Einser":
                number_to_write = kept_dices.count(1) * 1
            case "Zweier":
                number_to_write = kept_dices.count(2) * 2
            case "Dreier":
                number_to_write = kept_dices.count(3) * 3
            case "Vierer":
                number_to_write = kept_dices.count(4) * 4
            case "Fünfer":
                number_to_write = kept_dices.count(5) * 5
            case "Sechser":
                number_to_write = kept_dices.count(6) * 6
            case "Dreierpasch":
                if max(kept_dices.count(dice) for dice in kept_dices) >= 3:
                    number_to_write = sum(kept_dices)
                else:
                    number_to_write = 0
            case "Viererpasch":
                if max(kept_dices.count(dice) for dice in kept_dices) >= 4:
                    number_to_write = sum(kept_dices)
                else:
                    number_to_write = 0
            case "Full House":
                unique_dice = set(kept_dices)
                if len(unique_dice) == 2 and any(kept_dices.count(dice) == 3 for dice in unique_dice):
                    number_to_write = 25
                else:
                    number_to_write = 0
            case "Kleine Straße":
                if any(all(x in kept_dices for x in seq) for seq in ([1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6])):
                    number_to_write = 30
                else:
                    number_to_write = 0
            case "Große Straße":
                if set([1, 2, 3, 4, 5]).issubset(kept_dices) or set([2, 3, 4, 5, 6]).issubset(kept_dices):
                    number_to_write = 40
                else:
                    number_to_write = 0
            case "Kniffel":
                if len(set(kept_dices)) == 1:
                    number_to_write = 50
                else:
                    number_to_write = 0
            case "Chance":
                number_to_write = sum(kept_dices)
            case _:
                raise ValueError(f"Invalid field: {chosen_field}")
        scoreboard[player_name][chosen_field] = number_to_write
        return scoreboard

    def initialize_scoreboard(self):
        ''' Initializes the scoreboard.
        Input:
        ...
        
        Output:
        scoreboard: The empty scoreboard
        Type: dict'''
        scoreboard = {player.name:{} for player in self.player_list}
        for player in self.player_list:
            scoreboard[player.name] = {
                                        "Einser": None,
                                        "Zweier": None,
                                        "Dreier": None,
                                        "Vierer": None,
                                        "Fünfer": None,
                                        "Sechser": None,
                                        "Dreierpasch": None,
                                        "Viererpasch": None,
                                        "Full House": None,
                                        "Kleine Straße": None,
                                        "Große Straße": None,
                                        "Kniffel": None,
                                        "Chance": None,
                                       }
        return scoreboard