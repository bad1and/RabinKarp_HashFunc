def simple_hash(s: str) -> int:
    name = "simple_hash_summ_codes"
    """
    Самая простая хеш-функция - сумма кодов символов.
    Много коллизий, но простая для понимания.
    """
    h = 0
    for char in s:
        h += ord(char)  # ord() возвращает код символа
    return h