# -*- coding: utf-8 -*-
import itertools
import unittest

from gilded_tros import Item, GildedTros, item_wrapper_factory, ItemWrapper, _LegendaryItemWrapper, _SmellyItemWrapper, \
    _BackstageItemWrapper
# TODO documentation

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
    return [Item(name, sell_days, quality) for name in names]


def _item_wrapper_generator(names: [str], sell_days: int, quality: int) -> [Item]:
    return [item_wrapper_factory(Item(name, sell_days, quality)) for name in names]


class GildedTrosTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_tros = GildedTros(items)
        gilded_tros.update_quality()
        self.assertEqual("foo", items[0].name)


class ItemConstructorTest(unittest.TestCase):
    def test_item_happy_day(self):
        test_names = _regular_quality_item_names()
        for quality in range(ItemWrapper.QUALITY_LOWER_BOUND, ItemWrapper.QUALITY_UPPER_BOUND + 1):
            items = _item_wrapper_generator(test_names, 44, quality)
            for item in items:
                self.assertTrue(
                    ItemWrapper.QUALITY_LOWER_BOUND <= item.quality <= ItemWrapper.QUALITY_UPPER_BOUND)

    def test_legendary_item_happy_day(self):
        items = _item_wrapper_generator(_LEGENDARY_ITEMS, 0, _LegendaryItemWrapper.ITEM_QUALITY)
        for item in items:
            self.assertEqual(item.quality, _LegendaryItemWrapper.ITEM_QUALITY)

    def test_item_boundaries(self):
        test_names = _regular_quality_item_names()
        # Value lower boundary upper boundary
        for name in test_names:
            with self.assertRaises(ValueError):
                item_wrapper_factory(Item(name, 468, ItemWrapper.QUALITY_LOWER_BOUND - 1))

            with self.assertRaises(ValueError):
                item_wrapper_factory(Item(name, 468, ItemWrapper.QUALITY_UPPER_BOUND + 1))

    def test_legendary_item_boundaries(self):

        modified = (
            -1 * _LegendaryItemWrapper.ITEM_QUALITY,
            _LegendaryItemWrapper.ITEM_QUALITY - 1,
            _LegendaryItemWrapper.ITEM_QUALITY + 1,
            -1 * _LegendaryItemWrapper.ITEM_QUALITY - 1,
            -1 * _LegendaryItemWrapper.ITEM_QUALITY + 1,
            _LegendaryItemWrapper.ITEM_QUALITY + (1 / 2 ** 10),
            _LegendaryItemWrapper.ITEM_QUALITY - (1 / 2 ** 10)
        )

        for name, modified_quality in itertools.product(_LEGENDARY_ITEMS, modified):
            with self.assertRaises(ValueError):
                item_wrapper_factory(Item(name, 404, modified_quality))


class BaseUpdateQualityTest(unittest.TestCase):
    """
    Base class to be used to collect some shared test runners.
    """
    driver: GildedTros
    items: [Item]
    SELL_DAYS = 30
    STARTING_ITEM_QUALITY = 45

    def _inner_run(self, run_time, equals):
        for _ in range(int(run_time)):
            self.driver.update_quality()
        for item in self.items:
            self.assertEqual(item.quality, equals)


