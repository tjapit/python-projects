class SortingUtils:

    @staticmethod
    def mergesort(array:list) -> list:
        """Sorts the given list using mergesort
        
        Args:
            array (list): list to be sorted
        Returns:
            list:the sorted list
        """
        n:int = len(array)
        if n == 1:
            return array
        mid:int = n // 2
        left:list = array[:mid]
        right:list = array[mid:]
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
        leftidx:int = 0
        rightidx:int = 0
        currentidx:int = leftidx + rightidx
        n:int = len(array)
        while currentidx < n:
            # picking from right sublist, 
            # if the right sublist has been exhausted or 
            # left sublist still has elements and 
            # the current value on left sublist is less than current value on right sublist
            if rightidx == len(right) or (leftidx < len(left) and left[leftidx] < right[rightidx]):
                # place item from right sublist of right index in the current index (left + right index) of original array 
                array[currentidx] = left[leftidx]
                leftidx += 1
            # picking from left sublist
            else:
                # place item from left sublist of left index in current index of original array
                array[currentidx] = right[rightidx]
                rightidx += 1
            # update current index on original array
            currentidx = leftidx + rightidx

        return array

