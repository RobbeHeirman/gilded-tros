# -*- coding: utf-8 -*-
import unittest

from gilded_tros import Item, GildedTros


class GildedTrosTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_tros = GildedTros(items)
        gilded_tros.update_quality()
        self.assertEqual("foo", items[0].name)


class ItemConstructorTest(unittest.TestCase):

    # TODO: Item constructor happy day
    def test_item_happy_day(self):
        pass

    def test_good_wine_happy_day(self):
        pass

    def test_legendary_item_happy_day(self):
        pass

    def test_backstage_passes_happy_day(self):
        pass
# TODO: Constructor boundary tests.
# TODO: test raise ValuError quality UPPER_BOUNDARY > item > LOWER_BOUNDARY
# TODO: test raise ValueError legendary item != 80


class UpdateQualityTest(unittest.TestCase):
    pass
# TODO: update_quality tests
# TODO: Happy day scenario -> check end result after x loops for each kind of item
# TODO: check invariants during update_quality function
#       - item boundaries
#       - legendary item

if __name__ == '__main__':
    unittest.main()
