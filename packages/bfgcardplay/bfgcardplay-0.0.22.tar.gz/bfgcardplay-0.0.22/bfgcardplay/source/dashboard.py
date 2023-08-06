"""Provide the Dashboard class for bfgcardplay."""

from typing import List, Dict, Tuple
from termcolor import colored

from bridgeobjects import Hand, Card, Suit, SUITS, RANKS

MODULE_COLOUR = 'magenta'

class Dashboard():
    "Statistics for a player."
    def __init__(self, player) -> None:
        self.player = player
        if not player.is_defender:
            self.threats = self._get_threats()
            self.winners = self._get_suit_winners()
            self.winner_count = self._get_winner_count()
            self.suit_lengths = self._suit_lengths()
            self.extra_winners_length = self._extra_winners_length()
            # extra_winners_strength must be generated after winners
            self.extra_winners_strength = self._extra_winners_strength()
            # if player.seat == 'E':
            #     for suit in SUITS:
            #         print(colored(f'{self.threats[suit]}', MODULE_COLOUR))

    def __repr__(self):
        print(colored(f'self.threats={self.threats}', MODULE_COLOUR))
        print(colored(f'self.winners={self.winners}', MODULE_COLOUR))
        print(colored(f'self.suit_lengths={self.suit_lengths}', MODULE_COLOUR))
        print(colored(f'self.extra_winners_length={self.extra_winners_length}', MODULE_COLOUR))
        print(colored(f'self.extra_winners_strength={self.extra_winners_strength}', MODULE_COLOUR))
        return ''

    def _get_threats(self) -> Dict[str, Card]:
        """Return a dict of cards by suit that threaten players cards."""
        if self.player.trump_suit:
            return self._get_threats_suit_contract()
        else:
            return self._get_threats_nt_contract()

    def _get_threats_nt_contract(self) -> Dict[str, Card]:
        """Return a dict of cards by suit that threaten players cards."""
        player = self.player

        threats = {suit: [] for suit in SUITS}
        ranks = [rank for rank in RANKS]
        ranks.reverse()
        sorted_ranks = ranks[:-1]

        for suit in SUITS:
            long_cards = player.unplayed_cards[suit]
            our_cards = player.our_unplayed_cards[suit]
            opponents_cards = player.opponents_unplayed_cards[suit]
            missing = len(opponents_cards)
            winners = 0
            skip_card = False
            for index, rank in enumerate(sorted_ranks):
                ranking_card = Card(rank, suit)
                if ranking_card in player.total_unplayed_cards[suit]:
                    if ranking_card in our_cards:
                        if not skip_card:
                            winners += 1
                        skip_card = False

                        # No more cards to lose
                        if winners > missing:
                            break
                    else:
                        threats[suit].append(ranking_card)
                        # skip card means that the next card in the suit is assumed to have been beaten
                        skip_card = True

                    #threats only in long hand
                    if index + 1 >= len(long_cards):
                        break
                if len(opponents_cards) <= index + 1:
                    break
        return threats

    def _get_threats_suit_contract(self) -> Dict[str, Card]:
        """Return a dict of cards by suit that threaten players cards."""
        player = self.player
        (long_hand, short_hand) = self.get_long_short_trump_hands()
        unplayed_cards = player.cards_by_suit(long_hand)
        long_cards = unplayed_cards[player.trump_suit.name]

        threats = {suit: [] for suit in SUITS}
        ranks = [rank for rank in RANKS]
        ranks.reverse()
        sorted_ranks = ranks[:-1]

        for suit in SUITS:
            our_cards = player.our_unplayed_cards[suit]
            my_cards = player.unplayed_cards[suit]
            partners_cards = player.partners_unplayed_cards[suit]
            max_length = max(len(my_cards), len(partners_cards))
            opponents_cards = player.opponents_unplayed_cards[suit]
            missing = len(opponents_cards)
            winners = 0
            skip_card = False
            for index, rank in enumerate(sorted_ranks):
                ranking_card = Card(rank, suit)
                if ranking_card in player.total_unplayed_cards[suit]:
                    if ranking_card in our_cards:
                        if not skip_card:
                            winners += 1
                        skip_card = False

                        # Only count to the number of cards in our hands
                        if index + 1 >= max_length:
                            break

                        # No more cards to lose
                        if winners > missing:
                            break
                    else:
                        threats[suit].append(ranking_card)
                        # skip card means that the next card in the suit is assumed to have been beaten
                        skip_card = True

                    #threats only in long hand
                    if index + 1 >= len(long_cards):
                        break
                if len(opponents_cards) <= index + 1:
                    break
        return threats

    def get_long_short_trump_hands(self) -> Tuple[Hand, Hand]:
        """Return the  hands for long and short trump hand between player and partner."""
        return self.get_long_short_hands(self.player.trump_suit)

    def get_long_short_hands(self, suit: Suit) -> Tuple[Hand, Hand]:
        """Return the  hands for long and short hand between player and partner."""
        player = self.player
        my_unplayed_cards = player.unplayed_cards
        partners_unplayed_cards = player.partners_unplayed_cards
        if len(my_unplayed_cards[suit.name]) >= len(partners_unplayed_cards[suit.name]):
            return (player.hand, player.partners_hand)
        else:
            return (player.partners_hand, player.hand)

        # declarers_cards = player.get_unplayed_cards_by_suit(suit, player.declarer)
        # dummys_cards = player.get_unplayed_cards_by_suit(suit, player.dummy)

        # if len(declarers_cards) > len(dummys_cards):
        #     long_hand = player.declarer
        # else:
        #     long_hand = player.dummy

        # if long_hand == player.seat:
        #     long_unplayed_cards = player.unplayed_cards
        #     short_unplayed_cards = player.partners_unplayed_cards
        # else:
        #     short_unplayed_cards = player.unplayed_cards
        #     long_unplayed_cards = player.partners_unplayed_cards
        # return (long_unplayed_cards, short_unplayed_cards)

    def _get_suit_winners(self) -> Dict[str, Card]:
        """Return a dict of cards by suit that are certain winners."""
        player = self.player
        winners = {suit: [] for suit in SUITS}
        our_cards = player.our_unplayed_cards
        opponents_cards = player.opponents_unplayed_cards
        my_cards = player.unplayed_cards
        partners_cards = player.partners_unplayed_cards
        for suit in SUITS:
            if len(my_cards[suit]) > len(partners_cards[suit]):
                our_length = len(my_cards[suit])
            else:
                our_length = len(partners_cards[suit])
            for card in our_cards[suit]:
                if len(winners[suit]) < our_length:
                    if opponents_cards[suit]:
                        if card.value > opponents_cards[suit][0].value:
                            winners[suit].append(card)
                    else:
                        winners[suit].append(card)
        return winners

    def _suit_lengths(self) -> Dict[str, int]:
        """Return a dict of suit_lengths."""
        player = self.player
        suit_lengths = {suit: [] for suit in SUITS}
        our_cards = player.our_unplayed_cards
        opponents_cards = player.opponents_unplayed_cards
        for suit in SUITS:
            suit_lengths[suit] = len(our_cards[suit])
        return suit_lengths

    def _extra_winners_length(self):
        """Return a dict of potential extra length winners by suit."""
        player = self.player
        splits = {
            6: 4,
            5: 3,
            4: 3,
            3: 2,
            2: 2,
            1: 1,
            0: 0,
        }
        extra_winners = {suit: 0 for suit in SUITS}
        our_cards = player.our_unplayed_cards
        my_cards = player.unplayed_cards
        partners_cards = player.partners_unplayed_cards
        opponents_cards = player.opponents_unplayed_cards
        for suit in SUITS:
            if not len(our_cards[suit]) > len(opponents_cards[suit]):
                break
            our_length = max(len(my_cards[suit]), len(partners_cards[suit]))
            split = splits[len(opponents_cards[suit])]
            extra_winners[suit] = our_length - split
        return extra_winners

    def _extra_winners_strength(self):
        """Return a dict of potential extra strength winners by suit."""
        player = self.player
        extra_winners = {suit: [] for suit in SUITS}
        our_cards = player.our_unplayed_cards
        my_cards = player.unplayed_cards
        partners_cards = player.partners_unplayed_cards
        opponents_cards = player.opponents_unplayed_cards
        honours = 'AKQJT'
        for suit in SUITS:
            if len(my_cards[suit]) > len(partners_cards[suit]):
                our_length = len(my_cards[suit])
            else:
                our_length = len(partners_cards[suit])
            # if suit == 'C' and (player.is_declarer or player.is_dummy):
            #     print(colored(f'x {long_hand}', MODULE_COLOUR))
            for honour in honours:
                cards = our_cards[suit]
                test_card = Card(honour, suit)
                if test_card in opponents_cards[suit]:
                    test_cards = []
                    for rank in honours.replace(honour, ''):
                        test_cards.append(Card(rank, suit))
                    for index, card in enumerate(test_cards):
                        if card in  cards and our_length >= index + 2:
                            if card not in extra_winners[suit] and card not in self.winners[suit]:
                                extra_winners[suit].append(card)
        return extra_winners

    def _get_winner_count(self) -> int:
        """Return the total number of winners."""
        winner_count = 0
        for suit, cards in self.winners.items():
            winner_count += len(cards)
        return winner_count

