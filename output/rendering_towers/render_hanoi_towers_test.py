# This file is part of the Hanoi project
# © 2025 - Multi-AI collaborative development (Claude Sonnet 4 & Gemini 2.5 Pro)
# This is free and unencumbered software released into the public domain.
# For more information, please refer to the LICENSE file or <https://unlicense.org>

import unittest
from .render_hanoi_towers import padded_rendered_tower

class TestPaddedRenderedTower(unittest.TestCase):
    def test_single_disk(self):
        # Tower with one disk of width 2, max_height 3
        expected = (
            "  |  \n"
            "  |  \n"
            "__|__"
        )
        self.assertEqual(padded_rendered_tower([2], 3), expected)

    def test_multiple_disks(self):
        # Tower with disks [3, 2, 1], max_height 5
        expected = (
            "   |   \n"
            "   |   \n"
            "  _|_  \n"
            " __|__ \n"
            "___|___"
        )
        result = padded_rendered_tower([3, 2, 1], 5)
        self.assertEqual(result, expected, f"Expected:\n{expected}\n\nGot:\n{result}")

    def test_empty_tower(self):
        # No disks, just rod
        expected = ("|\n|\n|\n|\n|")
        self.assertEqual(padded_rendered_tower([], 5), expected)

    def test_known_random_tower(self):
        # Tower with disks [4, 2], max_height 3
        expected = (
            "    |    \n"
            "  __|__  \n"
            "____|____"
        )
        # This is a demonstration; adjust expected as per actual render_tower output
        result = padded_rendered_tower([4, 2], 3)
        self.assertEqual(result, expected, f"Expected:\n{expected}\n\nGot:\n{result}")


if __name__ == '__main__':
    unittest.main()