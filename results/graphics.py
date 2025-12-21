import pandas as pd
import matplotlib.pyplot as plt
import os

from results.checks.checks_graph_data import checks_file_name
from results.time.time_graph_data import time_file_name
from results.collizion.collizion_graph_data import collizion_file_name



def create_time_graphs(csv_file=f"results/time/time_graph_data_{time_file_name[:5]}.csv"):
    """Создает все 3 графика из CSV файла"""

    # Загружаем данные
    df = pd.read_csv(csv_file)

    # 1. ГРАФИК ВРЕМЕНИ РАБОТЫ
    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'chetsum_hash': 'green',
              'first_last_hash': 'red',
              'rolling_crc32': 'purple',
              'double_hash': 'orange'}

    for hash_func in df['hash_function'].unique():
        subset = df[df['hash_function'] == hash_func]
        plt.plot(subset['pattern_length'], subset['time_ms'],
                 marker='o',
                 label=hash_func,
                 color=colors.get(hash_func, 'black'),
                 linewidth=2.5,
                 markersize=8)

    plt.xlabel("Длина паттерна (символы)", fontsize=14)
    plt.ylabel("Время работы (миллисекунды)", fontsize=14)
    plt.title("График 1: Влияние хеш-функции на время поиска",
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.xscale('linear')
    plt.yscale('linear')
    plt.tight_layout()
    plt.savefig(f"results/time/time_graph_data_{time_file_name[:5]}.png", dpi=300)
    print("TIME GRAPH СОЗДАН")
    return df

def create_collizion_graphs(csv_file=f"results/collizion/collision_graph_data_{collizion_file_name[:3]}.csv"):
    # 2. ГРАФИК КОЛЛИЗИЙ
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'chetsum_hash': 'green',
              'first_last_hash': 'red',
              'rolling_crc32': 'purple',
              'double_hash': 'orange'}

    for hash_func in df['hash_function'].unique():
        subset = df[df['hash_function'] == hash_func]
        plt.plot(subset['pattern_length'], subset['collisions'],
                 marker='s',
                 label=hash_func,
                 color=colors.get(hash_func, 'black'),
                 linewidth= 2.5,
                 markersize= 8)

    plt.xlabel("Длина паттерна (символы)", fontsize=14)
    plt.ylabel("Количество коллизий", fontsize=14)
    plt.title("График 2: Качество хеширования - количество коллизий",
              fontsize=16, fontweight='bold', pad=20)

    plt.xscale('linear')
    plt.yscale('linear')
    # plt.ylim(bottom=0.1)  # начинаем с 0.1 чтобы видеть нули на логарифмической шкале

    # Деления оси X (все значения длины паттерна)
    # plt.xticks(sorted(df['pattern_length'].unique()))

    plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    plt.grid(True, alpha=0.3)

    # # Добавляем горизонтальные линии для наглядности
    # for y in [1, 10, 100, 1000, 10000]:
    #     plt.axhline(y=y, color='gray', linestyle='--', alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"results/collizion/collizion_graph_data_{collizion_file_name[:3]}.png", dpi=300)
    plt.show()

    return df

def create_checks_graphs(csv_file=f"results/checks/checks_graph_data_{checks_file_name[:3]}.csv"):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'chetsum_hash': 'green',
              'first_last_hash': 'red',
              'rolling_crc32': 'purple',
              'double_hash': 'orange'}

    for hash_func in df['hash_function'].unique():
        subset = df[df['hash_function'] == hash_func]
        plt.plot(subset['pattern_length'], subset['checks'],
                 marker='s',
                 label=hash_func,
                 color=colors.get(hash_func, 'black'),
                 linewidth= 2.5,
                 markersize= 8)

    plt.xlabel("Длина паттерна (символы)", fontsize=14)
    plt.ylabel("Количество проверок", fontsize=14)
    plt.title("График 3: График проверок",
              fontsize=16, fontweight='bold', pad=20)

    plt.xscale('linear')
    plt.yscale('linear')
    # plt.ylim(bottom=0.1)  # начинаем с 0.1 чтобы видеть нули на логарифмической шкале

    # Деления оси X (все значения длины паттерна)
    # plt.xticks(sorted(df['pattern_length'].unique()))

    plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    plt.grid(True, alpha=0.3)

    # # Добавляем горизонтальные линии для наглядности
    # for y in [1, 10, 100, 1000, 10000]:
    #     plt.axhline(y=y, color='gray', linestyle='--', alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"results/checks/checks_graph_data_{checks_file_name[:3]}.png", dpi=300)
    plt.show()

    return df
