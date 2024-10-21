import timeit

# Load the contents of the files
file1_path = "стаття 1.txt"
file2_path = "стаття 2.txt"

with open(file1_path, 'r', encoding='cp1251', errors='ignore') as f1:
    text1 = f1.read()

with open(file2_path, 'r', encoding='cp1251', errors='ignore') as f2:
    text2 = f2.read()

# Choose substrings for testing
substring_existing_file1 = "алгоритм"
substring_non_existing = "unexistingword"
substring_existing_file2 = "рекомендаційна"

# Implement search algorithms

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0 # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1




def knuth_morris_pratt(text, pattern):
    m = len(pattern)
    n = len(text)

    # Preprocessing: compute the longest prefix-suffix array
    lps = [0] * m
    j = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                lps[i] = 0
                i += 1

    # Searching
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j  # Pattern found
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  # Pattern not found

def rabin_karp(text, pattern, q=101):  # q is a prime number
    m = len(pattern)
    n = len(text)
    d = 256
    p = 0  # Hash value for pattern
    t = 0  # Hash value for text
    h = 1

    for _ in range(m - 1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i  # Pattern found
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1  # Pattern not found

# Measure execution time for each algorithm and substring

def measure_time(search_function, text, pattern):
    start_time = timeit.default_timer()
    result = search_function(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time

# Results dictionary
results = {
    "file1": {
        "existing": {},
        "non_existing": {}
    },
    "file2": {
        "existing": {},
        "non_existing": {}
    }
}

# Measure for file1 with existing substring
results["file1"]["existing"]["Boyer-Moore"] = measure_time(boyer_moore_search, text1, substring_existing_file1)
results["file1"]["existing"]["KMP"] = measure_time(knuth_morris_pratt, text1, substring_existing_file1)
results["file1"]["existing"]["Rabin-Karp"] = measure_time(rabin_karp, text1, substring_existing_file1)

# Measure for file1 with non-existing substring
results["file1"]["non_existing"]["Boyer-Moore"] = measure_time(boyer_moore_search, text1, substring_non_existing)
results["file1"]["non_existing"]["KMP"] = measure_time(knuth_morris_pratt, text1, substring_non_existing)
results["file1"]["non_existing"]["Rabin-Karp"] = measure_time(rabin_karp, text1, substring_non_existing)

# Measure for file2 with existing substring
results["file2"]["existing"]["Boyer-Moore"] = measure_time(boyer_moore_search, text2, substring_existing_file2)
results["file2"]["existing"]["KMP"] = measure_time(knuth_morris_pratt, text2, substring_existing_file2)
results["file2"]["existing"]["Rabin-Karp"] = measure_time(rabin_karp, text2, substring_existing_file2)

# Measure for file2 with non-existing substring
results["file2"]["non_existing"]["Boyer-Moore"] = measure_time(boyer_moore_search, text2, substring_non_existing)
results["file2"]["non_existing"]["KMP"] = measure_time(knuth_morris_pratt, text2, substring_non_existing)
results["file2"]["non_existing"]["Rabin-Karp"] = measure_time(rabin_karp, text2, substring_non_existing)


print(results)