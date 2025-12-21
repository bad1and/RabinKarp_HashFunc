def chetsum_hash(s: str, p: int = 31, m: int = 10 ** 9 + 7) -> int:
    name = "ChetSum_Hash"
    """Только символы на чётных позициях"""
    h = 0
    for i in range(0, len(s), 2):  # 0, 2, 4, ...
        h += ord(s[i])
    return h
