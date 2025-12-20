import pandas as pd
import matplotlib.pyplot as plt
import os


def create_all_graphs_from_csv(csv_file="results/alice_text/time_graph_data_alice.csv"):
    """Создает все 3 графика из CSV файла"""

    # Загружаем данные
    df = pd.read_csv(csv_file)

    # 1. ГРАФИК ВРЕМЕНИ РАБОТЫ
    plt.figure(figsize=(14, 8))

    colors = {'simple_hash': 'blue',
              'weighted_sum_hash': 'green',
              'polynomial_hash': 'red',
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
    plt.savefig("results/alice_text/01_time_vs_pattern_length.png", dpi=300)
    plt.show()

    # # 2. ГРАФИК КОЛЛИЗИЙ
    # plt.figure(figsize=(14, 8))
    #
    # for hash_func in df['hash_function'].unique():
    #     subset = df[df['hash_function'] == hash_func]
    #     plt.plot(subset['pattern_length'], subset['collisions'],
    #              marker='s',
    #              label=hash_func,
    #              color=colors.get(hash_func, 'black'),
    #              linewidth=2.5,
    #              markersize=8)
    #
    # plt.xlabel("Длина паттерна (символы)", fontsize=14)
    # plt.ylabel("Количество коллизий", fontsize=14)
    # plt.title("График 2: Качество хеширования - количество коллизий",
    #           fontsize=16, fontweight='bold', pad=20)
    # plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    # plt.grid(True, alpha=0.3)
    # plt.tight_layout()
    # plt.savefig("results/alice_text/02_collisions_vs_pattern_length.png", dpi=300)
    # plt.show()
    #
    # # 3. ГРАФИК ПРОВЕРОК
    # plt.figure(figsize=(14, 8))
    #
    # for hash_func in df['hash_function'].unique():
    #     subset = df[df['hash_function'] == hash_func]
    #     plt.plot(subset['pattern_length'], subset['checks'],
    #              marker='^',
    #              label=hash_func,
    #              color=colors.get(hash_func, 'black'),
    #              linewidth=2.5,
    #              markersize=8)
    #
    # plt.xlabel("Длина паттерна (символы)", fontsize=14)
    # plt.ylabel("Количество посимвольных проверок", fontsize=14)
    # plt.title("График 3: Эффективность поиска - количество проверок",
    #           fontsize=16, fontweight='bold', pad=20)
    # plt.legend(fontsize=12, title="Хеш-функции", title_fontsize=13)
    # plt.grid(True, alpha=0.3)
    # plt.tight_layout()
    # plt.savefig("results/alice_text/03_checks_vs_pattern_length.png", dpi=300)
    # plt.show()

    return df


# Использование:
if __name__ == "__main__":
    df = create_all_graphs_from_csv()