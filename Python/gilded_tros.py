# -*- coding: utf-8 -*-

# TODO: What is the purpose of this class?
from abc import ABC, abstractmethod


class GildedTros(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # TODO: quite alot
        for item in self.items:
            if item.name != "Good Wine" and item.name != "Backstage passes for Re:Factor" \
                    and item.name != "Backstage passes for HAXX":
                if item.quality > 0:
                    if item.name != "B-DAWG Keychain":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes for Re:Factor" or item.name == "Backstage passes for HAXX":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "B-DAWG Keychain":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Good Wine":
                    if item.name != "Backstage passes for Re:Factor" and item.name != "Backstage passes for HAXX":
                        if item.quality > 0:
                            if item.name != "B-DAWG Keychain":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemWrapper(Item, ABC):
    """
    Wrap old item class to extend the functionality.
    Each implementation class of the ItemWrapper will need implement update_quality(days=1).
    """

    # Constants should be in a settings file.
    QUALITY_LOWER_BOUND = 0
    QUALITY_UPPER_BOUND = 50
    QUALITY_DETERIORATION_RATE = 1
    OVERDUE_FACTOR = 2

    def __init__(self, item: Item):
        super().__init__(item.name, item.sell_in, item.quality)
        self._item = item
        self._check_item_constraints()

    @abstractmethod
    def update_quality(self, days: int = 1) -> None:
        pass

    @abstractmethod
    def _check_item_constraints(self):
        pass


class _RegularItemWrapper(ItemWrapper, ABC):

    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass


class _GoodWineItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass


class _LegendaryItemWrapper(ItemWrapper):
    ITEM_QUALITY = 80

    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass


class _BackstageItemWrapper(ItemWrapper):
    QUALITY_THRESHOLDS = {
        10.0: 1 * ItemWrapper.QUALITY_DETERIORATION_RATE,
        5.0: 3 * ItemWrapper.QUALITY_DETERIORATION_RATE,
        -1: 0 * ItemWrapper.QUALITY_DETERIORATION_RATE

    }

    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass


class _SmellyItemWrapper(ItemWrapper):
    SMELLY_ITEMS_DETERIORATION_RATE = 2 * ItemWrapper.QUALITY_DETERIORATION_RATE

    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass


def item_wrapper_factory(item: Item) -> ItemWrapper:
    # Not a fan of hard coding and deferring types by name.
    # Could also explicitly define all items?
    match item.name:

        case _: return _RegularItemWrapper(item)
