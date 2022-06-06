class SortingUtils:

    @staticmethod
    def mergesort(array:list) -> list:
        """Sorts the given list using mergesort
        
        Args:
            array (list): list to be sorted
        Returns:
            list:the sorted list
        """
        n = len(array)
        if n == 1:
            return array
        mid = n // 2
        left = array[:mid]
        right = array[mid:]
        SortingUtils.mergesort(left)
        SortingUtils.mergesort(right)
        SortingUtils.__merge(left, right, array)
    
    def __merge(left:list, right:list, array:list) -> list:
        """Merges the left and right lists and returns a single list where the elements are sorted from the left and right lists.

        Args:
            left (list): left half of the original list
            right (list): right half of the original list
            array (list): original list

        Returns:
            list: sorted list from left and right
        """
        leftidx = 0
        rightidx = 0

        return array

