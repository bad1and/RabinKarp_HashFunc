def first_last_hash(s: str, base: int = 31) -> int:
    name = "First_Last_Hash"

    """Только первый и последний символ"""

    if not s:
        return 0
    return ord(s[0]) + ord(s[-1])
