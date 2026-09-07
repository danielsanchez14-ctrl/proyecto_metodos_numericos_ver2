import numpy as np
import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler
from core.single_variable_parser import SingleVariableParser
from core.methods.newton_raphson_roots_method import NewtonRaphsonRootsMethod
from utils.plotter import Plotter


class NewtonRaphsonRootsHandler(MethodHandler):

    def get_parameters(self):
        return [
            ParamSpec(name="f", label="f(x)", type="text"),
            ParamSpec(name="x0", label="Conjetura inicial (x0)", type="float"),
            ParamSpec(name="tol", label="Tolerancia", type="float", default="0.0001"),
            ParamSpec(name="num_iter", label="Máx. iteraciones", type="float", default="50000"),
        ]

    def execute(self, raw_values: dict[str, str]) -> MethodResult:
        # 1. Leer y convertir valores
        texto_f = raw_values["f"]
        x0 = float(raw_values["x0"])
        tol = float(raw_values["tol"])
        num_iter = int(float(raw_values["num_iter"]))

        # 2. Convertir texto de función a algo evaluable, y calcular su derivada
        parser = SingleVariableParser()
        expression, variable = parser.to_symbolic_expression(texto_f)
        derivative_expr = parser.derivative(expression, variable)

        f = parser.to_python_function(expression, variable)
        df = parser.to_python_function(derivative_expr, variable)

        # 3. Ejecutar el algoritmo puro
        table, iterations, root, f_root = NewtonRaphsonRootsMethod.compute(
            f, df, x0, tol, num_iter
        )
        table_df = pd.DataFrame(table)

        # 4. Generar gráfica de la función
        margen = 5.0
        x_vals = np.linspace(x0 - margen, x0 + margen, 1000)
        y_vals = [f(x) for x in x_vals]
        function_fig = Plotter.plot_function(
            x_vals, y_vals, "Gráfica de la función", "x", "f(x)", texto_f
        )

        # 5. Generar gráfica del error
        error_col = "Error : |X0 - X1|"
        error_fig = Plotter.plot_function(
            list(range(iterations)), table[error_col],
            f"Evolución del {error_col}", "Núm. de iteración", "Error", error_col
        )

        # 6. Empaquetar en el DTO
        return MethodResult(
            table=table_df,
            iterations=iterations,
            result_x=root,
            function_fig=function_fig,
            error_fig=error_fig,
        )