import random


class Card:
    """
    Represents a single playing card with a suit and a rank.
    """

    def __init__(self, suit, rank):
        """
        Initialize the card with a suit and rank.
        """
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """
        Return a string representation of the card.
        """
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    """
    Represents a deck of 52 playing cards.
    """

    def __init__(self):
        """
        Initialize the deck with 52 cards.
        """
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "Ace", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "Jack", "value": 10},
            {"rank": "Queen", "value": 10},
            {"rank": "King", "value": 10}
        ]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        """
        Shuffle the deck of cards.
        """
        random.shuffle(self.cards)

    def deal(self, number):
        """
        Deal a number of cards from the deck.
        """
        return [self.cards.pop() for _ in range(number)]


class Hand:
    """
    Represents a hand of cards held by a player or dealer.
    """

    def __init__(self, dealer=False):
        """
        Initialize the hand, optionally as a dealer's hand.
        """
        self.cards = []
        self.dealer = dealer

    def add_card(self, card_list):
        """
        Add a list of cards to the hand.
        """
        self.cards.extend(card_list)

    def get_value(self):
        """
        Calculate and get the total value of the hand, accounting for aces.
        """
        value = sum(card.rank["value"] for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank["rank"] == "Ace")

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

    def is_blackjack(self):
        """
        Check if the hand is a blackjack (total value of 21 with two cards).
        """
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        """
        Display the cards in the hand, hiding the dealer's first card if applicable.
        """
        print(f"{'Dealer' if self.dealer else 'Your'} hand:")
        if self.dealer and not show_all_dealer_cards:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            if not self.dealer:
                print("Value:", self.get_value())
        print()


class Game:
    """
    Represents a game of Blackjack.
    """

    def play(self):
        """
        Play the specified number of games of Blackjack.
        """
        while True:
            games_to_play = self.get_number_of_games()

            for game_number in range(1, games_to_play + 1):
                deck = Deck()
                deck.shuffle()

                player_hand = Hand()
                dealer_hand = Hand(dealer=True)

                player_hand.add_card(deck.deal(2))
                dealer_hand.add_card(deck.deal(2))

                print(f"\n{'*' * 30}\nGame {game_number} of {games_to_play}\n{'*' * 30}")
                player_hand.display()
                dealer_hand.display()

                if self.check_winner(player_hand, dealer_hand):
                    continue

                self.player_turn(player_hand, deck)
                if self.check_winner(player_hand, dealer_hand):
                    continue

                self.dealer_turn(dealer_hand, deck)
                self.show_final_results(player_hand, dealer_hand)

            if not self.ask_to_play_again():
                print("Thanks for playing! Goodbye.")
                break

    @staticmethod
    def get_number_of_games():
        """
        Get the number of games to play from the user.

        Static Method: This method does not depend on any specific instance of the Game class.
        It is used to encapsulate functionality related to getting input from the user.
        """
        while True:
            try:
                games_to_play = int(input("How many games do you want to play? "))
                if games_to_play > 0:
                    return games_to_play
                else:
                    print("You must enter a positive number.")
            except ValueError:
                print("You must enter a number.")

    @staticmethod
    def player_turn(player_hand, deck):
        """
        Handle the player's turn.

        Static Method: This method operates on the parameters passed to it and does not require access to
        any specific instance variables of the Game class. It encapsulates the functionality of the player's turn.
        """
        while player_hand.get_value() < 21:
            choice = input("Please choose 'Hit' or 'Stand': ").lower()
            if choice in ["stand", "s"]:
                break
            elif choice in ["hit", "h"]:
                player_hand.add_card(deck.deal(1))
                player_hand.display()
            else:
                print("Please enter 'Hit' (H) or 'Stand' (S).")

    @staticmethod
    def dealer_turn(dealer_hand, deck):
        """
         Handle the dealer's turn.

         Static Method: Similar to player_turn, this method operates on the parameters passed to it and does not
         require access to any specific instance variables of the Game class. It encapsulates the functionality
         of the dealer's turn.
         """
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal(1))
        dealer_hand.display(show_all_dealer_cards=True)

    @staticmethod
    def check_winner(player_hand, dealer_hand, game_over=False):
        """
        Determine the winner of the game.

        Static Method: This method operates on the parameters passed to it and does not require access to any
        specific instance variables of the Game class. It encapsulates the functionality of determining the winner.
        """
        player_value = player_hand.get_value()
        dealer_value = dealer_hand.get_value()

        if player_value > 21:
            print("You busted! Dealer wins.")
            return True
        elif dealer_value > 21:
            print("Dealer busted! You win.")
            return True
        elif game_over:
            if player_value > dealer_value:
                print("You win!")
            elif player_value < dealer_value:
                print("Dealer wins!")
            else:
                print("It's a tie!")
            return True
        return False

    @staticmethod
    def show_final_results(player_hand, dealer_hand):
        """
        Display the final results of the game.

        Static Method: Similar to check_winner, this method operates on the parameters passed to it and does not
        require access to any specific instance variables of the Game class. It encapsulates the functionality
        of displaying the final results of the game.
        """
        print("Final Results")
        print("Your hand:", player_hand.get_value())
        print("Dealer's hand:", dealer_hand.get_value())
        Game.check_winner(player_hand, dealer_hand, game_over=True)

    @staticmethod
    def ask_to_play_again():
        """
        Ask the player if they want to play again.

        Static Method: This method operates on the parameters passed to it and does not require access to any
        specific instance variables of the Game class. It encapsulates the functionality of asking the player if they want to continue playing.
        """
        while True:
            choice = input("Do you want to play again? (Y/N): ").lower()
            if choice in ["y", "yes"]:
                return True
            elif choice in ["n", "no"]:
                return False
            else:
                print("Please enter 'Y' (Yes) or 'N' (No).")


# Create a game instance and start the game
if __name__ == "__main__":
    g = Game()
    g.play()
