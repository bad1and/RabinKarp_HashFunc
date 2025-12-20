#!/usr/bin/env python3
import sys
import os


from src.rabin_karp import RabinKarp
from src.hash_simple import simple_hash


def load_text(filepath: str) -> str:
    """Загружает текст из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Пробуем другую кодировку если UTF-8 не работает
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def main():

    ##############################################################
    #TODO: ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ

    file_name = "test.txt"

    # Тестируем разные паттерны
    pattern = "алгоритм"

    hash_types = [
        simple_hash,
    ]

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
        result_file.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ\n")
        result_file.write("=" * 60 + "\n")
        result_file.write(f"Текст: {path_to_file}\n")
        result_file.write(f"Длина текста: {len(text)} символов\n")
        result_file.write(f"Паттерн: '{pattern}' (длина: {len(pattern)})\n")
        result_file.write("=" * 60 + "\n\n")


        for hash_type in hash_types:
            # Создаём экземпляр алгоритма с простой хеш-функцией
            algorithm = RabinKarp(hash_type)

            # Запускаем поиск
            position = algorithm.find(pattern, text)

            # Получаем статистику
            stats = algorithm.get_stats()

            # Записываем в файл
            result_file.write(f"Хеш-функция: {simple_hash.__name__}\n")
            result_file.write(f"  Найдено: {'Да' if position != -1 else 'Нет'}\n")
            result_file.write(f"  Позиция: {position}\n")
            result_file.write(f"  Коллизии: {stats['collisions']}\n")
            result_file.write(f"  Проверки: {stats['checks']}\n")
            result_file.write(f"  Время: {stats['time_ms']:.3f} мс\n")
            result_file.write("-" * 40 + "\n")

        # Итоговая статистика
        result_file.write("\n" + "=" * 60 + "\n")


    print("\n" + "=" * 60)
    print(f"Результаты сохранены в файл: results.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()