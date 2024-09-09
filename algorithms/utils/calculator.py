from math import sqrt


class Calculator:
    @staticmethod
    def euclidean_distance(point_a: tuple[int, int], point_b: tuple[int, int]) -> float:
        return sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)

    @staticmethod
    def calculate_path_length(distance_matrix: list[list[float]], indices: list[int]) -> float:
        total_distance = 0
        for i in range(len(indices) - 1):
            total_distance += distance_matrix[indices[i]][indices[i + 1]]
        return total_distance

    @staticmethod
    def calculate_distance_matrix(points: list[tuple[int, int]]) -> list[list[float]]:
        return [[Calculator.euclidean_distance(point_a, point_b) for point_b in points] for point_a in points]
