def double_hash(s: str) -> int:
    name = "Combinbated_double_Hash"
    """
    КОМБИНИРОВАННЫЙ ХЕШ
    Два полинома с разными параметрами для уменьшения коллизий.

    Возвращает 64-битное значение: (hash1 << 32) | hash2
    """
    h1 = 0
    h2 = 0
    p1, m1 = 31, 10 ** 9 + 7
    p2, m2 = 37, 10 ** 9 + 9

    for char in s:
        code = ord(char)
        h1 = (h1 * p1 + code) % m1
        h2 = (h2 * p2 + code) % m2

    return (h1 << 32) | h2  # объединяем два хеша