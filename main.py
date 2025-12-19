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


def create_test_file():
    """Создаёт тестовый файл если его нет"""
    test_text = """Алгоритм Рабина — Карпа — это алгоритм поиска строки, 
который ищет шаблон, то есть подстроку, в тексте, используя хеширование.
Алгоритм был разработан в 1987 году Ричардом Рабином и Майклом Карпом.
Алгоритм лучше всего подходит для поиска нескольких шаблонов в тексте."""

    os.makedirs('texts', exist_ok=True)
    with open('texts/test.txt', 'w', encoding='utf-8') as f:
        f.write(test_text)

    print("Создан тестовый файл: texts/test.txt")


def main():

    # Проверяем наличие тестового файла
    test_file = "texts/test.txt"
    if not os.path.exists(test_file):
        print(f"Файл {test_file} не найден!")
        create_test_file()

    # Загружаем текст
    text = load_text(test_file)
    if not text:
        print("Ошибка: не удалось загрузить текст")
        return

    print("=" * 60)
    print("ТЕСТ АЛГОРИТМА РАБИНА-КАРПА")
    print("=" * 60)
    print(f"Длина текста: {len(text)} символов")
    print(f"Файл: {test_file}")
    print("-" * 60)

    # Создаём экземпляр алгоритма с простой хеш-функцией
    algorithm = RabinKarp(simple_hash)

    # Тестируем разные паттерны
    test_patterns = [
        "алгоритм",  # Должен найтись
        "хеширование",  # Должен найтись
        "abcdefgh",  # Не должен найтись
        "Алгоритм Рабина",  # Должен найтись
    ]

    # Открываем файл для записи результатов
    with open("results/results.txt", "w", encoding="utf-8") as result_file:
        result_file.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ\n")
        result_file.write("=" * 60 + "\n")
        result_file.write(f"Текст: {test_file}\n")
        result_file.write(f"Длина текста: {len(text)} символов\n")
        result_file.write("=" * 60 + "\n\n")

        for pattern in test_patterns:
            print(f"\nПоиск паттерна: '{pattern}'")
            print(f"Длина паттерна: {len(pattern)}")

            # Запускаем поиск
            position = algorithm.find(pattern, text)

            # Получаем статистику
            stats = algorithm.get_stats()

            # Выводим результат
            if position != -1:
                print(f"✓ Найдено на позиции: {position}")
            else:
                print("✗ Не найдено")

            print(f"  Коллизии: {stats['collisions']}")
            print(f"  Проверки: {stats['checks']}")
            print(f"  Время: {stats['time_ms']:.3f} мс")

            # Записываем в файл
            result_file.write(f"Паттерн: '{pattern}' (длина: {len(pattern)})\n")
            result_file.write(f"  Найдено: {'Да' if position != -1 else 'Нет'}\n")
            result_file.write(f"  Позиция: {position}\n")
            result_file.write(f"  Коллизии: {stats['collisions']}\n")
            result_file.write(f"  Проверки: {stats['checks']}\n")
            result_file.write(f"  Время: {stats['time_ms']:.3f} мс\n")
            result_file.write("-" * 40 + "\n")

        # Итоговая статистика
        result_file.write("\n" + "=" * 60 + "\n")
        result_file.write("Хеш-функция: simple_hash (сумма кодов символов)\n")
        result_file.write("Алгоритм: Рабина-Карпа (упрощённая версия)\n")

    print("\n" + "=" * 60)
    print(f"Результаты сохранены в файл: results.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()