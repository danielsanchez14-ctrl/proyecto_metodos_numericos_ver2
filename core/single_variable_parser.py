from core.abstract_classes.parser import Parser
from core.exceptions import ParserError
import sympy as sp
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
import tokenize


class SingleVariableParser(Parser):
    """
    Convierte texto como "x**2 - 4" en una función Python evaluable,
    y permite obtener derivadas simbólicas (necesario para Newton-Raphson).
    """

    def to_symbolic_expression(self, f:str):
        """Convierte el string a una expresión de SymPy y detecta la variable."""

        try:
            MATH_CONSTANTS = {"e": sp.E, "pi": sp.pi}
            # Aplica transformaciones para el parseo del string a expresión simbólica
            transformations = standard_transformations + (implicit_multiplication_application,)
            #Parsear string a expresión
            # Reemplaza 'e' sola (la constante) por 'E' de SymPy antes de parsear, lo mismo con pi
            expression = sp.parse_expr(f, local_dict=MATH_CONSTANTS, transformations=transformations)
            #Obtener la variable independiente
            free_vars = list(expression.free_symbols)
            if len(free_vars) == 0:
                # Caso función constante
                variable = sp.symbols('x')
            else:
                variable = free_vars[0]

            return expression, [variable]
        except (sp.SympifyError, SyntaxError, TypeError, tokenize.TokenizeError) as e:
            raise ParserError(f"No se pudo interpretar la función '{f}': revisa la sintaxis.") from e

    def to_python_function(self, f, variable_list):
        """Convierte una expresión simbólica en una función Python evaluable."""
        return sp.lambdify(variable_list, f)

    def derivative(self, expression, variable, n:int = 1):
        """Deriva la expresión respecto a su variable (necesario para Newton-Raphson)."""
        return sp.diff(expression, variable[0], n)