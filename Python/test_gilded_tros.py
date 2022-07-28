# -*- coding: utf-8 -*-
import unittest

from gilded_tros import Item, GildedTros


class GildedTrosTest(unittest.TestCase):
    # TODO: Fix existing test. What part of the code does this test? Constructor or update quality?
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_tros = GildedTros(items)
        gilded_tros.update_quality()
        self.assertEquals("foo", items[0].name)


# TODO: Item constructor test (Pre conditions).
# TODO: Item constructor happy day
# TODO: Constructor boundary tests.
# TODO: test raise ValuError quality UPPER_BOUNDARY > item > LOWER_BOUNDARY
# TODO: test raise ValueError legendary item != 80

# TODO: update_quality tests
# TODO: Happy day scenario -> check end result after x loops for each kind of item
# TODO: check invariants during update_quality function
#       - item boundaries
#       - legendary item

if __name__ == '__main__':
    unittest.main()
