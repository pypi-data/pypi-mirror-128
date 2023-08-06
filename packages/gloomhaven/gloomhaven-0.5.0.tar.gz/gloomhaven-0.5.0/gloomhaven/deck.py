import random
from typing import Any, Generator, List, Union

from gloomhaven.mod_applier import ModDeckApplier

from .constants import DEFAULT_DECK, RESET_LIST


class GloomhavenDeck:

    RESET_SET = set(RESET_LIST)

    def __init__(
        self,
        cards: List[str] = None,
        name: str = None,
        shuffle: bool = True,
        mod_applier: ModDeckApplier = None,
    ):
        # map in values
        self.card_list = cards if cards else DEFAULT_DECK
        self.name = name if name else "<default name>"
        if mod_applier is None:
            self.mod_applier = ModDeckApplier(self.mod_fn_factory)
            self._build_modifier_fns()
        else:
            self.mod_applier = mod_applier

        # create copy
        self.current_deck = [*self.card_list]
        if shuffle:
            self._shuffle_deck()

        # error checking
        if all([self._is_continue_card(card) for card in self.card_list]):
            raise ValueError("Invalid deck: contains all continue cards.")

    @staticmethod
    def mod_fn_factory(mod: str):
        def apply_mod(x):
            return x + int(mod) if (x + int(mod)) >= 0 else 0

        return apply_mod

    @staticmethod
    def _is_continue_card(card: str):
        return card[0] == "c"

    @staticmethod
    def _parse_attack_continue_card(card: str):
        return card[1:]

    def _build_modifier_fns(self):
        # build default ones
        self.mod_applier["Miss"] = lambda x: 0
        self.mod_applier["2x"] = lambda x: 2 * x

        # generate mod fns
        for card in set(self.card_list):
            if card not in ["Miss", "2x"] and not self._is_continue_card(card):
                self.mod_applier[card] = self.mod_fn_factory(card)

    def _shuffle_deck(self):
        random.shuffle(self.current_deck)

    def _reset_deck(self):
        self.current_deck = [*self.card_list]

    def _draw_card(self) -> str:
        return self.current_deck.pop()

    def remove_card(self, card: str) -> bool:
        for idx, c in enumerate(self.card_list):
            if c == card:
                _ = self.card_list.pop(idx)
                self._reset_deck()
                return True
        return False

    def add_card(self, card: str) -> bool:
        self.card_list.append(card)
        self._build_modifier_fns()
        self._reset_deck()
        return True

    def draw(self) -> str:
        """Draw card based on playing rules"""

        # if deck is empty reset and shuffle
        if not self.current_deck:
            self._reset_deck()
            self._shuffle_deck()

        # draw card
        card = self._draw_card()

        # reset deck if necessary
        if card in self.RESET_SET:
            self._reset_deck()
            self._shuffle_deck()

        return card

    def get_attack(self, base_attack: int):
        """Get a final attack value from a base attack"""
        card = self.draw()
        attack_dmg = base_attack
        while True:
            if self._is_continue_card(card):
                card = self._parse_attack_continue_card(card)
                attack_dmg = self.mod_applier[card](attack_dmg)
                card = self.draw()
            else:
                return self.mod_applier[card](attack_dmg)

    def simulate(
        self,
        base_attacks: Union[List[int], Generator[int, Any, Any]],
        fresh: bool = True,
    ) -> List[int]:
        if fresh:
            self._reset_deck()
            self._shuffle_deck()

        res = []
        for attack in base_attacks:
            res.append(self.get_attack(attack))
        return res

    def copy(self):
        new_deck = GloomhavenDeck(
            cards=[*self.card_list],
            mod_applier=self.mod_applier,
            name=f"{self.name}_copy",
        )
        new_deck.current_deck = [*self.current_deck]
        return new_deck

    def __repr__(self):
        return "\n".join(
            [
                self.name,
                f"Cards: {', '.join(self.card_list)}",
                f"Current Deck: {', '.join(reversed(self.current_deck))}",
            ]
        )

    def __str__(self):
        return self.__repr__()
