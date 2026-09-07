from core.exceptions import ValidationError
from core.dto import ParamSpec

class InputValidator:
    """
    Valida el formato de los valores crudos (strings) del formulario.
    No convierte tipos ni valida reglas matemáticas — solo verifica
    que el texto ingresado tenga el formato correcto según ParamSpec.type.
    """

    def validate(self, param_spec: ParamSpec, raw_value:str):
        """
            Verifica los tipos de un solo parámetro
            param_spec : objeto DTO de la clase ParamSpec, representa un parámetro y su meta data.
            raw_value : el dato ingresado en ese parámetro desde la interfaz
        """
        label = param_spec.label #La etiqueta visible
        param_type = param_spec.type #El tipo

        if raw_value is None or raw_value.strip() == "":
            raise ValidationError(f"El campo '{label}' no puede estar vacío.")

        if param_type == "float":
            try:
                float(raw_value)
            except ValueError:
                raise ValidationError(f"'{label}' debe ser debe ser un número (ej. 1.5, -3, 1e-6).")
        elif param_type == "int":
            try:
                int(raw_value)
            except ValueError:
                raise ValidationError(f"'{label}' debe ser un número entero.")
        elif param_type == "text":
            pass
        elif param_type == "bool":
            if raw_value.strip().lower() not in ("true", "false"):
                raise ValidationError(f"'{label}' debe ser True o False.")

    def validate_all(self, params_spec: list[ParamSpec], raw_values: dict[str, str]):
        for param_spec in params_spec:
            self.validate(param_spec=param_spec, raw_value=raw_values.get(param_spec.name))