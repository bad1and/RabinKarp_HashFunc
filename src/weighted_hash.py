def weighted_sum_hash(s: str, base: int = 31) -> int:
    name = "Weighted_Simple_Hash"
    """
    УЛУЧШЕННАЯ СУММА
    Каждый символ умножается на вес, зависящий от позиции.

    Плюсы:
    - Учитывает порядок символов
    - Меньше коллизий чем у simple_sum
    - Достаточно простая

    Минусы:
    - Может переполняться на длинных строках

    Формула: Σ char_i * base^i
    Скользящий хеш: сложнее, нужно хранить веса
    """
    h = 0
    weight = 1
    for char in s:
        h += ord(char) * weight
        weight *= base
    return h