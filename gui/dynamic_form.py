import tkinter as tk
from core.dto import ParamSpec
from tkinter import ttk

class DynamicForm:
    """
    Dibuja campos de entrada según una lista de ParamSpec.
    Se reconstruye cada vez que el usuario elige un método distinto.
    No valida ni convierte tipos, solo muestra campos y devuelve texto.
    """

    def __init__(self, parent:tk.Widget):
        self.fields_frame = tk.Frame(parent)
        self.fields_frame.pack(side="top", fill="x")
        self.vars: dict[str, tk.StringVar] = {}

    def build(self, parameters: list[ParamSpec]):
        # Borra los campos del método anterior
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.vars.clear()

        # crea un label (etiqueta) junto con una entrada (Entry) por parámetro
        for row, param in enumerate(parameters):
            tk.Label(self.fields_frame, text=param.label).grid(
                row = row, column=0, sticky="w", padx=5, pady=3)

            var = tk.StringVar(value=param.default)
            if param.type == "bool":
                widget = ttk.Combobox(
                self.fields_frame, textvariable=var,
                values=["True", "False"], state="readonly"
                )
            else:
                widget = tk.Entry(self.fields_frame, textvariable=var)

            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=3)

            self.vars[param.name] = var

        self.fields_frame.columnconfigure(1, weight=1)

    def get_raw_values(self) -> dict[str, str]:
        return {name: var.get() for name, var in self.vars.items()}
    