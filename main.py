import argparse

from algorithms.ant_algorithm import ACO
from algorithms.genetic_algorithm import GA
from visualise import Visualiser, generate_problem


def main(n, m, total_n, total_m):
    points = generate_problem(total_n, total_m)

    paths = []

    aco = ACO(200, 50, 1.5, 1.2, 0.6, 10, n, m, total_n, total_m)
    paths.append(aco.run(points=points, name='ACO'))
    aco1 = GA(100, 30, 1.5, 1.2, n, m, total_n, total_m)
    paths.append(aco1.run(points=points, name='GA'))

    Visualiser(points, n, m, path=paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Решение задачи коммивояжера с ограничениями.")
    parser.add_argument('-n', '--n', type=int, default=2,
                        help='Количество городов первого типа для посещения (по умолчанию 2)')
    parser.add_argument('-m', '--m', type=int, default=3,
                        help='Количество городов второго типа для посещения (по умолчанию 3)')
    parser.add_argument('-N', '--N', type=int, default=4, help='Общее количество городов первого типа (по умолчанию 4)')
    parser.add_argument('-M', '--M', type=int, default=5, help='Общее количество городов второго типа (по умолчанию 5)')

    args = parser.parse_args()

    main(args.n, args.m, args.N, args.M)
