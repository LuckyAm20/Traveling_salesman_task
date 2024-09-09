from math import inf
from random import random, shuffle

from .utils.calculator import Calculator
from .utils.path import Path


class ACO:
    def __init__(self, ants: int, iter: int, a: float, b: float, p: float, q: float, n, m, N, M) -> None:
        self.ants = ants
        self.iter = iter
        self.a = a
        self.b = b
        self.p = p
        self.q = q
        self.n = n
        self.m = m
        self.N = N
        self.M = M

    @staticmethod
    def __select_i(selection: list[int]) -> int:
        sum_num = sum(selection)
        if sum_num == 0:
            return len(selection) - 1
        tmp_num = random()
        prob = 0
        for i in range(len(selection)):
            prob += selection[i] / sum_num
            if prob >= tmp_num:
                return i

    def __create_indx(self, dm: list[list[float]], pm: list[list[float]]) -> list[int]:
        count_a = 0
        count_b = 0
        unvisited_indx = list(range(self.N + self.M))
        unvisited_a_cities = list(range(self.N))
        unvisited_b_cities = list(range(self.N, self.N + self.M))
        shuffle(unvisited_indx)
        visited_indx = [unvisited_indx.pop()]
        if visited_indx[0] in unvisited_b_cities:
            count_b += 1
        elif visited_indx[0] in unvisited_a_cities:
            count_a += 1
        for _ in range(self.n + self.m - 1):
            i = visited_indx[-1]
            selection = []

            if count_a == self.n:
                for el in unvisited_a_cities:
                    if el in unvisited_indx:
                        unvisited_indx.remove(el)
            if count_b == self.m:
                for el in unvisited_b_cities:
                    if el in unvisited_indx:
                        unvisited_indx.remove(el)

            for j in unvisited_indx:
                selection.append(
                    (pm[i][j] ** self.a) * ((1 / max(dm[i][j], 10**-5)) ** self.b)
                )
            selected_i = ACO.__select_i(selection)
            if unvisited_indx[selected_i] in unvisited_b_cities:
                count_b += 1
            elif unvisited_indx[selected_i] in unvisited_a_cities:
                count_a += 1

            visited_indx.append(unvisited_indx.pop(selected_i))
        visited_indx.append(visited_indx[0])
        return visited_indx

    def update_pm(self, pm: list[list[float]], tmp_indx: list[list[int]], tmp_leng: list[float]) -> None:
        l = len(pm)
        for i in range(l):
            for j in range(i, l):
                pm[i][j] *= 1 - self.p
                pm[j][i] *= 1 - self.p
        for i in range(self.ants):
            delta = self.q / tmp_leng[i]
            indx = tmp_indx[i]
            for j in range(len(indx) - 1):
                pm[indx[j]][indx[j + 1]] += delta
                pm[indx[j + 1]][indx[j]] += delta

    def run(self, points: list[tuple[tuple[int, int], str]], name: str = None) -> Path:
        l = len(points)
        dm = Calculator.calculate_distance_matrix([x[0] for x in points])
        pm = [[1 for _ in range(l)] for _ in range(l)]
        res_indx = []
        res_leng = inf
        for _ in range(self.iter):
            tmp_indx = []
            tmp_leng = []
            for _ in range(self.ants):
                indx = self.__create_indx(dm, pm)
                tmp_indx.append(indx)
                tmp_leng.append(Calculator.calculate_path_length(dm, indx))
            self.update_pm(pm, tmp_indx, tmp_leng)
            best_leng = min(tmp_leng)
            if best_leng < res_leng:
                res_leng = best_leng
                res_indx = tmp_indx[tmp_leng.index(best_leng)]
        return Path(indexes=res_indx, length=res_leng, name=name)
