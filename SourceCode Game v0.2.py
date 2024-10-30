import random
from abc import ABC, abstractmethod
from collections import Counter
import time
import tkinter as tk
from tkinter import messagebox, simpledialog


class Card(ABC):
    @abstractmethod
    def __init__(self, name, attack, defense, health, level):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.level = level
        self.set_base_stats(self.attack, self.defense, self.health)
        
    @abstractmethod
    def set_base_stats(self):
        pass
    
    @abstractmethod
    def special_ability(self):
        pass
    
    def upgrade(self):
        self.level += 1
        self.attack += self.attack_growth
        self.defense += self.defense_growth if self.defense <= 0.9 else 0
        self.health += self.health_growth
        print(f"{self.name} has been merged and upgraded to level {self.level}!")
        print(f"New stats - Attack: {self.attack}, Defense: {self.defense:.2f}, Health: {self.health}")

    def take_damage(self, damage):
        actual_damage = damage * (1 - self.defense)
        self.health -= actual_damage
        print(f"{self.name} received {actual_damage:.2f} damage, remaining health: {self.health:.2f}")
        
    def is_alive(self):
        return self.health > 0

    def calculate_power(self):
        return (self.attack * self.attack_multiplier + 
                self.defense * self.defense_multiplier) * self.level
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
    

class Warrior(Card):
    def __init__(self, name, attack, defense, health, level=1):
        super().__init__(name, attack, defense, health, level)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 6
        self.defense_growth = 0.05
        self.health_growth = 25
        self.attack_multiplier = 1.2
        self.defense_multiplier = 0.8
        
    def special_ability(self):
        return self.attack * (1 + (1 - self.health/90) * 0.5)

class Archer(Card):
    def __init__(self, name, attack, defense, health, level=1):
        super().__init__(name, attack, defense, health, level)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 8
        self.defense_growth = 0.03
        self.health_growth = 15
        self.attack_multiplier = 1.5
        self.defense_multiplier = 0.5
        
    def special_ability(self):
        return self.attack * 2 if random.random() < 0.3 else self.attack

class Guardian(Card):
    def __init__(self, name, attack, defense, health, level=1):
        super().__init__(name, attack, defense, health, level)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 4
        self.defense_growth = 0.07
        self.health_growth = 35
        self.attack_multiplier = 0.8
        self.defense_multiplier = 1.2
        
    def special_ability(self):
        return self.defense * 10

class Assassin(Card):
    def __init__(self, name, attack, defense, health, level=1):
        super().__init__(name, attack, defense, health, level)
        
    def set_base_stats(self, attack, defense, health):
        self.attack = attack
        self.defense = defense
        self.health = health
        self.attack_growth = 9
        self.defense_growth = 0.02
        self.health_growth = 12
        self.attack_multiplier = 1.7
        self.defense_multiplier = 0.3
        
    def special_ability(self):
        return self.attack * 3 if random.random() < 0.2 else self.attack

def load_cards_from_db():
    cards = []
    with open("db.txt", 'r') as file:
        for line in file:
            # Parse each line
            data = line.strip().split(',')
            card_type = data[0]
            name = data[1]
            attack = int(data[2])
            defense = float(data[3])
            health = int(data[4])
            
            
            # Based on the name, instantiate the correct class
            # Instantiate the correct class with parameters
            if card_type == "Warrior":
                card = Warrior(name, attack, defense, health)
            elif card_type == "Archer":
                card = Archer(name, attack, defense, health)
            elif card_type == "Guardian":
                card = Guardian(name, attack, defense, health)
            elif card_type == "Assassin":
                card = Assassin(name, attack, defense, health)
                continue
            
            # Set the card's base stats using a method that applies these values
            card.set_base_stats(attack, defense, health)
            cards.append(card)
            
    return cards

