from typing import Callable
from collections import defaultdict
from core.exceptions import AlgorithmError

class FalsePositionMethod:

    @staticmethod
    def compute(f:Callable[[float], float], xl:float, xu:float, tol:float):
        iter_count = 0
        table = defaultdict(list)
        root = None

        try:

            MAX_ITERATION = 100

            if f(xl) * f(xu) > 0:
                raise AlgorithmError("El intervalo no contiene una raíz.")

            while(abs(xl - xu) > tol and iter_count < MAX_ITERATION):

                iter_count += 1

                f_xu, f_xl = f(xu), f(xl)

                xr = xu - ((f_xu * (xl - xu))) / (f_xl - f_xu)
                f_xr = f(xr)

                table["Extremo inferior (Xl)"].append(xl)
                table["Extremo superior (Xu)"].append(xu)
                table["Punto medio (Xr)"].append(xr)
                table["f(Xl)"].append(f_xl)
                table["f(Xu)"].append(f_xu)
                table["f(Xr)"].append(f_xr)
                table["f(Xl)*f(Xr)"].append(f_xl*f_xr)
                table["Error: |Xl - Xu|"].append(abs(xl - xu))

                root = xr

                if f_xr == 0:
                    break
                elif f(xr)*f(xl) < 0:
                    xu = xr
                else:
                    xl = xr


        except AlgorithmError as e:
            raise AlgorithmError("El intervalo no contiene una raíz.") from e

        return table, root, iter_count