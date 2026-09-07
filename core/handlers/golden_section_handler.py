import numpy as np
import pandas as pd

from core.dto import ParamSpec, MethodResult
from core.abstract_classes.method_handler import MethodHandler
from core.single_variable_parser import SingleVariableParser
from core.methods.golden_section_method import GoldenSectionMethod
from utils.plotter import Plotter


class GoldenSectionHandler(MethodHandler):

    def get_parameters(self):
        return [
            ParamSpec(name="f", label="f(x)", type="text"),
            ParamSpec(name="xlow", label="Extremo inferior (xlow)", type="float"),
            ParamSpec(name="xhigh", label="Extremo superior (xhigh)", type="float"),
            ParamSpec(name="tol", label="Tolerancia", type="float", default="0.001"),
            ParamSpec(name="maximize", label="¿Buscar máximo?", type="bool", default="True"),
        ]

    def execute(self, raw_values: dict[str, str]) -> MethodResult:
        # 1. Leer y convertir valores
        texto_f = raw_values["f"]
        xlow = float(raw_values["xlow"])
        xhigh = float(raw_values["xhigh"])
        tol = float(raw_values["tol"])
        maximize = raw_values["maximize"].strip().lower() == "true"

        # 2. Convertir texto de función a algo evaluable
        parser = SingleVariableParser()
        expression, variable = parser.to_symbolic_expression(texto_f)
        f = parser.to_python_function(expression, variable)

        # 3. Ejecutar el algoritmo puro
        table, xopt, fx, iterations = GoldenSectionMethod.compute(
            xlow, xhigh, tol, f, maximize
        )
        df = pd.DataFrame(table)

        # 4. Generar gráfica de la función
        x_vals = np.linspace(xlow, xhigh, 1000)
        y_vals = [f(x) for x in x_vals]
        function_fig = Plotter.plot_function(
            x_vals, y_vals, "Gráfica de la función", "x", "f(x)", texto_f
        )

        # 5. Generar gráfica del error
        error_col = "Error: |X1 - X2|"
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