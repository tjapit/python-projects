import unittest
from sortingutils import SortingUtils

class TestCase(unittest.TestCase):
    """Tests the mergesort implementation"""
    def test_mergesort(self):
        test_list = [2, 3, 1, 5, 4]
        SortingUtils.mergesort(test_list)
        for i in range(1, len(test_list) + 1):
            self.assertEqual(i, test_list[i - 1])

if __name__ == '__main__':
    unittest.main()
