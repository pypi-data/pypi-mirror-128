"""Methods to support declarer play."""
from typing import List, Dict, Tuple, Union
from termcolor import colored

import inspect
from ..logger import log

from bridgeobjects import Card, Suit, CARD_VALUES
from bfgsupport import Trick

import bfgcardplay.source.global_variables as global_vars
from .player import Player

MODULE_COLOUR = 'magenta'

def lead_to_find_missing_ace(player: Player,
                            suit: Suit,
                            trick: Union[Trick, None]=None) -> Union[Card, None]:
    """Return the appropriate card if missing the ace."""
    manager = global_vars.manager
    my_suit_cards = player.suit_cards[suit]
    partners_suit_cards = player.partners_suit_cards[suit]
    max_length = max(len(my_suit_cards), len(partners_suit_cards))
    if max_length >= 4:
        if (Card('K', suit.name) in player.our_unplayed_cards[suit.name] and
                Card('Q', suit.name) in player.our_unplayed_cards[suit.name] and
                Card('J', suit.name) in player.our_unplayed_cards[suit.name] and
                Card('T', suit.name) in player.our_unplayed_cards[suit.name]):
                for card in my_suit_cards:
                    if card.value >= CARD_VALUES['T']:
                        return log(inspect.stack(), card)

    partners_entries = player.get_entries_in_other_suits(player.partners_hand, suit)
    if ((Card('K', suit.name) in my_suit_cards and
                Card('Q', suit.name) in my_suit_cards and partners_entries) or
                (Card('Q', suit.name) in my_suit_cards and
                Card('J', suit.name) in my_suit_cards and partners_entries) ):
        card = _make_entry_to_partners_hand(player, manager, partners_entries)
        if card:
            return log(inspect.stack(), card)
    return my_suit_cards[-1]

def _make_entry_to_partners_hand(player, manager, partners_entries):
    """Return a card to enable partner to return suit_to_develop."""
    for entry in partners_entries:
        entry_suit = entry.suit.name
        my_entry_cards = player.suit_cards[entry_suit]
        if my_entry_cards:
            manager.win_trick[player.partner_seat] = True
            return my_entry_cards[-1]
    return None

def handle_missing_king(player: Player, suit: Suit) -> Union[Card, None]:
    """Return the appropriate card if missing the king."""
    manager = global_vars.manager
    my_suit_cards = player.suit_cards[suit]
    partners_suit_cards = player.partners_suit_cards[suit]
    my_entries = player.get_entries_in_other_suits(player.hand, suit)
    partners_entries = player.get_entries_in_other_suits(player.partners_hand, suit)

    tenace_in_my_hand = player.get_suit_tenaces(my_suit_cards)
    right_hand_opponent_is_void = manager.voids[player.right_hand_seat][suit.name]
    if tenace_in_my_hand and right_hand_opponent_is_void:
        for card in my_suit_cards:
            if card.value < CARD_VALUES['K']:
                return log(inspect.stack(), card)

    if tenace_in_my_hand and len(partners_entries) >= 1:
        card = _make_entry_to_partners_hand(player, manager, partners_entries)
        if card:
            return log(inspect.stack(), card)

    tenace_in_partners_hand = player.get_suit_tenaces(partners_suit_cards)
    queen = Card('Q', suit.name)
    jack = Card('J', suit.name)
    if tenace_in_partners_hand and len(my_entries) >= 1:
        return log(inspect.stack(), my_suit_cards[-1])
    elif queen in my_suit_cards and jack in my_suit_cards:
        return log(inspect.stack(), queen)
    elif queen in partners_suit_cards and jack in partners_suit_cards:
        return log(inspect.stack(), my_suit_cards[-1])

    for card in my_suit_cards[::-1]:
        if player.is_winner_declarer(card):
            return log(inspect.stack(), card)
        else:
            return log(inspect.stack(), my_suit_cards[0])

    print(colored(f'handle_missing_king return None {suit}', MODULE_COLOUR))
    return None

def handle_missing_queen(player: Player,
                            suit: Suit,
                            trick: Union[Trick, None]=None) -> Union[Card, None]:
    """Return the appropriate card if missing the queen."""
    manager = global_vars.manager
    my_suit_cards = player.suit_cards[suit]
    partners_suit_cards = player.partners_suit_cards[suit]

    if not partners_suit_cards:
        return log(inspect.stack(), my_suit_cards[0])

    if len(player.our_cards[suit.name]) >= 9:
        if trick:
            trick_cards = trick.cards
        else:
            trick_cards = []
        if Card('A', suit.name) in my_suit_cards and Card('K', suit.name) not in trick_cards:
            return log(inspect.stack(), my_suit_cards[0])
        if Card('K', suit.name) in my_suit_cards and Card('A', suit.name) not in trick_cards:
            return log(inspect.stack(), my_suit_cards[0])
        return log(inspect.stack(), my_suit_cards[-1])

    my_entries = player.get_entries_in_other_suits(player.hand, suit)
    partners_entries = player.get_entries_in_other_suits(player.partners_hand, suit)

    tenace_in_my_hand = player.get_suit_tenaces(my_suit_cards)
    right_hand_opponent_is_void = manager.voids[player.right_hand_seat][suit.name]
    if tenace_in_my_hand and right_hand_opponent_is_void:
        for card in my_suit_cards:
            if card.value < CARD_VALUES['Q']:
                return log(inspect.stack(), card)

    if tenace_in_my_hand and len(partners_entries) >= 1:
        card = _make_entry_to_partners_hand(player, manager, partners_entries)
        if card:
            return log(inspect.stack(), card)

    if Card('A', suit.name) in partners_suit_cards:
        return log(inspect.stack(), my_suit_cards[-1])

    if not tenace_in_my_hand:
        tenace_in_partners_hand = player.get_suit_tenaces(partners_suit_cards)
        if tenace_in_partners_hand and len(my_entries) >= 1:
            if my_suit_cards[0].rank == 'A' or my_suit_cards[0].rank == 'K':
                return log(inspect.stack(), my_suit_cards[0])
            else:
                return log(inspect.stack(), my_suit_cards[-1])

    for card in my_suit_cards[::-1]:
        if player.is_winner_declarer(card):
            return log(inspect.stack(), card)
        else:
            manager.card_to_play[player.partner_seat] = player.partners_unplayed_cards[suit.name][-1]
            return log(inspect.stack(), my_suit_cards[0])
    print(colored(f'handle_missing_queen return None {suit}', MODULE_COLOUR))
    return None