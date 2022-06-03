import unittest
from linked_list import LinkedList

class TestLinkedList(unittest.TestCase):


    # def setUp(self):
    #     """Sets up tests by constructing a new empty list
    #     **For some reason Pylance acts up and says that there is 'no newList defined' eventhough the test runs fine
    #     **Nvm, with an instance setUp() method, we need to add the 'self' keyword to the instantiated variable used for testing... Enter @classmethod
    #     """
    #     # construct list
    #     self.newList: LinkedList = LinkedList()

    @classmethod
    def setUpClass(cls) -> None:
        """ **Still need to use self. """
        cls.__newlist: LinkedList = LinkedList()
        return super().setUpClass()

    def test_LinkedList(self):
        # test empty node and 0 size
        self.assertEqual(None, self.__newlist.front())
        self.assertTrue(self.__newlist.is_empty())
        self.assertEqual(0, self.__newlist.size())
    
    def test_add(self):
        # raises IndexError if out of bounds
        with self.assertRaises(IndexError):
            self.__newlist.add(1, 1)
            self.__newlist.add(1, -1)
        
        # add to empty list
        self.__newlist.add(1, 0)
        self.assertEqual(1, self.__newlist.front())
        self.assertEqual(1, self.__newlist.size())
        self.assertFalse(self.__newlist.is_empty())

        # add to front
        self.__newlist.add(2, 0)
        self.assertEqual(2, self.__newlist.front())
        self.assertEqual(2, self.__newlist.size())
        self.assertFalse(self.__newlist.is_empty())

        # add to middle
        self.__newlist.add(3, 1)
        self.assertEqual(2, self.__newlist.front())
        self.assertEqual(3, self.__newlist.size())
        self.assertFalse(self.__newlist.is_empty())

        # add to end
        self.__newlist.add(5, self.__newlist.size())
        self.assertEqual(2, self.__newlist.front())
        self.assertEqual(4, self.__newlist.size())
        self.assertFalse(self.__newlist.is_empty())






if __name__ == '__main__':
    unittest.main()