class Player:
    def __init__(self, name, available_cards):
        self.name = name
        self.cards = []  # Player’s own deck of cards
        self.coins = 10
        self.available_cards = available_cards  # List of cards loaded from db.txt

    def add_card(self, card):
        """Add a card to the player's deck."""
        self.cards.append(card)
        
    # Method untuk menampilkan kartu yang valid
    def view_cards(self):
        print(f"\n{self.name}'s Cards:")
        
        # Cek dan hapus kartu yang tidak valid (health <= 0)
        self.cards = [card for card in self.cards if card.health > 0]
        
        if not self.cards:
            print("No cards available.")
            return
        
        # Tampilkan kartu yang masih valid
        for i, card in enumerate(self.cards, 1):
            print(f"{i}. {card.name} (Level {card.level})")
            print(f"   Attack: {card.attack}, Defense: {card.defense:.2f}, Health: {card.health}")
        
        input("\nPress Enter to continue...")


    def merge_cards(self):
        if len(self.cards) < 2:
            print("Need at least 2 cards to merge!")
            return False
            
        while True:
            print(f"\n{self.name}, choose two cards to merge (or 0 to cancel):")
            for i, card in enumerate(self.cards, 1):
                print(f"{i}. {card.name} - Level: {card.level}")
            
            try:
                choice1 = int(input("Choose first card (0 to cancel): "))
                if choice1 == 0:
                    return False
                    
                choice2 = int(input("Choose second card (0 to cancel): "))
                if choice2 == 0:
                    return False
                
                choice1 -= 1
                choice2 -= 1
                
                if (0 <= choice1 < len(self.cards) and 
                    0 <= choice2 < len(self.cards) and
                    choice1 != choice2):
                    
                    card1, card2 = self.cards[choice1], self.cards[choice2]
                    
                    # Check if both cards are of the same class and level
                    if (card1.__class__ == card2.__class__ and 
                        card1.level == card2.level):
                        
                        # Upgrade the first card and remove the second one
                        card1.upgrade()
                        del self.cards[choice2]
                        print(f"Merged {card1.name} to level {card1.level}!")
                        return True
                    else:
                        print("Cards must be of the same type and level to merge.")
                else:
                    print("Invalid selection.")
                    return False
            except ValueError:
                print("Please enter valid numbers.")
                return False

    def buy_card(self):
        if self.coins <= 0:
            print("Not enough coins to buy a new card!")
            return False

        # Select 5 random cards, ensuring no card appears more than twice
        chosen_cards = []
        count = Counter()
        while len(chosen_cards) < 5:
            card = random.choice(self.available_cards)
            if count[card.name] < 2:  # Only allow each card up to 2 times
                chosen_cards.append(card)
                count[card.name] += 1

        # Display options to the player
        print("\nAvailable cards to buy:")
        for i, card in enumerate(chosen_cards, 1):
            print(f"{i}. {card.name} - Attack: {card.attack}, Defense: {card.defense:.2f}, Health: {card.health}")

        print("0. Cancel purchase")

        # Let player choose a card
        try:
            choice = int(input("Choose a card to buy (0-5): "))
            if choice == 0:
                return False
            elif 1 <= choice <= 5:
                selected_card = chosen_cards[choice - 1]
                self.cards.append(selected_card)
                self.coins -= 5
                print(f"{self.name} bought a new card: {selected_card.name}")
                return True
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Please enter a valid number.")
            return False

    def choose_card(self):
        while True:
            print(f"\n{self.name}, choose your action:")
            print("1. Choose card for battle")
            print("2. View all cards")
            
            try:
                action = input("Enter your choice (1-2): ")
                
                if action == "1":
                    print(f"\nChoose your card:")
                    for i, card in enumerate(self.cards, 1):
                        print(f"{i}. {card.name} - Level: {card.level}")
                        print(f"   Attack: {card.attack}, Defense: {card.defense:.2f}, Health: {card.health}")
                    
                    choice = int(input("Choose card number: ")) - 1
                    if 0 <= choice < len(self.cards):
                        return self.cards[choice]
                    else:
                        print("Invalid card number.")
                elif action == "2":
                    self.view_cards()
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

