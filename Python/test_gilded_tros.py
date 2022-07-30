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
    return [item_factory(name, sell_days, quality) for name in names]


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


class BaseUpdateQualityTest(unittest.TestCase):
    """
    Base class to be used to collect some shared test runners.
    """
    driver: GildedTros
    items: [Item]
    SELL_DAYS = 30
    STARTING_ITEM_QUALITY = 45

    def _inner_run(self, run_time, equals):
        for _ in range(run_time):
            self.driver.update_quality()
        for item in self.items:
            self.assertEqual(item.quality, equals)


class UpdateQualityRegularTest(BaseUpdateQualityTest):
    def setUp(self) -> None:
        self.items = _item_generator(_ITEM_NAMES, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = self.SELL_DAYS // 2

        self._inner_run(run_range, self.STARTING_ITEM_QUALITY - (run_range * constants.ITEM_QUALITY_DETERIORATION_RATE))
        self._inner_run(run_range, (self.STARTING_ITEM_QUALITY - (
                2 * run_range + self.SELL_DAYS % 2)) * constants.ITEM_QUALITY_DETERIORATION_RATE)
        self._inner_run(1, self.STARTING_ITEM_QUALITY - self.SELL_DAYS - constants.ITEM_OVERDUE_FACTOR)

    def test_invariant_item_boundaries(self):
        for _ in range(self.STARTING_ITEM_QUALITY + self.SELL_DAYS):
            self.driver.update_quality()
        for item in self.items:
            self.assertEqual(item.quality, 0)


class UpdateQualityGoodWineTest(BaseUpdateQualityTest):

    def setUp(self) -> None:
        self.items = _item_generator(_GOOD_WINE, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = constants.ITEM_QUALITY_UPPER_BOUND - self.STARTING_ITEM_QUALITY
        interval_increase = run_range * constants.ITEM_QUALITY_DETERIORATION_RATE
        self._inner_run(run_range, self.STARTING_ITEM_QUALITY + interval_increase)

    def test_invariant_item_boundaries(self):
        run_range = constants.ITEM_QUALITY_UPPER_BOUND - self.STARTING_ITEM_QUALITY + 1
        self._inner_run(run_range, constants.ITEM_QUALITY_UPPER_BOUND)


class UpdateQualityLegendaryItems(BaseUpdateQualityTest):

    def setUp(self) -> None:
        self.items = _item_generator(_LEGENDARY_ITEMS, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = self.SELL_DAYS // 2
        self._inner_run(run_range, constants.LEGENDARY_ITEM_QUALITY)

    def test_invariant_legendary_item_boundaries(self):
        run_range = self.SELL_DAYS * 2
        self._inner_run(run_range, constants.LEGENDARY_ITEM_QUALITY)


class UpdateQualityBackstageItems(unittest.TestCase):
    pass


class UpdateQualitySmellyItems(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
