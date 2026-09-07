class ParserError(Exception):
    """Error al interpretar la expresión matemática ingresada por el usuario."""
    pass


class ValidationError(Exception):
    """Error de formato en los datos ingresados (antes de llegar al algoritmo)."""
    pass


class AlgorithmError(Exception):
    """Error de una regla matemática del método (ej. intervalo sin raíz)."""
    pass