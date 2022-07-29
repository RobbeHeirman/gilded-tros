# -*- coding: utf-8 -*-
import itertools
import unittest
from gilded_tros import Item, GildedTros, item_factory
import constants

_ITEM_NAMES = (
    "Ring of Cleansening Code",
    "Elixir of the SOLID",
    "A DRY glass of wine",
    "A composite cocktail",
    "Inherited drinking debt",
    "Polymorphic beer"
)
_GOOD_WINE = (
    "Good Wine",
)
_BACKSTAGE_PASSES = (
    "Backstage passes for Re:Factor",
    "Backstage passes for HAXX"
)

_LEGENDARY_ITEMS = (
    "B-DAWG Keychain",
)

_SMELLY_ITEMS = (
    "Duplicate Code",
    "Long Methods",
    "Ugly Variable Names"
)


def _regular_quality_item_names():
    return _ITEM_NAMES + _GOOD_WINE + _BACKSTAGE_PASSES + _SMELLY_ITEMS


def _item_generator(names: [str], sell_days: int, quality: int) -> [Item]:
    return [item_factory(names, sell_days, quality) for name in names]


class GildedTrosTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_tros = GildedTros(items)
        gilded_tros.update_quality()
        self.assertEqual("foo", items[0].name)


class ItemConstructorTest(unittest.TestCase):
    def test_item_happy_day(self):
        test_names = _regular_quality_item_names()
        for test_name in test_names:
            for quality in range(constants.ITEM_QUALITY_LOWER_BOUND, constants.ITEM_QUALITY_UPPER_BOUND + 1):
                item = item_factory(test_name, 0, quality)
                self.assertTrue(
                    constants.ITEM_QUALITY_LOWER_BOUND <= item.quality <= constants.ITEM_QUALITY_UPPER_BOUND)

    def test_legendary_item_happy_day(self):
        for test_name in _LEGENDARY_ITEMS:
            item = item_factory(test_name, 0, constants.LEGENDARY_ITEM_QUALITY)
            self.assertEqual(item.quality, constants.LEGENDARY_ITEM_QUALITY)

    # TODO: Constructor boundary tests.
    def test_item_boundaries(self):
        test_names = _regular_quality_item_names()
        # Value lower boundary upper boundary
        for name in test_names:
            with self.assertRaises(ValueError):
                item_factory(name, 468, constants.ITEM_QUALITY_LOWER_BOUND - 1)

            with self.assertRaises(ValueError):
                item_factory(name, 468, constants.ITEM_QUALITY_UPPER_BOUND + 1)

    def test_legendary_item_boundaries(self):

        modified = (
            -1 * constants.LEGENDARY_ITEM_QUALITY,
            constants.LEGENDARY_ITEM_QUALITY - 1,
            constants.LEGENDARY_ITEM_QUALITY + 1,
            -1 * constants.LEGENDARY_ITEM_QUALITY - 1,
            -1 * constants.LEGENDARY_ITEM_QUALITY + 1,
            constants.LEGENDARY_ITEM_QUALITY + (1 / 2 ** 55),  # ULP in python?
            constants.LEGENDARY_ITEM_QUALITY - (1 / 2 ** 55)
        )

        for name, modified_quality in itertools.product(_LEGENDARY_ITEMS, modified):
            with self.assertRaises(ValueError):
                item_factory(name, 404, modified_quality)


# TODO: update_quality tests
class UpdateQualityTest(unittest.TestCase):
    # TODO: Happy day scenario -> check end result after x loops for each kind of item
    def setUp(self) -> None:
        self.starting_item_quality = 15  # Arbitrary number
        self.sell_days = 30
        self.regular_items = _item_generator(_ITEM_NAMES, self.sell_days, self.starting_item_quality)
        self.good_wine = item_factory(_GOOD_WINE, self.sell_days, self.starting_item_quality)
        self.legendary_items = _item_generator(_LEGENDARY_ITEMS,
                                               self.sell_days,
                                               constants.LEGENDARY_ITEM_QUALITY)
        self.smelly_items = _item_generator(_SMELLY_ITEMS, self.sell_days, self.starting_item_quality)

    def test_update_quality_happy_day(self):
        items_to_test = self.regular_items + self.legendary_items + self.smelly_items + self.good_wine
        driver = GildedTros(items_to_test)

    # TODO: check invariants during update_quality function
    def test_invariant_item_boundaries(self):
        pass

    def test_invariant_legendary_item(self):
        pass


if __name__ == '__main__':
    unittest.main()
