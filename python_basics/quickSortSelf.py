def QuickSort(unsorted):
    if len(unsorted == 0 || 1)
        return unsorted
    else
        middle = unsorted[0]
        left = [less for less in unsorted[1:] if less <= middle]
        right = [greater for greater in unsorted[1:] if greater > middle]
        return QuickSort(left) + [middle] + QuickSort(right)
