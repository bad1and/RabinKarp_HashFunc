import time


class RabinKarp:

    def __init__(self, hash_func, hash_name: str = ""):
        self.hash_func = hash_func
        self.hash_name = hash_name

        # Если передали linear_hash, но не указали имя
        if hasattr(hash_func, 'name'):
            self.hash_name = hash_func.name

        self.collisions = 0
        self.checks = 0
        self.time_ns = 0

    def _get_rolling_func(self, pattern_length: int, p: int = 31, m: int = 10 ** 9 + 7):

        # Для linear_hash (линейный поиск) - НЕТ скользящего хеша
        if "linear" in self.hash_name.lower():
            return None  # Будем пересчитывать каждый раз

        if "simple" in self.hash_name.lower():
            return self._simple_rolling

        elif "weighted" in self.hash_name.lower():
            return self._weighted_rolling

        elif "polynomial" in self.hash_name.lower():
            return lambda h, old, new: self._polynomial_rolling(h, old, new, pattern_length, p, m)

        else:
            return None

    def _simple_rolling(self, old_hash: int, old_char: str, new_char: str) -> int:
        # Скользящий хеш для simple_hash (сумма кодов)
        return old_hash - ord(old_char) + ord(new_char)

    def _weighted_rolling(self, old_hash: int, old_char: str, new_char: str,
                          first_char_weight: int, base: int = 31) -> int:
        # Скользящий хеш для weighted_sum_hash
        return (old_hash - ord(old_char) * first_char_weight) * base + ord(new_char)

    def _polynomial_rolling(self, old_hash: int, old_char: str, new_char: str,
                            m: int, p: int = 31, mod: int = 10 ** 9 + 7) -> int:
        # Скользящий хеш для polynomial_hash
        p_pow = pow(p, m - 1, mod)

        new_hash = (old_hash - ord(old_char) * p_pow) % mod

        new_hash = (new_hash * p + ord(new_char)) % mod

        return new_hash

    def _linear_search(self, pattern: str, text: str, start_time: int) -> int:
        # Оптимизированный линейный поиск для linear_hash
        m = len(pattern)
        n = len(text)
        total_windows = n - m + 1

        # Простой линейный поиск
        for i in range(total_windows):
            if text[i:i + m] == pattern:
                self.checks = i + 1
                self.collisions = 0  # коллизий нет
                self.time_ns = time.perf_counter_ns() - start_time
                return i

        # Не нашли
        self.checks = total_windows
        self.collisions = 0
        self.time_ns = time.perf_counter_ns() - start_time
        return -1

    def find(self, pattern: str, text: str) -> int:
        # Сбрасываем статистику
        self.collisions = 0
        self.checks = 0

        # замер времени
        start_time = time.perf_counter_ns()

        # Проверка данных
        if not pattern or not text or len(pattern) > len(text):
            self.time_ns = time.perf_counter_ns() - start_time
            return -1

        m = len(pattern)
        n = len(text)

        # ОБРАБОТКА ДЛЯ LINEAR_HASH
        if "linear" in self.hash_name.lower():
            return self._linear_search(pattern, text, start_time)

        """
        Поиск паттерна в тексте.
        Возвращает позицию первого вхождения или -1 если не найдено.
        """
        # Сбрасываем статистику
        self.collisions = 0
        self.checks = 0

        # Начинаем замер времени
        start_time = time.perf_counter_ns()

        # Проверка входных данных
        if not pattern or not text or len(pattern) > len(text):
            self.time_ns = time.perf_counter_ns() - start_time
            return -1

        m = len(pattern)
        n = len(text)

        # 1. Вычисляем хеш паттерна
        pattern_hash = self.hash_func(pattern)

        # 2. Вычисляем хеш первого окна текста
        first_window = text[:m]
        window_hash = self.hash_func(first_window)

        # 3. Получаем функцию для скользящего хеша
        rolling_func = self._get_rolling_func(m)

        first_char_weight = 1
        if "weighted" in self.hash_name.lower():
            first_char_weight = 31 ** (m - 1)

        # 4. Основной цикл поиска
        for i in range(n - m + 1):
            # Если хеши совпали
            if window_hash == pattern_hash:
                # Увеличиваем счётчик проверок
                self.checks += 1

                # Проверяем посимвольно (на случай коллизии)
                if text[i:i + m] == pattern:
                    # Нашли! Завершаем замер времени
                    self.time_ns = time.perf_counter_ns() - start_time
                    return i
                else:
                    # Коллизия: хеши совпали, но строки разные
                    self.collisions += 1

            if i < n - m:
                if rolling_func:
                    old_char = text[i]
                    new_char = text[i + m]

                    if "weighted" in self.hash_name.lower():
                        window_hash = rolling_func(window_hash, old_char, new_char, first_char_weight)
                    elif "polynomial" in self.hash_name.lower():
                        window_hash = rolling_func(window_hash, old_char, new_char)
                    else:
                        window_hash = rolling_func(window_hash, old_char, new_char)
                else:
                    # Для функций без скользящего хеша пересчитываем с нуля
                    window = text[i + 1:i + m + 1]
                    window_hash = self.hash_func(window)

        # Паттерн не найден
        self.time_ns = time.perf_counter_ns() - start_time
        return -1

    def get_stats(self) -> dict:
        # Возвращает статистику выполнения
        return {
            "collisions": self.collisions,
            "checks": self.checks,
            "time_ns": self.time_ns,
            "time_ms": self.time_ns / 1_000_000,
            "time_sec": self.time_ns / 1_000_000_000
        }
