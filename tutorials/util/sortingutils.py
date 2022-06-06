class SortingUtils:
    """ Collection of sorting algorithms. All algorithms sort the given array in place. """

    @staticmethod
    def mergesort(array:list) -> list:
        """Sorts the given list using mergesort
        
        Args:
            array (list): list to be sorted
        Returns:
            list:the sorted list
        """
        n:int = len(array)
        # base case: array with only 1 element
        if n == 1:
            return array
        # median index of array
        mid:int = n // 2
        # left half of array
        left:list = array[:mid]
        # right half of array
        right:list = array[mid:]
        # recursive splitting of the left half
        SortingUtils.mergesort(left)
        # recursive splitting of the right half
        SortingUtils.mergesort(right)
        # return the merged array
        return SortingUtils.__merge(left, right, array)
    
    def __merge(left:list, right:list, array:list) -> list:
        """Merges the left and right lists and returns a single list where the elements are sorted from the left and right lists.

        Args:
            left (list): left half of the original list
            right (list): right half of the original list
            array (list): original list

        Returns:
            list: sorted list from left and right
        """
        # indices for left and right half of the original array respectively
        leftidx:int = 0
        rightidx:int = 0
        # current index being filled on original array
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
        # return sorted array
        return array

    def bubblesort(array:list) -> list:
        """Sorts the given list using bubblesort
        
        Args:
            array (list): list to be sorted
        Returns:
            list:the sorted list
        """
        n:int = len(array)
        # pass over the entire array until no swaps occur
        repeat:bool = True
        while repeat:
            # assume no pass happens, and flip to True when a swap happens
            repeat = False
            for i in range(n - 1):
                # if current value is larger than the one after,
                if array[i] > array[i+1]:
                    # swap the values (large values bubble to the top/end)
                    temp:int = array[i]
                    array[i] = array[i+1]
                    array[i+1] = temp
                    # a swap happened, repeat again
                    repeat = True
        # return sorted array
        return array

        

