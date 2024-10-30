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
            print(f"\n{player.symbol} {player.name}'s turn (Coins: {player.coins}\n)")
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
                self.player1.coins += 3
                print(f"{self.player1.name} earned 3 coins!")
            elif winner == 2:
                self.player2.coins += 3
                print(f"{self.player2.name} earned 3 coins!")

            # Perbarui deck masing-masing pemain
            self.player1.view_cards()
            self.player2.view_cards()

        print("\n=== Game Over ===")
        if self.player1.cards:
            print(f"{self.player1.name} wins the game!")
        elif self.player2.cards:
            print(f"{self.player2.name} wins the game!")


'''
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
    game = Game(player1, player2, rounds)
    game.start()

if __name__ == "__main__":
    main()

'''
class CardGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game")

        self.all_cards = load_cards_from_db()  # Assume this function loads card data
        self.rounds = 5  # Set example rounds or adjust as necessary
        self.game = None  # Will hold the Game instance

        # Main window widgets
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()
        
        tk.Label(self.main_frame, text="Enter Player 1 Name:").pack()
        self.player1_entry = tk.Entry(self.main_frame)
        self.player1_entry.pack()
        
        tk.Label(self.main_frame, text="Enter Player 2 Name:").pack()
        self.player2_entry = tk.Entry(self.main_frame)
        self.player2_entry.pack()
        
        self.start_button = tk.Button(self.main_frame, text="Start Game", command=self.initialize_game)
        self.start_button.pack()

    def initialize_game(self):
        # Collect player names
        player1_name = self.player1_entry.get()
        player2_name = self.player2_entry.get()
        
        if not player1_name or not player2_name:
            messagebox.showwarning("Warning", "Both players must enter their names!")
            return
        
        # Initialize players and assign cards
        player1 = Player(player1_name, self.all_cards)
        player2 = Player(player2_name, self.all_cards)

        # Give each player 2 starting cards
        player1.add_card(random.choice(self.all_cards))
        player1.add_card(random.choice(self.all_cards))
        player2.add_card(random.choice(self.all_cards))
        player2.add_card(random.choice(self.all_cards))

        # Initialize the Game instance and store it
        self.game = Game(player1, player2, self.rounds)
        
        # Display initial card stats in GUI
        self.display_initial_cards(player1, player2)
        
        # Start player turn screen
        self.main_frame.pack_forget()  # Hide the main screen
        self.player_turn_screen(player1)  # Start with player1's turn

    def display_initial_cards(self, player1, player2):
        print("\nInitial Cards:")
        player1.view_cards()
        player2.view_cards()

    def player_turn_screen(self, player):
        # Setup the player turn screen with options
        self.turn_frame = tk.Frame(self.root)
        self.turn_frame.pack()

        tk.Label(self.turn_frame, text=f"{player.name}'s Turn (Coins: {player.coins})").pack()
        
        tk.Button(self.turn_frame, text="View Cards", command=player.view_cards).pack()
        tk.Button(self.turn_frame, text="Buy Card", command=lambda: self.buy_card_screen(player)).pack()
        tk.Button(self.turn_frame, text="Merge Cards", command=lambda: self.merge_card_screen(player)).pack()
        tk.Button(self.turn_frame, text="Continue to Battle", command=self.battle_phase).pack()

    def buy_card_screen(self, player):
        # Window for buying cards
        self.turn_frame.pack_forget()
        self.buy_frame = tk.Frame(self.root)
        self.buy_frame.pack()
        
        tk.Label(self.buy_frame, text=f"{player.name}, select a card to buy").pack()

        for idx, card in enumerate(self.all_cards, 1):
            tk.Button(self.buy_frame, text=f"Buy {card.name} - {card.attack}/{card.defense}/{card.health}", 
                      command=lambda idx=idx: self.buy_card(player, idx)).pack()

        tk.Button(self.buy_frame, text="Cancel", command=self.cancel_action(player)).pack()

    def buy_card(self, player, card_idx):
        # Buy card logic using GUI instead of input
        selected_card = self.all_cards[card_idx - 1]
        if player.coins >= 0:  # Assume each card has a `price` attribute
            player.add_card(selected_card)
            player.coins -= 5
            messagebox.showinfo("Purchase", f"{player.name} bought {selected_card.name}!")
        else:
            messagebox.showwarning("Purchase", "Not enough coins!")
        self.cancel_action(player)

    def merge_card_screen(self, player):
        # Window for merging cards
        self.turn_frame.pack_forget()
        self.merge_frame = tk.Frame(self.root)
        self.merge_frame.pack()
        
        tk.Label(self.merge_frame, text=f"{player.name}, choose two cards to merge").pack()
        
        for idx, card in enumerate(player.cards, 1):
            tk.Button(self.merge_frame, text=f"{idx}. {card.name} - Level: {card.level}",
                      command=lambda idx=idx: self.select_merge_card(player, idx)).pack()

        self.merge_selection = []
        tk.Button(self.merge_frame, text="Cancel", command=self.cancel_action(player)).pack()

    def select_merge_card(self, player, card_idx):
        # Select cards for merging
        selected_card = player.cards[card_idx - 1]
        self.merge_selection.append(selected_card)
        
        if len(self.merge_selection) == 2:
            if player.merge_cards(self.merge_selection[0], self.merge_selection[1]):
                messagebox.showinfo("Merge", "Cards merged successfully!")
            else:
                messagebox.showwarning("Merge", "Merge unsuccessful.")
            self.merge_selection = []
            self.cancel_action(player)

    def battle_phase(self):
        # Set up battle phase
        self.turn_frame.pack_forget()
        self.battle_frame = tk.Frame(self.root)
        self.battle_frame.pack()
        
        card1 = self.game.player1.choose_card()  # Modify to Tkinter selection logic as needed
        card2 = self.game.player2.choose_card()

        winner = self.game.battle(card1, card2)
        
        if winner == 1:
            self.game.player1.coins += 3
            messagebox.showinfo("Battle", f"{self.game.player1.name} wins this round!")
        elif winner == 2:
            self.game.player2.coins += 3
            messagebox.showinfo("Battle", f"{self.game.player2.name} wins this round!")
        else:
            messagebox.showinfo("Battle", "It's a tie!")
        
        # Check for next round or end of game
        if not self.game.player1.cards or not self.game.player2.cards:
            self.game_over_screen()
        else:
            self.player_turn_screen(self.game.player1)

    def cancel_action(self, player):
        # Return to main turn frame
        self.merge_frame = tk.Frame(self.root)
        self.buy_frame.pack_forget()
        self.merge_frame.pack_forget()
        self.player_turn_screen(self.game.player1)  # Or whichever player’s turn it is

    def game_over_screen(self):
        self.turn_frame.pack_forget()
        self.battle_frame.pack_forget()
        self.game_over_frame = tk.Frame(self.root)
        self.game_over_frame.pack()
        
        winner_text = self.determine_winner()
        tk.Label(self.game_over_frame, text=winner_text).pack()
        tk.Button(self.game_over_frame, text="Exit", command=self.root.quit).pack()

    def determine_winner(self):
        if len(self.game.player1.cards) > len(self.game.player2.cards):
            return f"{self.game.player1.name} wins the game!"
        elif len(self.game.player2.cards) > len(self.game.player1.cards):
            return f"{self.game.player2.name} wins the game!"
        else:
            return "The game is a tie!"

root = tk.Tk()
game_gui = CardGameGUI(root)
root.mainloop()
