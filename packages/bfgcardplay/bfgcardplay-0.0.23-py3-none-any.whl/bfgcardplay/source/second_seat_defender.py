"""Second seat card play for defender."""
from termcolor import colored

import inspect

from ..logger import log

from bridgeobjects import Card, CARD_VALUES, SUITS, Suit, Trick
import bfgcardplay.source.global_variables as global_vars
from .player import Player
from .second_seat import SecondSeat
from .defender_play import get_hilo_signal_card, signal_card, surplus_card, best_discard

MODULE_COLOUR = 'green'

class SecondSeatDefender(SecondSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the second seat."""
        player = self.player
        manager = global_vars.manager
        trick = player.board.tricks[-1]

        cards = player.cards_for_trick_suit(trick)

        # Singleton
        if len(cards) == 1:
            return log(inspect.stack(), cards[0])

        # Void
        if not cards:
            return self._select_card_if_void(player, trick)

        # cover honour with honour
        # TODO see this web site http://www.rpbridge.net/4l00.htm
        cover_allowed = True
        if player.dummy_on_right:
            if player.dummy_holds_adjacent_card(trick.cards[0]):
                cover_allowed = False

        # Top of touching honours
        # suit_cards = player.suit_cards[trick.suit.name]
        # if (len(suit_cards) > 1 and
        #         suit_cards[0].value == suit_cards[1].value + 1 and
        #         suit_cards[1].value >= 9):
        #     return log(inspect.stack(), suit_cards[1])

        if player.is_winner_declarer(cards[0]) and len(player.dummys_unplayed_cards[trick.suit.name]) <= 2:
            return log(inspect.stack(), cards[0])

        if cover_allowed and trick.cards[0].value >= CARD_VALUES['9']: # nine or above
            if len(cards) >= 2:
                if cards[1].value >= CARD_VALUES['T']:
                    for card in cards[::-1]:
                        if card.value > trick.cards[0].value:
                            return log(inspect.stack(), card)

        # If winner and last opportunity to play it
        if player.trump_suit and cards:
            opponents_trumps = len(player.opponents_unplayed_cards[player.trump_suit.name])
            safe_tricks = 13 - len(player.board.tricks) - opponents_trumps
            opponents_cards = player.opponents_unplayed_cards[trick.suit.name]
            if opponents_cards:
                opponents_top_card = player.opponents_unplayed_cards[trick.suit.name][0].value
                winners = 0
                if player.is_winner_defender(cards[0], trick):
                    return log(inspect.stack(), cards[0])
                # for card in cards:
                #     if player.is_winner_defender(card, trick):
                #         winners +=1
                #     else:
                #         break
                # if safe_tricks <= winners:
                #     return log(inspect.stack(), cards[0])

        # else:  # TODO add something for NT contracts
        #         for card in cards[::-1]:
        #             if card.value > trick.cards[0].value:
        #                 return card

        # Play honour if higher honour in dummy
        if player.dummy_on_right:
            for card in cards:
                if card.is_honour and card.rank != 'A':
                    value = card.value
                    test_card = Card(CARD_VALUES[value+1], trick.suit.name)
                    if test_card in player.dummys_unplayed_cards[trick.suit.name]:
                        return log(inspect.stack(), card)

        # Win trick if winner in other suit # TODO why?
        if cards and player.is_winner_defender(cards[0], trick):
            for suit, other_cards in player.unplayed_cards.items():
                if other_cards and suit != trick.suit.name:
                    if player.is_winner_defender(other_cards[0], trick):
                        return log(inspect.stack(), cards[0])

        # Signal even/odd
        if not trick.suit == player.trump_suit:
            return get_hilo_signal_card(player, cards)

        return log(inspect.stack(), cards[-1])

    def _select_card_if_void(self, player: Player, trick: Trick) -> Card:
        """Return card if cannot follow suit."""
        player.record_void(trick.suit)
        trick = player.board.tricks[-1]
        manager = global_vars.manager

        # Trump if appropriate
        if player.trump_suit and player.unplayed_cards[player.trump_suit] and not player.is_defender:
            if not player.opponents_trumps:
                return log(inspect.stack(), player.unplayed_cards[player.trump_suit][-1])
            elif len(player.total_unplayed_cards[trick.suit.name]) > 7: # TODO crude
                return log(inspect.stack(), player.unplayed_cards[player.trump_suit][-1])
            else:
                return log(inspect.stack(), player.unplayed_cards[player.trump_suit][0])


        best_suit = self._best_suit(player)

        # Signal suit preference."""
        card = signal_card(player, manager, best_suit)
        if card:
            return log(inspect.stack(), card)

        # Discard if more cards than the opposition
        card = surplus_card(player)
        if card:
            return log(inspect.stack(), card)

        # Best discard
        return best_discard(player)

    def _best_suit(self, player: Player) -> Suit:
        """Select suit for signal."""
        # TODO handle no points and equal suits
        cards = player.hand_cards.list
        suit_points = player.get_suit_strength(cards)
        max_points = 0
        best_suit = None
        for suit in SUITS:
            hcp = suit_points[suit]
            if hcp > max_points:
                max_points = hcp
                best_suit = suit
        if not best_suit:
            return player.longest_suit
        return Suit(best_suit)
