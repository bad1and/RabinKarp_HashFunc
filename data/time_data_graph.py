import sys
import os


from src.rabin_karp import RabinKarp
from src.hash_simple import simple_hash
from src.weighted_hash import weighted_sum_hash
from src.polynomial_hash import polynomial_hash
from src.lite_crc32 import rolling_crc32
from src.double_hash import double_hash

def load_text(filepath: str) -> str:
    """Загружает текст из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Пробуем другую кодировку если UTF-8 не работает
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()

def time_data_graph():

    ##############################################################
    #TODO: ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ

    file_name = "alice.txt"

    text = load_text(f"texts/{file_name}")
    patterns = [
        text[:1],  # первый символ текста
        text[:5],  # первые 5 символов
        text[:10],  # первые 10 символов
        text[:20],  # первые 20 символов
        text[:50],
        text[:100],
        text[:150],
        text[:200],# первые 50 символов
    ]

    hash_types = [
        simple_hash,
        weighted_sum_hash,
        polynomial_hash,
        rolling_crc32,
        double_hash,
    ]

    # TODO: ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ
    ##############################################################

    # Проверяем наличие тестового файла
    path_to_file = f"texts/{file_name}"
    if not os.path.exists(path_to_file):
        print(f"Файл {path_to_file} не найден!")
        return

    # Загружаем текст
    text = load_text(path_to_file)
    if not text:
        print("Ошибка: не удалось загрузить текст")
        return
    print(f"Файл: {path_to_file}")


    # Открываем файл для записи результатов
    with open("results/results.txt", "w", encoding="utf-8") as result_file:
        result_file.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ\n\n")

        result_file.write(f"Текст: {path_to_file}\n")
        result_file.write(f"Длина текста: {len(text)} символов\n")
        result_file.write("=" * 60 + "\n\n")


        for hash_type in hash_types:
            result_file.write(f"\nХеш-функция: {hash_type.__name__}\n\n")
            for pattern in patterns:

                # Создаём экземпляр алгоритма с простой хеш-функцией
                algorithm = RabinKarp(hash_type)

                # Запускаем поиск
                position = algorithm.find(pattern, text)

                # Получаем статистику
                stats = algorithm.get_stats()

                # Записываем в файл
                result_file.write(f"Длина паттерна: {len(pattern)}\n")
                result_file.write(f"  Найдено: {'Да' if position != -1 else 'Нет'}\n")
                result_file.write(f"  Коллизии: {stats['collisions']}\n")
                result_file.write(f"  Проверки: {stats['checks']}\n")
                result_file.write(f"  Время: {stats['time_ms']:.4f} мс\n")
                result_file.write("-" * 40 + "\n")
            result_file.write("\n" + "=" * 60)


    print("\n" + "=" * 60)
    print(f"Результаты сохранены в файл: results.txt")
    print("=" * 60)