import time

from results.checks.checks_graph_data import create_checks_metrics
from results.collizion.collizion_graph_data import create_collision_metrics
from results.time.time_graph_data import create_time_metrics
from results.graphics import create_time_graphs, create_collizion_graphs, create_checks_graphs


def main():

    create_time_metrics()
    time.sleep(2)
    create_time_graphs()

    time.sleep(1)

    create_collision_metrics()
    time.sleep(2)
    create_collizion_graphs()

    time.sleep(1)

    create_checks_metrics()
    time.sleep(2)
    create_checks_graphs()



if __name__ == "__main__":
    main()
