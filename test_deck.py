from deck import Deck

def test_has_52_cards():
    deck = Deck()
    assert len(deck.cards) == 52

def test_deck_size():
    deck = Deck()
    deck.deal_cards()
    assert len(deck.cards) == 51
