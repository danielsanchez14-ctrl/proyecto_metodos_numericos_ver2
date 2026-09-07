import numpy as np
import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler
from core.single_variable_parser import SingleVariableParser
from core.methods.newton_raphson_optimization_method import NewtonRaphsonOptimizationMethod
from utils.plotter import Plotter


class NewtonRaphsonOptimizationHandler(MethodHandler):

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

        # 2. Convertir texto de función a algo evaluable, y calcular primera y segunda derivada
        parser = SingleVariableParser()
        expression, variable = parser.to_symbolic_expression(texto_f)

        derivative_expr = parser.derivative(expression, variable)          # n=1 por defecto
        second_derivative_expr = parser.derivative(expression, variable, n=2)

        f = parser.to_python_function(expression, variable)
        df = parser.to_python_function(derivative_expr, variable)
        df2 = parser.to_python_function(second_derivative_expr, variable)

        # 3. Ejecutar el algoritmo puro
        table, iterations, x_opt, f_opt, classification = NewtonRaphsonOptimizationMethod.compute(
            f, df, df2, x0, tol, num_iter
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
            result_x=x_opt,
            result_value=f_opt,
            classification=classification,
            function_fig=function_fig,
            error_fig=error_fig,
        )