class Game:
    def __init__(self, player1, player2, rounds=3):
        self.player1 = player1
        self.player2 = player2
        self.rounds = rounds

    def battle(self, card1, card2):
        print(f"\nBattle: {self.player1.name}'s {card1.name} vs {self.player2.name}'s {card2.name}")
        
        while card1.is_alive() and card2.is_alive():
            # Card 1's turn
            attack_damage = card1.special_ability()
            card2.take_damage(attack_damage)
            if not card2.is_alive():
                print(f"{card2.name} has been defeated!")
                print(f"{self.player1.name} wins this round!")
                return 1

            # Card 2's turn
            attack_damage = card2.special_ability()
            card1.take_damage(attack_damage)
            if not card1.is_alive():
                print(f"{card1.name} has been defeated!")
                print(f"{self.player2.name} wins this round!")
                return 2

        return 0

    def player_turn(self, player, turn_time_limit=60):
        start_time = time.time()
        
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= turn_time_limit:
                print("\nTime's up! Moving to the next phase.\n")
                break
            
            print(f"{player.name}'s turn (Coins: {player.coins}) - Time remaining: {int(turn_time_limit - elapsed_time)} seconds\n")
            print("1. Decks \n")
            print("2. Market \n")
            print("3. Merge \n")
            print("4. Battle \n")
            
            action = input("Choose your action (1-4): ")
            
            if action == "1":
                player.view_cards()
            elif action == "2":
                if player.buy_card():
                    print("Card purchased successfully!")
            elif action == "3":
                if player.merge_cards():
                    print("Cards merged successfully!")
            elif action == "4":
                print("Proceeding to battle...")
                break
            else:
                print("Invalid choice. Please try again.")
            
            # Check remaining time after each action
            if time.time() - start_time >= turn_time_limit:
                print("\nTime's up! Moving to the next phase.\n")
                break
            

    def start(self):
        print("\n=== Game Start ===")

        while self.player1.cards and self.player2.cards:  # Loop hingga salah satu deck kosong
            # Player turns
            self.player_turn(self.player1)
            self.player_turn(self.player2)

            # Battle phase
            card1 = self.player1.choose_card()
            card2 = self.player2.choose_card()

            # Lakukan pertarungan
            winner = self.battle(card1, card2)
            if winner == 1:
                self.player1.coins += 10
                self.player2.coins += 3
                print(f"{self.player1.name} earned 10 coins!")
                print(f"{self.player2.name} earned 3 coins!")
            elif winner == 2:
                self.player2.coins += 10
                self.player1.coins += 3
                print(f"{self.player1.name} earned 3 coins!")
                print(f"{self.player2.name} earned 10 coins!")

            # Perbarui deck masing-masing pemain
            self.player1.view_cards()
            self.player2.view_cards()

        print("\n=== Game Over ===")
        if self.player1.cards:
            print(f"{self.player1.name} wins the game!")
        elif self.player2.cards:
            print(f"{self.player2.name} wins the game!")

def main():
    # Welcome message
    print("--- Welcome to Card Battle Game ---")
    print("Two players will battle using their cards and special abilities!\n")
    
    # Get player names
    player1_name = input("\nEnter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")
    
    # Load cards from the database and assign starting cards
    all_cards = load_cards_from_db()

    # Initialize players
    player1 = Player(player1_name, all_cards)
    player2 = Player(player2_name, all_cards)

    # give each player 2 card
    player1.add_card(random.choice(all_cards))  # Random starting card
    player1.add_card(random.choice(all_cards))  # Another random starting card
    
    player2.add_card(random.choice(all_cards))
    player2.add_card(random.choice(all_cards))
    
    # display each player card
    # Display initial card stats
    print("\nInitial Cards:")
    player1.view_cards()
    player2.view_cards()
    
    # Initialize game
    game = Game(player1, player2)
    game.start()

if __name__ == "__main__":
    main()
