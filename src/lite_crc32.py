def rolling_crc32(s: str, crc: int = 0) -> int:
    name = "Lite_CRC32"
    """
    УПРОЩЁННЫЙ CRC32 ДЛЯ СКОЛЬЗЯЩЕГО ХЕШИРОВАНИЯ
    """
    poly = 0xEDB88320  # стандартный полином CRC32

    for char in s:
        byte = ord(char)
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1

    return crc