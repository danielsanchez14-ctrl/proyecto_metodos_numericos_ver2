from dataclasses import dataclass
import pandas as pd
from typing import Optional, Union
from matplotlib.figure import Figure

@dataclass
class ParamSpec:
    """
        Describe un campo del formulario: nombre interno, texto visible y tipo
    """

    name:str
    label:str
    type:str #"text o float"
    default: str = ""

@dataclass
class MethodResult:
    """
    Resultado uniforme para cualquier método numérico. Campos opcionales
    según la categoría del método:

    - Búsqueda de raíces (Bisección, Falsa posición, Newton-raíces):
      solo usan 'result_x'. Los demás quedan en None.

    - Optimización dirigida (Sección dorada, Interpolación cuadrática):
      usan 'result_x', 'result_value' y 'is_maximization' (esto último
      lo decide el usuario al ingresar los datos, no el algoritmo).

    - Optimización con clasificación automática (Newton-Raphson optimización):
      usan 'result_x', 'result_value' y 'classification' (esto lo calcula
      el propio algoritmo a partir de la segunda/primera derivada).
    """
    table: pd.DataFrame
    iterations: int
    result_x: Union[float, tuple[float, float]]
    function_fig: Figure
    error_fig: Figure
    result_value: Optional[float] = None
    is_maximization: Optional[bool] = None
    classification: Optional[str] = None