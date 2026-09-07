from typing import Callable
from scipy import constants
from core.exceptions import AlgorithmError


class GoldenSectionMethod:
    @staticmethod
    def compute(xlow: float, xhigh: float, tol: float, f: Callable[[float], float],
                maximize: bool = True, maxit: int = 100):
        R = 1 / constants.golden_ratio
        table = {
            "Xl": [], "f(Xl)": [],
            "X2": [], "f(X2)": [],
            "X1": [], "f(X1)": [],
            "Xu": [], "f(Xu)": [],
            "d": [], "Error: |X1 - X2|": []
        }

        d = R * (xhigh - xlow)
        iter_count = 1

        x1, x2 = xlow + d, xhigh - d
        f_1, f_2 = f(x1), f(x2)

        best = lambda: (x1, f_1) if maximize == (f_1 > f_2) else (x2, f_2)
        xopt, fx = best()

        table["Xl"].append(xlow); table["f(Xl)"].append(f(xlow))
        table["X2"].append(x2); table["f(X2)"].append(f_2)
        table["X1"].append(x1); table["f(X1)"].append(f_1)
        table["Xu"].append(xhigh); table["f(Xu)"].append(f(xhigh))
        table["d"].append(d); table["Error: |X1 - X2|"].append(abs(x1 - x2))

        for _ in range(2, maxit + 1):
            d = R * d
            if (f_1 > f_2) == maximize:
                xlow = x2
                x2 = x1
                x1 = xlow + d
                f_2 = f_1
                f_1 = f(x1)
            else:
                xhigh = x1
                x1 = x2
                x2 = xhigh - d
                f_1 = f_2
                f_2 = f(x2)

            xopt, fx = best()
            error = abs(x1 - x2)

            table["Xl"].append(xlow); table["f(Xl)"].append(f(xlow))
            table["X2"].append(x2); table["f(X2)"].append(f_2)
            table["X1"].append(x1); table["f(X1)"].append(f_1)
            table["Xu"].append(xhigh); table["f(Xu)"].append(f(xhigh))
            table["d"].append(d); table["Error: |X1 - X2|"].append(error)

            iter_count += 1
            if error < tol:
                break

        return table, xopt, fx, iter_count