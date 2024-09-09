from random import randint

import plotly.graph_objects as go

from algorithms.utils.path import Path


def generate_problem(count_a: int, count_b: int, canvas_size: int = 1000) -> list[tuple[tuple[int, int], str]]:
    return [
        ((randint(0, canvas_size), randint(0, canvas_size)), 'a') for _ in range(count_a)
            ] + [
        ((randint(0, canvas_size), randint(0, canvas_size)), 'b') for _ in range(count_b)
    ]


class Visualiser:

    CLR_POINT = "#eb343a"
    CLR_PATH = [
        "#eb343a",
        "#db34eb",
        "#5b34eb",
        "#34b4eb",
        "#34eb4c",
        "#ebe534",
        "#eb9234",
    ]

    def __init__(self, points: list[tuple[tuple[int, int], str]], n, m, path: list[Path] = None) -> None:
        self.n = n
        self.m = m
        self.__points = points
        self.__path = path
        # self.__new_points = [points[x] for x in path.indexes] if path else None
        self.__fig = go.Figure()
        self.__show()

    def __draw_points(self) -> None:
        red_points = [x[0] for x in self.__points if x[1] == 'a']
        green_points = [x[0] for x in self.__points if x[1] == 'b']

        red_x, red_y = zip(*red_points)
        green_x, green_y = zip(*green_points)

        self.__fig.add_trace(go.Scatter(x=red_x, y=red_y, mode='markers', marker=dict(color='red'),
                                        name=f"Красные точки ({len(red_points)})"))
        self.__fig.add_trace(go.Scatter(x=green_x, y=green_y, mode='markers', marker=dict(color='green'),
                                        name=f"Зелёные точки ({len(green_points)})"))

        self.__add_annotations(red_points)
        self.__add_annotations(green_points)

    def __add_annotations(self, points):
        for i, p in enumerate(points):
            self.__fig.add_annotation(x=p[0], y=p[1], text=str(i + 1), showarrow=False, font=dict(size=8))
            self.__fig.add_annotation(x=p[0], y=p[1], text=f"({p[0]}; {p[1]})", showarrow=False, font=dict(size=6))

    def __draw_paths(self) -> None:
        if self.__path:
            paths = self.__path
            for i, path in enumerate(paths):
                points = [self.__points[i][0] for i in path.indexes]
                x, y = zip(*points)
                self.__fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers',
                                                line=dict(dash='dash', color=Visualiser.CLR_PATH[i]),
                                                name=f"{path.name} ({path.length:.2f})"))

    def __show(self) -> None:
        self.__draw_paths()
        self.__draw_points()

        self.__fig.update_layout(title="Подсказка: Нажмите на линии легенды, чтобы включить/выключить путь")
        self.__fig.show()
