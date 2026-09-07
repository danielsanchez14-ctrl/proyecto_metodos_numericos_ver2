import numpy as np
import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler

from core.single_variable_parser import SingleVariableParser
from core.methods.false_position_method import FalsePositionMethod
from utils.plotter import Plotter


class FalsePositionHandler(MethodHandler):

    def get_parameters(self) -> list[ParamSpec]:
        return [
            ParamSpec(name="f", label="f(x)", type="text"),
            ParamSpec(name="xl", label="Extremo inferior (xl)", type="float"),
            ParamSpec(name="xu", label="Extremo superior (xu)", type="float"),
            ParamSpec(name="tol", label="Tolerancia", type="float", default="0.0001"),
        ]

    def execute(self, raw_values: dict[str, str]) -> MethodResult:
        # 1. Leer y convertir valores
        texto_f = raw_values["f"]
        xl = float(raw_values["xl"])
        xu = float(raw_values["xu"])
        tol = float(raw_values["tol"])

        # 2. Convertir texto de función a algo evaluable
        parser = SingleVariableParser()
        expression, variable = parser.to_symbolic_expression(texto_f)
        f = parser.to_python_function(expression, variable)

        # 3. Ejecutar el algoritmo puro
        table, root, iterations = FalsePositionMethod.compute(f, xl, xu, tol)
        df = pd.DataFrame(table)

        # 4. Generar gráfica de la función
        x_vals = np.linspace(xl, xu, 1000)
        y_vals = [f(x) for x in x_vals]
        function_fig = Plotter.plot_function(
            x_vals, y_vals, "Gráfica de la función", "x", "f(x)", texto_f
        )

        # 5. Generar gráfica de error (Falsa posición solo tiene esta columna)
        error_col = "Error: |Xl - Xu|"
        error_fig = Plotter.plot_function(
            list(range(iterations)), table[error_col],
            f"Evolución del {error_col}", "Núm. de iteración", "Error", error_col
        )

        # 6. Empaquetar en el DTO
        return MethodResult(
            table=df,
            iterations=iterations,
            result_x=root,
            function_fig=function_fig,
            error_fig=error_fig,
        )