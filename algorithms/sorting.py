
def bubble_sort(arr):
    arr = arr.copy()
    steps = []

    for i in range(len(arr)):
        swapped = False

        for j in range(len(arr) - i - 1):
            steps.append((arr.copy(), j, j + 1, "compare"))

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append((arr.copy(), j, j + 1, "swap"))

        if not swapped:
            break

    return arr, steps


def selection_sort(arr):
    arr = arr.copy()
    steps = []

    for i in range(len(arr)):
        minimum = i

        for j in range(i + 1, len(arr)):
            steps.append((arr.copy(), minimum, j, "compare"))

            if arr[j] < arr[minimum]:
                minimum = j

        if minimum != i:
            arr[i], arr[minimum] = arr[minimum], arr[i]
            steps.append((arr.copy(), i, minimum, "swap"))

    return arr, steps


def insertion_sort(arr):
    arr = arr.copy()
    steps = []

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append((arr.copy(), j, j + 1, "shift"))
            j -= 1

        arr[j + 1] = key
        steps.append((arr.copy(), j + 1, i, "insert"))

    return arr, steps


def merge_sort(arr):
    arr = arr.copy()
    steps = []

    def merge_sort_range(left, right):
        if right - left <= 1:
            return arr[left:right]

        middle = (left + right) // 2
        a = merge_sort_range(left, middle)
        b = merge_sort_range(middle, right)

        merged = []
        i = j = 0

        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1

        merged.extend(a[i:])
        merged.extend(b[j:])
        arr[left:right] = merged
        steps.append((arr.copy(), left, right - 1, "merge"))
        return merged

    merge_sort_range(0, len(arr))
    return arr, steps


def quick_sort(arr):
    arr = arr.copy()
    steps = []

    def partition(low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            steps.append((arr.copy(), j, high, "compare"))

            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append((arr.copy(), i, j, "swap"))

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append((arr.copy(), i + 1, high, "pivot"))
        return i + 1

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(arr) - 1)
    return arr, steps
