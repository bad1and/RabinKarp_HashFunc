import time


class RabinKarp:
    """Упрощённая реализация алгоритма Рабина-Карпа с одной хеш-функцией"""

    def __init__(self, hash_func):
        self.hash_func = hash_func
        self.collisions = 0
        self.checks = 0
        self.time_ns = 0

    def _simple_rolling_hash(self, old_hash: int, old_char: str, new_char: str) -> int:
        """
        Скользящий хеш для функции суммы.
        Если old_hash = сумма всех символов старого окна,
        то новый хеш = старый - уходящий + приходящий
        """
        return old_hash - ord(old_char) + ord(new_char)

    def find(self, pattern: str, text: str) -> int:
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

        m = len(pattern)  # длина паттерна
        n = len(text)  # длина текста

        # 1. Вычисляем хеш паттерна
        pattern_hash = self.hash_func(pattern)

        # 2. Вычисляем хеш первого окна текста
        first_window = text[0:m]
        window_hash = self.hash_func(first_window)

        # 3. Основной цикл поиска
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

            # Пересчитываем хеш для следующего окна (если оно есть)
            if i < n - m:
                # Убираем уходящий символ, добавляем приходящий
                old_char = text[i]
                new_char = text[i + m]
                window_hash = self._simple_rolling_hash(window_hash, old_char, new_char)

        # Паттерн не найден
        self.time_ns = time.perf_counter_ns() - start_time
        return -1

    def get_stats(self) -> dict:
        """Возвращает статистику выполнения"""
        return {
            "collisions": self.collisions,
            "checks": self.checks,
            "time_ns": self.time_ns,
            "time_ms": self.time_ns / 1_000_000,
            "time_sec": self.time_ns / 1_000_000_000
        }