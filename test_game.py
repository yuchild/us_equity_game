import unittest
from game import settle

class GameTests(unittest.TestCase):
    def test_up_wins(self):
        self.assertAlmostEqual(settle(100, 102, "Up", 1000, 1).profit, 20)
    def test_down_wins(self):
        self.assertAlmostEqual(settle(100, 98, "Down", 1000, 3).profit, 20)
    def test_flat(self):
        self.assertEqual(settle(100, 100, "Up", 1000, 5).profit, 0)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            settle(0, 100, "Up", 1000, 1)

if __name__ == "__main__":
    unittest.main()