class UpdateQualityRegularTest(BaseUpdateQualityTest):
    def setUp(self) -> None:
        self.items = _item_wrapper_generator(_ITEM_NAMES, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = self.SELL_DAYS // 2

        self._inner_run(run_range, self.STARTING_ITEM_QUALITY - (run_range * ItemWrapper.QUALITY_DETERIORATION_RATE))
        self._inner_run(run_range, (self.STARTING_ITEM_QUALITY - (
                2 * run_range + self.SELL_DAYS % 2)) * ItemWrapper.QUALITY_DETERIORATION_RATE)
        self._inner_run(1, self.STARTING_ITEM_QUALITY - self.SELL_DAYS - ItemWrapper.OVERDUE_FACTOR)

    def test_invariant_item_boundaries(self):
        for _ in range(self.STARTING_ITEM_QUALITY + self.SELL_DAYS):
            self.driver.update_quality()
        for item in self.items:
            self.assertEqual(item.quality, 0)


class UpdateQualityGoodWineTest(BaseUpdateQualityTest):

    def setUp(self) -> None:
        self.items = _item_wrapper_generator(_GOOD_WINE, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = ItemWrapper.QUALITY_UPPER_BOUND - self.STARTING_ITEM_QUALITY
        interval_increase = run_range * ItemWrapper.QUALITY_DETERIORATION_RATE
        self._inner_run(run_range, self.STARTING_ITEM_QUALITY + interval_increase)

    def test_invariant_item_boundaries(self):
        run_range = ItemWrapper.QUALITY_UPPER_BOUND - self.STARTING_ITEM_QUALITY + 1
        self._inner_run(run_range, ItemWrapper.QUALITY_UPPER_BOUND)


class UpdateQualityLegendaryItems(BaseUpdateQualityTest):

    def setUp(self) -> None:
        self.items = _item_wrapper_generator(_LEGENDARY_ITEMS, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    def test_update_quality_happy_day(self):
        run_range = self.SELL_DAYS // 2
        self._inner_run(run_range, _LegendaryItemWrapper.ITEM_QUALITY)

    def test_invariant_legendary_item_boundaries(self):
        run_range = self.SELL_DAYS * 2
        self._inner_run(run_range, _LegendaryItemWrapper.ITEM_QUALITY)


class UpdateQualityBackstageItems(BaseUpdateQualityTest):
    def setUp(self) -> None:
        self.items = _item_wrapper_generator(_BACKSTAGE_PASSES, self.SELL_DAYS, self.STARTING_ITEM_QUALITY)
        self.driver = GildedTros(self.items)

    # TODO: could be useful somewhere else?
    # TODO: this is getting to complicated in a test => signs of bad design?
    # def _get_value_rate(self, sell_days: int) -> int:
    #     sorted_boundaries_keys = sorted(constants.BACKSTAGE_QUALITY_THRESHOLDS.keys(), key=lambda x: x * - 1)
    #     prev_val = constants.ITEM.QUALITY_DETERIORATION_RATE
    #     for key in sorted_boundaries_keys:
    #         if key <= sell_days:
    #             return prev_val
    #         prev_val = constants.BACKSTAGE_QUALITY_THRESHOLDS[key]
    #     return prev_val

    def test_backstage_happy_day(self):
        sorted_boundaries_keys = sorted(_BackstageItemWrapper.QUALITY_THRESHOLDS.keys(), key=lambda x: x * - 1)
        self.assertGreater(self.SELL_DAYS, sorted_boundaries_keys[0],
                           f'invalid test setup. start sell days ({self.SELL_DAYS}) should be bigger then the biggest'
                           f'sell boundary ({sorted_boundaries_keys[0]})')

        time_ro_run = self.SELL_DAYS - sorted_boundaries_keys[0]
        value_rate = ItemWrapper.QUALITY_DETERIORATION_RATE
        value_now = self.STARTING_ITEM_QUALITY + value_rate
        self._inner_run(time_ro_run, value_now)
        intervals = [abs(j - i) for i, j in zip(sorted_boundaries_keys[:-1], sorted_boundaries_keys[1:])]
        # TODO: Improve this bisect func could be useful
        for i, interval in enumerate(intervals):
            self._inner_run(interval,
                            value_now + interval * _BackstageItemWrapper.QUALITY_THRESHOLDS[sorted_boundaries_keys[i]])


class UpdateQualitySmellyItems(BaseUpdateQualityTest):
    ITEM_QUALITY = 200

    def setUp(self) -> None:
        self.items = _item_wrapper_generator(_SMELLY_ITEMS, self.SELL_DAYS, self.ITEM_QUALITY)

    def test_smelly_happy_day(self):
        time_to_run = self.SELL_DAYS // 2
        # 200  - 2 * 15 = 170,
        self._inner_run(time_to_run,
                        self.STARTING_ITEM_QUALITY - _SmellyItemWrapper.SMELLY_ITEMS_DETERIORATION_RATE * time_to_run)
        # 140
        self._inner_run(time_to_run,
                        self.STARTING_ITEM_QUALITY - _SmellyItemWrapper.SMELLY_ITEMS_DETERIORATION_RATE * time_to_run * 2)
        intermediate_val = self.STARTING_ITEM_QUALITY - _SmellyItemWrapper.SMELLY_ITEMS_DETERIORATION_RATE * time_to_run * 2
        intermediate_val -= _SmellyItemWrapper.SMELLY_ITEMS_DETERIORATION_RATE * self.SELL_DAYS % 2
        self._inner_run(self.SELL_DAYS % 2, intermediate_val)

        # Below 0 sell days
        intermediate_val -= time_to_run * _SmellyItemWrapper.SMELLY_ITEMS_DETERIORATION_RATE * ItemWrapper.OVERDUE_FACTOR
        self._inner_run(time_to_run, intermediate_val)

    def test_boundaries_smelly_items(self):
        run_time = self.ITEM_QUALITY
        self._inner_run(run_time, 0)

    # TODO end to end/ blackbox tests?


if __name__ == '__main__':
    unittest.main()
