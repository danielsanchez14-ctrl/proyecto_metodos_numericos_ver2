import numpy as np
import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler
from core.single_variable_parser import SingleVariableParser
from core.methods.quadratic_interpolation_method import QuadraticInterpolationMethod
from utils.plotter import Plotter


class QuadraticInterpolationHandler(MethodHandler):

    def get_parameters(self):
        return [
            ParamSpec(name="f", label="f(x)", type="text"),
            ParamSpec(name="x0", label="Punto x0", type="float"),
            ParamSpec(name="x1", label="Punto x1", type="float"),
            ParamSpec(name="x2", label="Punto x2", type="float"),
            ParamSpec(name="tol", label="Tolerancia", type="float", default="0.0001"),
            ParamSpec(name="maximize", label="¿Buscar máximo?", type="bool", default="True"),
        ]

    def execute(self, raw_values: dict[str, str]) -> MethodResult:
        # 1. Leer y convertir valores
        texto_f = raw_values["f"]
        x0 = float(raw_values["x0"])
        x1 = float(raw_values["x1"])
        x2 = float(raw_values["x2"])
        tol = float(raw_values["tol"])
        maximize = raw_values["maximize"].strip().lower() == "true"

        # 2. Convertir texto de función a algo evaluable
        parser = SingleVariableParser()
        expression, variable = parser.to_symbolic_expression(texto_f)
        f = parser.to_python_function(expression, variable)

        # 3. Ejecutar el algoritmo puro
        # Ojo con el orden real de retorno: (table, iter_count, xopt, fx)
        table, iterations, xopt, fx = QuadraticInterpolationMethod.compute(
            x0, x1, x2, f, maximize, tol
        )
        df = pd.DataFrame(table)

        # 4. Generar gráfica de la función
        margen = (x2 - x0) * 0.5
        x_vals = np.linspace(x0 - margen, x2 + margen, 1000)
        y_vals = [f(x) for x in x_vals]
        function_fig = Plotter.plot_function(
            x_vals, y_vals, "Gráfica de la función", "x", "f(x)", texto_f
        )

        # 5. Generar gráfica del error
        error_col = "Error : |X1 - X3|"
        error_fig = Plotter.plot_function(
            list(range(iterations)), table[error_col],
            f"Evolución del {error_col}", "Núm. de iteración", "Error", error_col
        )

        # 6. Empaquetar en el DTO
        return MethodResult(
            table=df,
            iterations=iterations,
            result_x=xopt,
            result_value=fx,
            is_maximization=maximize,
            function_fig=function_fig,
            error_fig=error_fig,
        )