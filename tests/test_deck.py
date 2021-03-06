"""Test the Deck class"""
# Disable this pylint rule because of a conflict with @pytest.fixture
# See: stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
# pylint: disable=redefined-outer-name

import pytest
from terminal_playing_cards.deck import Deck


def test_ace_high_deck():
    """Ace high specifications are captured in deck build"""
    deck = Deck(specifications=["ace_high"])
    ace_high = deck.pop()
    assert ace_high.value == 14


def test_face_card_are_ten_deck():
    """Face cards worth ten deck specifications are captured in deck build"""
    deck = Deck(specifications=["face_cards_are_ten"])
    cards_worth_ten = [card.face for card in deck if card.value == 10]

    for face_card in ["J", "Q", "K"]:
        assert cards_worth_ten.count(face_card) == 4


def test_only_aces_deck():
    """Custom built deck specifications are captured in deck build"""
    only_aces_deck_spec = {"A": {"clubs": 1, "diamonds": 2, "spades": 3, "hearts": 4}}
    deck = Deck(specifications=only_aces_deck_spec)
    assert len(deck) == 4
    assert all([card.face == "A" for card in deck])


def test_creating_hidden_deck():
    """Parameters are passed from Deck to Card"""
    deck = Deck(hidden=True)
    assert all([card.hidden for card in deck])


def test_adding_decks_together():
    """Stacking multiple decks on top of each other"""
    deck_1 = Deck()
    deck_2 = Deck()
    combined_deck = deck_1 + deck_2
    assert len(combined_deck) == 104


def test_adding_view_to_deck():
    """Add a View to an existing Deck"""
    from terminal_playing_cards import View

    deck = Deck()
    view = View([deck.pop() for _ in range(7)])
    assert len(view) == 7
    assert len(deck) == 45
    deck += view
    assert len(deck) == 52


def test_adding_cards_to_deck():
    """
    Add a list of Cards to an existing Deck,
    ensure that only a list of Cards is accepted
    """
    from terminal_playing_cards import Card

    joker_1 = Card("JK", suit="none")
    joker_2 = Card("JK", suit="none")
    deck = Deck()
    deck += [joker_1, joker_2]
    assert len(deck) == 54

    joker_3 = Card("JK", suit="none")
    with pytest.raises(NotImplementedError):
        deck += joker_3


def test_shuffling_deck():
    """Shuffle method shuffles the deck of cards"""
    deck = Deck()
    original_order = [(card.face, card.suit) for card in deck]
    deck.shuffle()
    shuffled_order = [(card.face, card.suit) for card in deck]
    assert any(
        [
            original[0] != shuffled[0] or original[1] != shuffled[1]
            for original, shuffled in zip(original_order, shuffled_order)
        ]
    )
