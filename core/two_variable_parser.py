from core.abstract_classes.parser import Parser
from core.exceptions import ParserError
import sympy as sp
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
import tokenize


class TwoVariableParser(Parser):
    """
    Convierte texto como "x**2 + y**2" en una función Python evaluable
    de dos variables, y permite obtener derivadas parciales.
    """

    def to_symbolic_expression(self, f: str):
        """Convierte el string a una expresión de SymPy y detecta sus 2 variables."""
        try:
            MATH_CONSTANTS = {"e": sp.E, "pi": sp.pi}
            transformations = standard_transformations + (implicit_multiplication_application,)
            expression = sp.parse_expr(f, local_dict=MATH_CONSTANTS, transformations=transformations)

            # Ordenamos alfabéticamente para que el orden sea siempre predecible:
            # variable[0] será 'x', variable[1] será 'y' (o el orden alfabético
            # que corresponda), sin importar el orden en que SymPy las detecte.
            free_vars = sorted(expression.free_symbols, key=lambda s: s.name)

            if len(free_vars) != 2:
                raise ParserError(
                    f"La función '{f}' debe depender de exactamente 2 variables "
                    f"(se encontraron {len(free_vars)})."
                )

            return expression, free_vars
        except (sp.SympifyError, SyntaxError, TypeError, tokenize.TokenizeError) as e:
            raise ParserError(f"No se pudo interpretar la función '{f}': revisa la sintaxis.") from e

    def to_python_function(self, f, variable_list):
        """Convierte una expresión simbólica en una función Python evaluable de 2 argumentos."""
        return sp.lambdify(variable_list, f)
