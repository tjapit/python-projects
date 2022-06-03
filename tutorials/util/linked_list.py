from typing_extensions import Self


class LinkedList:

    def __init__(self) -> None:
        self._front : ListNode = None
        self._size : int = 0

    def size(self) -> int:
        """ Returns the size of the list
        
        Return:
            int:size of the list
        """
        return self._size

    def add(self, value:int, idx:int) -> None:
        """ Add an item to the given index of list
        
        Args:
            value (int):integer to add to list
            idx (int):integer of the index
        """
        # out of bounds
        if (idx < 0 or idx > self._size):
            raise IndexError
        # empty list
        if self.is_empty():
            # construct node with the value and add to list
            self._front = ListNode(value, None)
        # beginning of list
        if idx == 0:
            # construct new node with its next node as front
            newNode: ListNode = ListNode(value, self._front)
            # reassign new node as the front node
            self._front = newNode
        # elsewhere
        else:    
            # set current to front of list
            current = self._front
            # traverse list until index-1 is reached
            i:int = 0
            while i < idx - 1 and current._next != None:
                current = current._next
                i += 1
            # construct new node with value to the middle/end of list
            current._next = ListNode(value, current._next) if idx != self.size() else ListNode(value, None)

        # increment size count
        self._size += 1
            
    def remove(self, idx:int) -> int:
        """ Returns the element removed
        
        Return:
            int:element removed
        """
        pass

    def is_empty(self) -> bool:
        """ Returns True if the list is empty
        
        Return:
            bool:True if the list is empty

        """
        return True if self._size == 0 else False

    def front(self) -> int:
        """ Returns the front of the list
        
        Return:
            ListNode:front node of the list or None if list is empty
        """
        if self.is_empty():
            return None
        return self._front.get_value()




class ListNode:
    def __init__(self, value: int, next: Self) -> None:
        self._value = value
        self._next = next
    

    def get_value(self) -> int:
        """ Returns the value in the node
        
        Return:
            int:value in the node
        """
        return self._value

    # def set_value(self, value: int) -> None:
    #     """ Sets the value in the node
        
    #     Args:
    #         value (int):value to be set
    #     """
    #     self._value = value

        
