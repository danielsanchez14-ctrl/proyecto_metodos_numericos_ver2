from typing import Callable
from collections import defaultdict
import random

class RandomSearchMethod:
    @staticmethod
    def compute(f : Callable[[float, float], float], points_x: tuple[float, float], points_y:tuple[float, float], maximize : bool = True, tol : float = 0.0001):
        # Desempaquetar puntos en x y en y
        xl, xu = points_x
        yl, yu = points_y

        critical_point_f = float('-inf') if maximize else float('inf')

        if maximize:
            compare = lambda new, best : new > best
        else:
            compare = lambda new, best : new < best

        table = defaultdict(list)
        error = None
        optimal_x, optimal_y = None, None

        MAX_ITER = 500000
        for i in range(MAX_ITER):
            x_random = xl + (xu - xl)*random.random()
            y_random = yl + (yu - yl)*random.random()

            f_n = f(x_random, y_random)
            previous_best = critical_point_f

            improved = compare(f_n, previous_best)
            if improved:
                critical_point_f = f_n
                optimal_x = x_random
                optimal_y = y_random

            # Cálculo del error: distancia entre el mejor punto hasta el momento y la iteración actual
            error = abs(f_n - critical_point_f)
            table["x"].append(x_random)
            table["y"].append(y_random)
            table["f(x,y)"].append(f_n)
            table["mejor"].append(critical_point_f)
            table["error"].append(error)

            if improved and previous_best not in (float('-inf'), float('inf')):
                stop_error = abs(critical_point_f - previous_best)
                if stop_error < tol:
                    break

        return optimal_x, optimal_y, critical_point_f, table, i + 1
    



            