def weighted_sum_hash_optimized(s: str, base: int = 31) -> int:
    name = "weighted_sum_hash"
    """
    Оптимизированная взвешенная сумма.
    Использует накопление веса вместо возведения в степень.
    """
    h = 0
    weight = 1
    for char in s:
        h += ord(char) * weight
        weight *= base  # увеличиваем вес для следующего символа
    return h