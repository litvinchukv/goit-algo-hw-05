def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2

        # Якщо знайдено точний збіг
        if arr[mid] == target:
            return (iterations, arr[mid])

        # Якщо значення в середині менше за цільове значення
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            upper_bound = arr[mid]

    # Якщо не знайдено точного збігу, "верхня межа" — це найменший елемент, більший за цільове значення
    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]

    return (iterations, upper_bound)
if __name__ == "__main__":
    # Тестуємо функцію:
    sorted_array = [0.5, 1.2, 2.4, 3.8, 4.1, 5.7, 6.3]
    target = 3.0

    result = binary_search(sorted_array, target)
    print("Кількість ітерацій:", result[0])
    print("Верхня межа:", result[1])