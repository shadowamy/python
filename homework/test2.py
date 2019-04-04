
def BinarySearch(lists, left, right, key, tag, mid=0, found=False):
    count = len(lists[left:right + 1]) + 1
    if tag == 0:
        mid = count // 2
    elif tag == 1:
        mid += count // 2
    else:
        mid -= count // 2

    if lists[mid] == key:
        found = True
    else:
        while left < right:
            if lists[mid] > key:
                right = mid
                tag = 2
                return BinarySearch(lists, left, right, key, tag, mid, found)
            elif lists[mid] < key:
                left = mid + 1
                tag = 1
                return BinarySearch(lists, left, right, key, tag, mid, found)
    if found:
        print (key, 'found, index is ', mid)
    elif left >= right and not found:
        print (key, 'is not found in lists')



