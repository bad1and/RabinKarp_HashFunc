import csv
import os

from src.double_hash import double_hash
from src.hash_simple import simple_hash
from src.linear_search import linear_search
from src.lite_crc32 import rolling_crc32
from src.chetsum_hash import chetsum_hash
from src.rabin_karp import RabinKarp
from src.first_last_hash import first_last_hash

time_file_name = "war_and_peace.txt"


def load_text(filepath: str) -> str:
    """Загружает текст из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Пробуем другую кодировку если UTF-8 не работает
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def save_to_csv(data, filename=f"results/time/time_graph_data_{time_file_name[:-4]}.csv"):
    """Сохраняет данные в CSV файл для графиков"""

    # Создаем папку results если её нет
    os.makedirs("results", exist_ok=True)

    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Заголовки CSV
        writer.writerow([
            'hash_function',
            'pattern_length',
            'time_ms',
            'collisions',
            'checks',
            'found',
            'position'
        ])

        # Данные
        for row in data:
            writer.writerow(row)

    return filename


def save_summary_to_txt(data, filename=f"results/time/time_summary_{time_file_name[:-4]}.txt"):
    """Сохраняет текстовую сводку результатов"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ: ВРЕМЯ РАБОТЫ\n")
        f.write("=" * 70 + "\n\n")

        # Группируем по хеш-функциям
        hash_groups = {}
        for row in data:
            hash_func = row[0]
            if hash_func not in hash_groups:
                hash_groups[hash_func] = []
            hash_groups[hash_func].append(row)

        # Вывод для каждой функции
        for hash_func, measurements in hash_groups.items():
            f.write(f"\nХЕШ-ФУНКЦИЯ: {hash_func}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{'Длина':>8} | {'Время (мс)':>12} | {'Коллизии':>10} | {'Проверки':>10} | {'Найдено':>8}\n")
            f.write("-" * 50 + "\n")

            for row in measurements:
                pattern_len, time_ms, collisions, checks, found, position = row[1:]
                f.write(
                    f"{pattern_len:8d} | {time_ms:12.4f} | {collisions:10d} | {checks:10d} | {'Да' if found else 'Нет':>8}\n")

            f.write("-" * 50 + "\n")

            # Средние значения
            avg_time = sum(r[2] for r in measurements) / len(measurements)
            total_collisions = sum(r[3] for r in measurements)
            total_checks = sum(r[4] for r in measurements)

            f.write(
                f"Среднее время: {avg_time:.4f} мс | Всего коллизий: {total_collisions} | Всего проверок: {total_checks}\n\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("Данные сохранены в формате CSV для построения графиков\n")
    return filename


def create_time_metrics():
    ##############################################################
    # ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ

    # Длины паттернов для тестирования
    pattern_lengths = [1, 5, 10, 20, 50, 100, 150, 200, 300, 400, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000,4500,
                       5000,6000,8000,10000]

    # Хеш-функции с именами
    hash_functions = [
        ("linear_hash", linear_search),
        ("simple_hash", simple_hash),
        ("first_last_hash", first_last_hash),
        ("chetsum_hash", chetsum_hash),
        ("rolling_crc32", rolling_crc32),
        ("double_hash", double_hash),
    ]
    ##############################################################

    # Проверяем наличие файла
    path_to_file = f"texts/{time_file_name}"
    if not os.path.exists(path_to_file):
        print(f"Файл {path_to_file} не найден!")
        return

    # Загружаем текст
    text = load_text(path_to_file)
    if not text:
        print("Ошибка: не удалось загрузить текст")
        return

    print("=" * 70)
    print(f"Файл: {path_to_file}")
    print(f"Длина текста: {len(text)} символов")
    print("=" * 70 + "\n")

    # Данные для CSV
    csv_data = []


    # Основной цикл тестирования
    for pattern_len in pattern_lengths:
        # Берем паттерн из текста (не с начала, чтобы избежать заголовков)
        start_pos = 1000  # начинаем с 1000-го символа
        if start_pos + pattern_len > len(text):
            print(f"Пропускаем паттерн {pattern_len} символов: выходит за пределы текста")
            continue

        pattern = text[start_pos:start_pos + pattern_len]

        for hash_name, hash_func in hash_functions:

            # Создаем алгоритм
            algorithm = RabinKarp(hash_func, hash_name=hash_name)

            # Запускаем поиск
            position = algorithm.find(pattern, text)

            # Получаем статистику
            stats = algorithm.get_stats()

            # Сохраняем данные для CSV
            csv_data.append([
                hash_name,
                pattern_len,
                stats['time_ms'],
                stats['collisions'],
                stats['checks'],
                position != -1,
                position
            ])

    # Сохраняем данные
    if csv_data:
        csv_filename = save_to_csv(csv_data)
        txt_filename = save_summary_to_txt(csv_data)

        print(f"Текстовая сводка сохранена в: {txt_filename}")
        print(f"CSV данные для графиков: {csv_filename}")

        # Группируем по функциям для сводки
        hash_results = {}
        for row in csv_data:
            hash_name = row[0]
            if hash_name not in hash_results:
                hash_results[hash_name] = []
            hash_results[hash_name].append(row)

        # Выводим лучшую функцию по времени
        fastest_func = None
        fastest_avg = float('inf')

        for hash_name, measurements in hash_results.items():
            avg_time = sum(r[2] for r in measurements) / len(measurements)
            total_collisions = sum(r[3] for r in measurements)

            if avg_time < fastest_avg:
                fastest_avg = avg_time
                fastest_func = hash_name

    else:
        print("Ошибка: не собраны данные для сохранения")

    print("РАБОТА ПО СОЗДАНИЮ МЕТРИК ОКОНЧЕНА УСПЕШНО")