from typing import Callable
from collections import defaultdict


class NewtonRaphsonOptimizationMethod:
    @staticmethod
    def compute(f: Callable[[float], float], df: Callable[[float], float],
                df2: Callable[[float], float], x0: float,
                tol: float = 0.0001, num_iter: int = 50000):
        MAX_ITER = num_iter
        table = defaultdict(list)
        iter_count = None

        for i in range(1, MAX_ITER + 1):
            x1 = x0 - df(x0) / df2(x0)
            table["X0"].append(x0)
            table["X1"].append(x1)
            error = abs(x1 - x0)
            x0 = x1
            table["Error : |X0 - X1|"].append(error)
            iter_count = i
            if error <= tol:
                break

        acceptance_range = 1e-7
        delta = 1e-4
        d_f2 = df2(x1)

        classification = None

        # Criterio de la segunda derivada
        if d_f2 > acceptance_range:
            classification = "MÍNIMO LOCAL"
        elif d_f2 < -acceptance_range:
            classification = "MÁXIMO LOCAL"
        else:
            # Segunda derivada ≈ 0: reintentar con criterio de la primera derivada
            d_f1_left = df(x0 - delta)
            d_f1_right = df(x0 + delta)

            if d_f1_left < -acceptance_range and d_f1_right > acceptance_range:
                classification = "MÍNIMO LOCAL"
            elif d_f1_left > acceptance_range and d_f1_right < -acceptance_range:
                classification = "MÁXIMO LOCAL"
            else:
                classification = "NO SE PUEDE DETERMINAR"

        return table, iter_count, x1, f(x1), classification