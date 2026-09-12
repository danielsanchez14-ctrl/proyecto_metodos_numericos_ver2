import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler
from core.two_variable_parser import TwoVariableParser
from core.methods.random_search_method import RandomSearchMethod
from utils.plotter import Plotter
from utils.two_variable_plotter import TwoVariablePlotter


class RandomSearchHandler(MethodHandler):

    def get_parameters(self):
        return [
            ParamSpec(name="f", label="f(x, y)", type="text"),
            ParamSpec(name="xl", label="x mínimo", type="float"),
            ParamSpec(name="xu", label="x máximo", type="float"),
            ParamSpec(name="yl", label="y mínimo", type="float"),
            ParamSpec(name="yu", label="y máximo", type="float"),
            ParamSpec(name="maximize", label="¿Buscar máximo?", type="bool", default="True"),
            ParamSpec(name="max_iter", label="Iteraciones", type="int", default="500000")
        ]

    def execute(self, raw_values: dict[str, str]) -> MethodResult:
        # 1. Leer y convertir valores
        texto_f = raw_values["f"]
        xl = float(raw_values["xl"])
        xu = float(raw_values["xu"])
        yl = float(raw_values["yl"])
        yu = float(raw_values["yu"])
        # tol = float(raw_values["tol"])
        maximize = raw_values["maximize"].strip().lower() == "true"
        iterations_default = int(raw_values["max_iter"])

        # 2. Convertir texto de función a algo evaluable (2 variables)
        parser = TwoVariableParser()
        expression, variables = parser.to_symbolic_expression(texto_f)
        f = parser.to_python_function(expression, variables)

        # 3. Ejecutar el algoritmo puro
        optimal_x, optimal_y, best_value, table, iterations = RandomSearchMethod.compute(
            f, (xl, xu), (yl, yu), maximize, iterations_default
        )
        df = pd.DataFrame(table)

        # 4. Generar gráfica de la función (mapa de contorno)
        function_fig = TwoVariablePlotter.plot_contour(
            (xl, xu), (yl, yu), f,
            "Mapa de la función f(x, y)", "x", "y",
            best_point=(optimal_x, optimal_y)
        )

        # 5. Generar gráfica de error
        error_fig = Plotter.plot_function(
            list(range(iterations)), table["error"],
            "Evolución del error", "Núm. de iteración", "Error : |punto calculado - mejor punto actual|", "error"
        )

        # 6. Empaquetar en el DTO — result_x es una tupla (x, y)
        return MethodResult(
            table=df,
            iterations=iterations,
            result_x=(optimal_x, optimal_y),
            result_value=best_value,
            is_maximization=maximize,
            function_fig=function_fig,
            error_fig=error_fig,
        )