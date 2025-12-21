import csv
import os

from src.double_hash import double_hash
from src.hash_simple import simple_hash
from src.lite_crc32 import rolling_crc32
from src.chetsum_hash import chetsum_hash
from src.rabin_karp import RabinKarp
from src.first_last_hash import first_last_hash

checks_file_name = "war_and_peace.txt"


def load_text(filepath: str) -> str:
    """Загружает текст из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Пробуем другую кодировку если UTF-8 не работает
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def save_to_csv(data, filename=f"results/checks/checks_graph_data_{checks_file_name[:3]}.csv"):
    """Сохраняет данные о коллизиях в CSV файл"""

    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Заголовки CSV
        writer.writerow([
            'hash_function',
            'pattern_length',
            'pattern',
            'time_ms',
            'collisions',
            'checks',
            'total_windows',
            'found',
            'position'
        ])

        # Данные
        for row in data:
            writer.writerow(row)

    return filename


def create_checks_metrics():
    ##############################################################
    # ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ

    # Длины паттернов для тестирования коллизий (меньше и короче)
    pattern_lengths = [2, 3, 4, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50, 100]

    # Хеш-функции с именами
    hash_functions = [
        ("simple_hash", simple_hash),
        ("first_last_hash", first_last_hash),
        ("chetsum_hash", chetsum_hash),
        ("rolling_crc32", rolling_crc32),
        ("double_hash", double_hash),
    ]
    ##############################################################

    # Проверяем наличие файла
    path_to_file = f"texts/{checks_file_name}"
    if not os.path.exists(path_to_file):
        print(f"Файл {path_to_file} не найден!")
        return

    # Загружаем текст
    text = load_text(path_to_file)
    if not text:
        print("Ошибка: не удалось загрузить текст")
        return

    print("=" * 70)
    print("ТЕСТИРОВАНИЕ CHECKS ПОСЛЕДОВАТЕЛЬНОСТИ")
    print(f"Файл: {path_to_file}")
    print(f"Длина текста: {len(text)} символов")


    # Данные для CSV
    csv_data = []

    # Словарь с ДНК паттернами
    dna_patterns = {
        2: "AT",
        3: "ATC",
        4: "ATCG",
        6: "ATCGAT",
        8: "ATCGATCG",
        10: "ATCGATCGAT",
        12: "ATCGATCGATCG",
        16: "ATCGATCGATCGATCG",
        20: "ATCGATCGATCGATCGATCG",
        25: "ATCGATCGATCGATCGATCGATCG",
        30: "ATCGATCGATCGATCGATCGATCGATCG",
        40: "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG",
        50: "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG",
        100: "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
    }

    # Основной цикл тестирования
    for pattern_len in pattern_lengths:
        # Берём паттерн из словаря или генерируем
        if pattern_len in dna_patterns:
            pattern = dna_patterns[pattern_len]
        else:
            # Генерируем случайный ДНК паттерн
            import random
            pattern = "".join(random.choice("ATCG") for _ in range(pattern_len))

        # Проверяем, что можем взять паттерн
        if pattern_len > len(text):
            print(f"Пропускаем паттерн {pattern_len} символов: длиннее текста")
            continue

        total_windows = len(text) - pattern_len + 1

        for hash_name, hash_func in hash_functions:
            # Создаем алгоритм
            algorithm = RabinKarp(hash_func)

            # Запускаем поиск
            position = algorithm.find(pattern, text)

            # Получаем статистику
            stats = algorithm.get_stats()

            # Сохраняем данные для CSV
            csv_data.append([
                hash_name,
                pattern_len,
                pattern,
                stats['time_ms'],
                stats['collisions'],
                stats['checks'],
                total_windows,
                position != -1,
                position
            ])


    # Сохраняем данные
    if csv_data:
        csv_filename = save_to_csv(csv_data)

        # Создаём текстовую сводку
        summary_filename = f"results/checks/checks_graph_summary_{checks_file_name[:3]}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("СВОДКА РЕЗУЛЬТАТОВ КОЛЛИЗИЙ НА ДНК\n")
            f.write("=" * 70 + "\n\n")

            # Группируем по функциям
            hash_results = {}
            for row in csv_data:
                hash_name = row[0]
                if hash_name not in hash_results:
                    hash_results[hash_name] = []
                hash_results[hash_name].append(row)

            # Пишем для каждой функции
            for hash_name, measurements in hash_results.items():
                total_collisions = sum(r[4] for r in measurements)
                total_checks = sum(r[5] for r in measurements)
                total_windows_sum = sum(r[6] for r in measurements)
                avg_collisions_pct = (total_collisions / total_windows_sum * 100) if total_windows_sum > 0 else 0

                f.write(f"{hash_name:20} | Всего коллизий: {total_collisions:6d} | "
                        f"Средний процент: {avg_collisions_pct:6.1f}% | "
                        f"Всего проверок: {total_checks:6d}\n")

            f.write("\n" + "=" * 70 + "\n")

        print("РАБОТА ПО СОЗДАНИЮ МЕТРИК checks ОКОНЧЕНА УСПЕШНО")

    else:
        print("Ошибка: не собраны данные для сохранения")
