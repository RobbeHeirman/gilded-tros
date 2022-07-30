# -*- coding: utf-8 -*-

# TODO: What is the purpose of this class?
from abc import ABC, abstractmethod


class GildedTros(object):

    def __init__(self, items):
        self.items = items
        self._wrapped_items = [item_wrapper_factory(item) for item in items]

    def update_quality(self, days: int = 1) -> None:
        """
        Main driver function. progresses the quality of items by given days.
        :param days: the amount of days to progress. defaults to 1
        :return:
        """
        for wrap_item in self._wrapped_items:
            wrap_item.update_quality(days)

        # TODO: quite alot
        # for item in self.items:
        #     if item.name != "Good Wine" and item.name != "Backstage passes for Re:Factor" \
        #             and item.name != "Backstage passes for HAXX":
        #         if item.quality > 0:
        #             if item.name != "B-DAWG Keychain":
        #                 item.quality = item.quality - 1
        #     else:
        #         if item.quality < 50:
        #             item.quality = item.quality + 1
        #             if item.name == "Backstage passes for Re:Factor" or item.name == "Backstage passes for HAXX":
        #                 if item.sell_in < 11:
        #                     if item.quality < 50:
        #                         item.quality = item.quality + 1
        #                 if item.sell_in < 6:
        #                     if item.quality < 50:
        #                         item.quality = item.quality + 1
        #     if item.name != "B-DAWG Keychain":
        #         item.sell_in = item.sell_in - 1
        #     if item.sell_in < 0:
        #         if item.name != "Good Wine":
        #             if item.name != "Backstage passes for Re:Factor" and item.name != "Backstage passes for HAXX":
        #                 if item.quality > 0:
        #                     if item.name != "B-DAWG Keychain":
        #                         item.quality = item.quality - 1
        #             else:
        #                 item.quality = item.quality - item.quality
        #         else:
        #             if item.quality < 50:
        #                 item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemWrapper(ABC):
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
        assert isinstance(item, Item)
        self._item = item
        self._check_item_constraints()

    def __repr__(self):
        return self._item.__repr__()

    @property
    def name(self):
        return self._item.name

    @property
    def sell_in(self):
        return self._item.sell_in

    @property
    def quality(self):
        return self._item.quality

    @abstractmethod
    def update_quality(self, days: int = 1) -> None:
        """
        Sub classes must implement update_quality. Updates the quality and amount of sell in days on an item.
        :param days: the amount of days we want to update for. Defaults to 1
        :return: None
        """
        pass

    def _check_item_constraints(self):
        if not ItemWrapper.QUALITY_LOWER_BOUND <= self._item.quality <= ItemWrapper.QUALITY_UPPER_BOUND:
            raise ValueError(f'Item Quality bounds not respected: = {self._item.quality}. Must be between '
                             f'({ItemWrapper.QUALITY_LOWER_BOUND},{ItemWrapper.QUALITY_UPPER_BOUND})')


class _RegularItemWrapper(ItemWrapper, ABC):

    def update_quality(self, days: int = 1) -> None:
        """
        For regular items the rules are simple.
        They deteriorate each day. And if their sell_in day is reached they deteriorate twice as fast.
        :param days: amount of days we progress. Defaults to 1
        :return: None
        """
        negative_days = min((0, self._item.sell_in - days)) * -1
        positive_days = days - negative_days

        positive_reduction = positive_days * ItemWrapper.QUALITY_DETERIORATION_RATE
        negative_reduction = negative_days * ItemWrapper.QUALITY_DETERIORATION_RATE * ItemWrapper.OVERDUE_FACTOR

        self._item.sell_in -= days
        self._item.quality -= positive_reduction + negative_reduction


class _GoodWineItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        pass


class _LegendaryItemWrapper(ItemWrapper):
    ITEM_QUALITY = 80

    def update_quality(self, days: int = 1) -> None:
        pass

    def _check_item_constraints(self) -> None:
        if not self._item.quality == _LegendaryItemWrapper.ITEM_QUALITY:
            raise ValueError(f'Legendary items always have a quality of {self.ITEM_QUALITY} now {self._item.quality}')


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
    """
    Implements the ItemWrapperfactory => Wrapping a legacy item object into an ItemWrapper object.
    Will select the appropriate implementation class based on name.
    :param item: The (legacy item)
    :return: ItemWrapper object.
    """

    # Not a fan of hard coding and deferring types by name.
    # Could introduce magic with regexes? => let's be explicit.
    # Alternative is a dict.
    match item.name:
        case 'B-DAWG Keychain':
            return _LegendaryItemWrapper(item)
        case 'Good Wine':
            return _GoodWineItemWrapper(item)
        case 'Backstage passes for Re:Factor', 'Backstage passes for HAXX':
            return _BackstageItemWrapper(item)
        case 'Duplicate Code', 'Long Methods', 'Ugly Variable Names':
            return _SmellyItemWrapper(item)
        case _:
            return _RegularItemWrapper(item)
