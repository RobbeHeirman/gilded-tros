# -*- coding: utf-8 -*-
import unittest
from gilded_tros import Item, GildedTros

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


class GildedTrosTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_tros = GildedTros(items)
        gilded_tros.update_quality()
        self.assertEqual("foo", items[0].name)


class ItemConstructorTest(unittest.TestCase):

    # TODO: Item constructor happy day
    def test_item_happy_day(self):
        test_names = _ITEM_NAMES + _GOOD_WINE + _BACKSTAGE_PASSES + _LEGENDARY_ITEMS + _SMELLY_ITEMS
        # for quality in range()
    def test_good_wine_happy_day(self):
        pass

    def test_legendary_item_happy_day(self):
        pass

    def test_backstage_passes_happy_day(self):
        pass

    # TODO: Constructor boundary tests.
    # TODO: test raise ValuError quality UPPER_BOUNDARY > item > LOWER_BOUNDARY
    def test_item_boundaries(self):
        pass

    # TODO: test raise ValueError legendary item != 80
    def test_legendary_item_boundaries(self):
        pass


# TODO: update_quality tests
class UpdateQualityTest(unittest.TestCase):
    # TODO: Happy day scenario -> check end result after x loops for each kind of item
    def test_update_quality_happy_day(self):
        pass

    # TODO: check invariants during update_quality function
    def test_invariant_item_boundaries(self):
        pass

    def test_invariant_legendary_item(self):
        pass


if __name__ == '__main__':
    unittest.main()
