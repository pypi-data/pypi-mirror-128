"""Fourth seat card play for declarer."""
import random
from typing import List, Union, Tuple
from termcolor import colored

import inspect
from ..logger import log

from bridgeobjects import SUITS, Card, Suit, Denomination, CARD_VALUES
from bfgsupport import Trick
from .player import Player
from .fourth_seat import FourthSeat
import bfgcardplay.source.global_variables as global_vars

MODULE_COLOUR = 'cyan'

class FourthSeatDeclarer(FourthSeat):
    def __init__(self, player: Player):
        super().__init__(player)
        self.player = player

    def selected_card(self) -> Card:
        """Return the card if the third seat."""
        player = self.player
        trick = player.board.tricks[-1]
        manager = global_vars.manager

        cards = player.cards_for_trick_suit(trick)

        # Void
        if not cards:
            return self._select_card_if_void(player, trick)

        # Singleton
        if len(cards) == 1:
            return log(inspect.stack(), cards[0])
        if manager.suit_strategy == '':
            pass

        # play low if partner is winning trick
        if self._second_player_winning_trick(cards, trick, player.trump_suit):
            return log(inspect.stack(), cards[-1])

        # When to duck - rule of 7
        duck_trick = False
        if not player.trump_suit:
            duck_trick = self._duck_trick(player, trick, cards)
            if duck_trick:
                return log(inspect.stack(), cards[-1])
            else:
                for card in cards[::-1]:
                    if self.can_win_trick(player, card):
                        return log(inspect.stack(), card)

        # win trick if possible
        winning_card = self._winning_card(trick)
        if winning_card:
            return winning_card

        # play smallest card
        return log(inspect.stack(), cards[-1])


    def _select_card_if_void(self, player: Player, trick: Trick) -> Card:
        """Return card if cannot follow suit."""
        player.record_void(trick.suit)

        # Trump if appropriate
        if player.trump_suit:
            (value_0, value_1, value_2) = self._trick_card_values(trick, player.trump_suit)
            if player.trump_cards:
                if value_0 > value_1 or value_2 > value_1:
                    for card in player.trump_cards[::-1]:
                        if card.value + 13 > value_0 and card.value + 13 > value_2:
                            return log(inspect.stack(), card)

        # Signal best suit
        best_suit = self._best_suit()
        suit_cards = player.suit_cards[best_suit.name]
        for card in suit_cards:
            if not card.is_honour:
                log(inspect.stack(), card)
                return card

        retain_suit = {suit_name: False for suit_name in SUITS}
        if player.is_defender:
            for suit_name in SUITS:
                cards = player.unplayed_cards[suit_name]
                if cards:
                    if len(cards) == 1 and player.is_winner_declarer(cards[0], trick):
                        retain_suit[suit_name] = True

        other_suit = player.other_suit_for_signals(best_suit)
        other_suit_cards = player.suit_cards[other_suit]
        if other_suit_cards and not retain_suit[other_suit]:
            return log(inspect.stack(), other_suit_cards[-1])

        for suit_name in SUITS:
            if suit_name != best_suit.name and suit_name != other_suit:
                final_suit_cards = player.suit_cards[suit_name]
                if final_suit_cards:
                     return log(inspect.stack(), final_suit_cards[-1])

        for suit in SUITS:
            if player.unplayed_cards[suit]:
                return log(inspect.stack(), player.unplayed_cards[suit][-1])

        # cards = player.suit_cards[suit.name]
        # if len(cards) == 1:
        #     log(inspect.stack(), f'{cards[0]}')
        #     return cards[0]

        # for index, card in enumerate(cards[:-1]):
        #     if card.value > cards[index+1].value + 1:
        #         log(inspect.stack(), f'{card}')
        #         return card
        # return log(inspect.stack(), f'{cards[-1]}')

    def _best_suit(self) -> Suit:
        """Select suit for signal."""
        # TODO handle no points and equal suits
        player = self.player
        cards = player.hand_cards.list
        suit_points = player.get_suit_strength(cards)
        max_points = 0
        best_suit = self._strongest_suit()
        return best_suit

    def _strongest_suit(self) -> Union[Suit, None]:
        """Return the strongest_suit."""
        player = self.player
        suits = {suit: 0 for suit in SUITS}
        for suit in SUITS:
            cards = player.unplayed_cards[suit]
            for card in cards:
                suits[suit] += card.value
        if player.trump_suit:
            suits[player.trump_suit.name] = 0
        best_suits = player.get_list_of_best_scores(suits)
        if not best_suits:
            return player.trump_suit
        return Suit(random.choice(best_suits))

    def _duck_trick(self, player: Player, trick: Trick, cards: List[Card]) -> bool:
        """Return True if the player is to duck the trick."""
        opponents_unplayed_cards = player.opponents_unplayed_cards[trick.suit.name]
        if cards and opponents_unplayed_cards:
            # partners_cards = player.partners_suit_cards[trick.suit.name]
            # partner_can_win = False
            # if partners_cards:
            #     if  partners_cards[0].value > trick.cards[0].value:
            #         partner_can_win = True
            if (len(cards) == 2 and cards[0].value == CARD_VALUES['K'] and
                    Card('A', trick.suit.name) in opponents_unplayed_cards):
                return False
            can_win_trick = (cards[0].value > opponents_unplayed_cards[0].value and
                cards[0].value > trick.cards[0].value and
                cards[0].value > trick.cards[2].value)
            if self._rule_of_seven(player, trick) and can_win_trick:
                return False
        return True

    @staticmethod
    def _rule_of_seven(player: Player, trick: Trick) -> bool:
        """Return True if rule of seven applies."""
        our_cards = player.our_cards[trick.suit]
        duck_count = 7 - len(our_cards) - len(player.board.tricks)
        return duck_count < 0