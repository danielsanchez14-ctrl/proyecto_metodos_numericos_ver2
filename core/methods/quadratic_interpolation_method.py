from typing import Callable
from collections import defaultdict


class QuadraticInterpolationMethod:
    @staticmethod
    def compute(x0: float, x1: float, x2: float, f: Callable[[float], float],
                maximize: bool = True, tol: float = 0.001):
        table = defaultdict(list)

        f0, f1, f2 = f(x0), f(x1), f(x2)
        if not x0 < x1 < x2:
            raise ValueError("No se cumple: x0 < x1 < x2")

        if maximize and not (f1 > f0) and not (f1 > f2):
            raise ValueError("No se cumple: f(X1) > f(X2) Y f(X1) > f(X0)")
        elif not maximize and not (f1 < f0) and not (f1 < f2):
            raise ValueError("No se cumple: f(X1) < f(X2) Y f(X1) < f(X0)")

        is_best = lambda a, b: a > b if maximize else a < b

        MAX_ITER = 100
        iter_count = 0
        error = float("inf")

        while error > tol and iter_count <= MAX_ITER:
            x3 = (f0 * (x1**2 - x2**2) + f1 * (x2**2 - x0**2) + f2 * (x0**2 - x1**2)) / \
                 (2*f0*(x1 - x2) + 2*f1*(x2 - x0) + 2*f2*(x0 - x1))
            f3 = f(x3)
            error = abs(x1 - x3)

            table["X0"].append(x0); table["f(X0)"].append(f0)
            table["X1"].append(x1); table["f(X1)"].append(f1)
            table["X2"].append(x2); table["f(X2)"].append(f2)
            table["X3"].append(x3); table["f(X3)"].append(f3)
            table["Error : |X1 - X3|"].append(error)

            if x3 > x1:
                if is_best(f3, f1):
                    x0, x1 = x1, x3
                else:
                    x2 = x3
            else:
                if is_best(f3, f1):
                    x2, x1 = x1, x3
                else:
                    x0 = x3

            f0, f1, f2 = f(x0), f(x1), f(x2)
            iter_count += 1

        return table, iter_count, x3, f3