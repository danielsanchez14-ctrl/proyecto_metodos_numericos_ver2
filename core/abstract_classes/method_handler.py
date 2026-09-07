from abc import ABC, abstractmethod
from core.dto import ParamSpec, MethodResult

class MethodHandler(ABC):
    """
    Contrato que debe cumplir cada método numérico (equivalente a una
    interfaz de Java). MainWindow solo conoce estas dos operaciones —
    nunca sabe cómo funciona el algoritmo por dentro.
    """

    @abstractmethod
    def get_parameters(self) -> list[ParamSpec]:
        """Qué campos debe mostrar el formulario para este método (los parámetros que necesita el algoritmo)."""
        pass

    @abstractmethod
    def execute(self, raw_values:dict[str, str]) -> MethodResult:
        """Dado lo que escribió el usuario (como texto), calcula y devuelve el resultado."""
        pass