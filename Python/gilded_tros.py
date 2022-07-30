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


def item_factory(name, sell_in, quality):
    # TODO: needs to be implemented
    return Item(name, sell_in, quality)


class ItemWrapper(Item, ABC):
    """
    Wrap old item class to extend the functionality.
    Each implementation class of the ItemWrapper will need implement update_quality(days=1).
    """

    def __init__(self, item: Item):
        super().__init__(item.name, item.sell_in, item.quality)
        self._item = item
        self._check_item_constraints()

    @abstractmethod
    def update_quality(self, days: int=1) -> None:
        pass

    @abstractmethod
    def _check_item_constraints(self):
        pass

class RegularItemWrapper(ItemWrapper, ABC):

    def update_quality(self, days: int=1) -> None:
        pass

    def _check_item_constraints(self)-> None:
        pass

class GoodWineItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass

class LegendaryItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass

class BackstageItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass

class SmellyItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        pass
