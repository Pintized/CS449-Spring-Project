import random

class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        order = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = [(rank, suit) for suit in suits for rank in order]

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deal_cards(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
