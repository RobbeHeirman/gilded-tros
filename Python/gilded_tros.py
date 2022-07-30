# -*- coding: utf-8 -*-

# TODO: What is the purpose of this class?
import bisect
from abc import ABC, abstractmethod


class GildedTros(object):

    def __init__(self, items):
        self.items = items
        # for sake of argument let's assume we can't assign the wrapper items to self.items
        self._wrapped_items = [item_wrapper_factory(item) for item in items]

    def update_quality(self, days: int = 1) -> None:
        """
        Main driver function. progresses the quality of items by given days.
        :param days: the amount of days to progress. defaults to 1
        :return:
        """
        for wrap_item in self._wrapped_items:
            wrap_item.update_quality(days)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


def _regular_deterioration(days: int, start_days, factor: float, overdue_factor: float) -> float:
    """
    Calculates how much reduction on quality needs to be applied. Takes into account when a item is overdue.
    :param days: days we progress
    :param start_days: day we started from
    :param factor: the factor to reduce with
    :param overdue_factor: the factor that is applied when an item is overdue
    :return: the amount to reduce
    """

    negative_days = min((0, start_days - days)) * -1
    positive_days = days - negative_days
    positive_reduction = positive_days * factor
    negative_reduction = negative_days * factor * overdue_factor
    return positive_reduction + negative_reduction


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

    # def __repr__(self):
    #     return self._item.__repr__()

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
        Subclasses must implement update_quality. Updates the quality and amount of sell in days on an item.
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

        new_val = self._item.quality - _regular_deterioration(days,
                                                              self.sell_in,
                                                              self.QUALITY_DETERIORATION_RATE,
                                                              self.OVERDUE_FACTOR
                                                              )
        self._item.sell_in -= days
        self._item.quality = max((new_val, ItemWrapper.QUALITY_LOWER_BOUND))


class _GoodWineItemWrapper(ItemWrapper):
    def update_quality(self, days: int = 1) -> None:
        """
        Good wine always increases in quality
        :param days:  amount of days we progress. Defaults to 1
        :return: None
        """

        self._item.sell_in -= days
        new_val = self.__class__.QUALITY_DETERIORATION_RATE * days + self._item.quality
        self._item.quality = min((self.__class__.QUALITY_UPPER_BOUND, new_val))


class _LegendaryItemWrapper(ItemWrapper):
    ITEM_QUALITY = 80

    def update_quality(self, days: int = 1) -> None:
        """
        A legendary item doesn't update his quality.
        :param days: amount of days we progress. Defaults to 1
        """

        self._item.sell_in -= days

    def _check_item_constraints(self) -> None:
        if not self._item.quality == _LegendaryItemWrapper.ITEM_QUALITY:
            raise ValueError(f'Legendary items always have a quality of {self.ITEM_QUALITY} now {self._item.quality}')


class _BackstageItemWrapper(ItemWrapper):
    QUALITY_THRESHOLDS = {
        10: 2 * ItemWrapper.QUALITY_DETERIORATION_RATE,
        5: 3 * ItemWrapper.QUALITY_DETERIORATION_RATE,
    }

    def update_quality(self, days: int = 1) -> None:
        """
        The interesting one. Backstage passes have different quality rates based on how close they are to the
        sell in day.
        :param days: amount of days we progress. Defaults to 1
        :return:
        """

        # Let's save where we started from
        original_days = self._item.sell_in
        original_quality = self._item.quality

        self._item.sell_in -= days

        # After the conference :(
        # Interpreted as still holds value on the day of the conference.
        if original_days - days < 0:
            self._item.quality = 0
            return

        keys = sorted(self.__class__.QUALITY_THRESHOLDS.keys())
        for day in range(1, days + 1):
            day_at = original_days - day
            # Bisect returns where on the left side we will need to insert the element to keep the list sorted.
            # Then it also holds true in what interval our number falls.
            key_index = bisect.bisect_left(keys, day_at)
            if key_index < len(keys):
                original_quality += self.__class__.QUALITY_THRESHOLDS[keys[key_index]]
            else:
                # print(original_quality)
                original_quality += self.__class__.QUALITY_DETERIORATION_RATE

            self._item.quality = min(self.__class__.QUALITY_UPPER_BOUND, original_quality)


class _SmellyItemWrapper(ItemWrapper):
    DETERIORATION_RATE = 2 * ItemWrapper.QUALITY_DETERIORATION_RATE

    def update_quality(self, days: int = 1) -> None:

        deter = _regular_deterioration(days, self.sell_in, self.DETERIORATION_RATE, self.OVERDUE_FACTOR)
        new_val = self.quality - deter

        self._item.sell_in -= days
        self._item.quality = max((self.QUALITY_LOWER_BOUND, new_val))


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
        case 'Backstage passes for Re:Factor' | 'Backstage passes for HAXX':
            return _BackstageItemWrapper(item)
        case 'Duplicate Code', 'Long Methods' | 'Ugly Variable Names':
            return _SmellyItemWrapper(item)
        case _:
            return _RegularItemWrapper(item)
