import matplotlib.pyplot as plt
import pandas as pd

from results.checks.checks_graph_data import checks_file_name
from results.collizion.collizion_graph_data import collizion_file_name
from results.time.time_graph_data import time_file_name


def create_time_graphs(csv_file=f"results/time/time_graph_data_{time_file_name[:-4]}.csv"):
    """Создает все 3 графика из CSV файла"""

    # Загружаем данные
    df = pd.read_csv(csv_file)

    # 1. ГРАФИК ВРЕМЕНИ РАБОТЫ
    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'chetsum_hash': 'green',
              'first_last_hash': 'red',
              'rolling_crc32': 'purple',
              'double_hash': 'orange',
              'linear_hash': 'black',
              }

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
    plt.title(f"Влияние хеш-функции на время  ({time_file_name})",
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.xscale('linear')
    plt.yscale('linear')
    plt.tight_layout()
    plt.savefig(f"results/time/time_graph_data_{time_file_name[:-4]}.png", dpi=300)
    print("TIME GRAPH СОЗДАН")
    return df


def create_collizion_graphs(csv_file=f"results/collizion/collision_graph_data_{collizion_file_name[:-4]}.csv"):
    # 2. ГРАФИК КОЛЛИЗИЙ
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'chetsum_hash': 'green',
              'first_last_hash': 'red',
              'rolling_crc32': 'purple',
              'double_hash': 'orange',
              'linear_hash': 'black',
              }

    for hash_func in df['hash_function'].unique():
        subset = df[df['hash_function'] == hash_func]
        plt.plot(subset['pattern_length'], subset['collisions'],
                 marker='s',
                 label=hash_func,
                 color=colors.get(hash_func, 'black'),
                 linewidth=2.5,
                 markersize=8)

    plt.xlabel("Длина паттерна (символы)", fontsize=14)
    plt.ylabel("Количество коллизий", fontsize=14)
    plt.title(f"Качество хеширования - количество коллизий ({collizion_file_name})",
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
    plt.savefig(f"results/collizion/collizion_graph_data_{collizion_file_name[:-4]}.png", dpi=300)
    # plt.show()

    return df


def create_checks_graphs(csv_file=f"results/checks/checks_graph_data_{checks_file_name[:-4]}.csv"):
    df = pd.read_csv(csv_file)

    fig, ax1 = plt.subplots(figsize=(14, 8))
    ax2 = ax1.twinx()  # Вторичная ось Y

    colors = {
        'simple_hash': 'blue',
        'chetsum_hash': 'green',
        'first_last_hash': 'red',
        'rolling_crc32': 'purple',
        'double_hash': 'orange',
        'linear_hash': 'black',
    }

    # Основные хеш-функции на ax1
    for hash_func in df['hash_function'].unique():
        if hash_func == 'linear_hash':
            continue

        subset = df[df['hash_function'] == hash_func]
        ax1.plot(subset['pattern_length'], subset['checks'],
                 marker='s',
                 label=hash_func,
                 color=colors.get(hash_func, 'black'),
                 linewidth=2.5,
                 markersize=8)

    # linear_hash на ax2
    linear_data = df[df['hash_function'] == 'linear_hash']
    if not linear_data.empty:
        ax2.plot(linear_data['pattern_length'], linear_data['checks'],
                 marker='o',
                 label='linear_hash (бейзлайн)',
                 color='black',
                 linewidth=3,
                 markersize=10,
                 linestyle='--')

    ax1.set_xlabel("Длина паттерна (символы)", fontsize=14)
    ax1.set_ylabel("Проверки (хеш-функции)", fontsize=14, color='blue')
    ax2.set_ylabel("Проверки (linear_hash)", fontsize=14, color='black')

    plt.title(f"График проверок ({checks_file_name})",
              fontsize=16, fontweight='bold', pad=20)

    # Объединяем легенды
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               fontsize=12, title="Хеш-функции", title_fontsize=13)

    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/checks/checks_graph_data_{checks_file_name[:-4]}.png", dpi=300)

    return df
