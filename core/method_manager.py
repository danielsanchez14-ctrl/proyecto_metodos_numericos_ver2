from core.handlers.bisection_handler import BisectionHandler
from core.handlers.golden_section_handler import GoldenSectionHandler
from core.handlers.false_position_handler import FalsePositionHandler
from core.handlers.quadratic_interpolation_handler import QuadraticInterpolationHandler
from core.handlers.newton_raphson_roots_handler import NewtonRaphsonRootsHandler
from core.handlers.newton_raphson_optimization_handler import NewtonRaphsonOptimizationHandler
from core.handlers.random_search_handler import RandomSearchHandler


from core.abstract_classes.method_handler import MethodHandler



class MethodManager:
    """
    Registro de métodos disponibles. Mapea el nombre visible en el
    Combobox con la clase Handler que sabe ejecutarlo.
    """

    METHODS = {
        "Bisección": BisectionHandler,
        "Falsa posición": FalsePositionHandler,
        "Sección dorada": GoldenSectionHandler,
        "Interpolación cuadrática": QuadraticInterpolationHandler,
        "Newton-Raphson (raíces)": NewtonRaphsonRootsHandler,
        "Newton-Raphson (optimización)": NewtonRaphsonOptimizationHandler,
        "Búsqueda aleatoria": RandomSearchHandler,
    }

    @classmethod
    def get_method_names(cls) -> list[str]:
        """Nombres para llenar el Combobox."""
        return list(cls.METHODS.keys())

    @classmethod
    def get_handler(cls, method_name: str) -> MethodHandler:
        """Instancia y devuelve el Handler correspondiente al método elegido."""
        handler_class = cls.METHODS[method_name]
        return handler_class()