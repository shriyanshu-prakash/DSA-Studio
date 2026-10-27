
def linear_search(arr, target):
    steps = []

    for i, value in enumerate(arr):
        steps.append((i, value, "compare"))

        if value == target:
            steps.append((i, value, "found"))
            return i, steps

    return -1, steps


def binary_search(arr, target):
    if arr != sorted(arr):
        raise ValueError("Binary search requires a sorted array.")

    steps = []
    left, right = 0, len(arr) - 1

    while left <= right:
        middle = (left + right) // 2
        steps.append((middle, arr[middle], "compare"))

        if arr[middle] == target:
            steps.append((middle, arr[middle], "found"))
            return middle, steps

        if arr[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1, steps
