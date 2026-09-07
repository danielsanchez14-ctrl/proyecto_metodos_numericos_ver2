from typing import Callable
from collections import defaultdict


class NewtonRaphsonRootsMethod:
    @staticmethod
    def compute(f: Callable[[float], float], df: Callable[[float], float],
                x0: float, tol: float = 0.0001, num_iter: int = 50000):
        MAX_ITER = num_iter
        table = defaultdict(list)
        iter_count = None

        for i in range(1, MAX_ITER + 1):
            x1 = x0 - f(x0) / df(x0)
            table["X0"].append(x0)
            table["X1"].append(x1)
            error = abs(x1 - x0)
            x0 = x1
            table["Error : |X0 - X1|"].append(error)
            iter_count = i
            if error <= tol:
                break

        return table, iter_count, x1, f(x1)