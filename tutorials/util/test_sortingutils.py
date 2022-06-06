import unittest
from sortingutils import SortingUtils
import sys

class TestCase(unittest.TestCase):
    """Tests the SortingUtils sort algorithms implementation"""

    def setUp(self) -> None:
        self.__test_list:list = [2, 3, 1, 5, 4]
        self.__sorted_list:list = sorted(self.__test_list)
        return super().setUp()
        
    def test_mergesort(self) -> None:
        """ Tests mergesort algo """
        self.assertListEqual(self.__sorted_list, SortingUtils.mergesort(self.__test_list))

    def test_bubblesort(self) -> None:
        """ Tests bubblesort algo """
        self.assertListEqual(self.__sorted_list, SortingUtils.bubblesort(self.__test_list))

if __name__ == '__main__':
    unittest.main()
