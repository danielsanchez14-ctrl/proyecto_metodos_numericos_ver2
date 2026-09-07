import tkinter as tk
from tkinter import ttk, messagebox

from core.method_manager import MethodManager
from gui.dynamic_form import DynamicForm
from gui.input_validator import InputValidator
from gui.canvas_manager import CanvasManager
from gui.data_frame_view import DataFrameView


class MainWindow:
    def __init__(self):
        self.root = tk.Tk() # Ventana principal
        self.root.title("Métodos Numéricos")
        self.root.geometry("900x700")

        self.validator = InputValidator() #Valida inputs
        self.current_handler = None # Manipula el algoritmo numérico que se necesite
        self.content = None
        self.method_var = None
        self.dynamic_form = None
        self.resultado_label = None


        self._build_scrollable_container() #Para envolver todo en un contenedor con scroll
        self._build_form() #Construye el formulario
        self._build_results_area() #Contenedor donde van la tabla y gráficas


    def _build_scrollable_container(self):
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Luego, todo el contenido real es un Frame dentro de canvas
        self.content = tk.Frame(canvas)
        content_window = canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(content_window, width=e.width)
        )

    def _build_form(self):
        form = tk.Frame(self.content)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Método:").pack(anchor="w")
        self.method_var = tk.StringVar()
        selector = ttk.Combobox(
            form,
            textvariable=self.method_var,
            values=MethodManager.get_method_names(),
            state="readonly"
        )

        selector.pack(fill="x")
        selector.bind("<<ComboboxSelected>>", self._on_method_selected)

        self.dynamic_form = DynamicForm(form)

        button = tk.Button(form, text="Ejecutar", command=self._on_ejecutar)
        button.pack(pady=10)

        self.resultado_label = tk.Label(form, text="", font=("Arial", 10, "bold"))
        self.resultado_label.pack()


    # ------------------------------------------------------------------
    # RESULTADOS: tabla + 2 gráficas, con altura fija para que se vean
    # completas al hacer scroll
    # ------------------------------------------------------------------
    def _build_results_area(self):
        table_frame = tk.Frame(self.content, height=250)
        table_frame.pack(fill="x", padx=10, pady=10)
        table_frame.pack_propagate(False)
        self.table_view = DataFrameView(table_frame)

        function_frame = tk.Frame(self.content, height=350)
        function_frame.pack(fill="x", padx=10, pady=10)
        function_frame.pack_propagate(False)
        self.function_canvas = CanvasManager(function_frame)

        error_frame = tk.Frame(self.content, height=350)
        error_frame.pack(fill="x", padx=10, pady=10)
        error_frame.pack_propagate(False)
        self.error_canvas = CanvasManager(error_frame)

    def _on_method_selected(self, event):
        method_name = self.method_var.get()
        self.current_handler = MethodManager.get_handler(method_name=method_name)
        self.dynamic_form.build(self.current_handler.get_parameters())

    def _on_ejecutar(self):
        if self.current_handler is None:
            messagebox.showerror("Error", "Selecciona un método antes de ejecutar.")
            return

        try:
            raw_values = self.dynamic_form.get_raw_values()
            self.validator.validate_all(self.current_handler.get_parameters(), raw_values=raw_values)

            resultado = self.current_handler.execute(raw_values=raw_values)

            self.resultado_label.config(text=self._build_summary_text(resultado=resultado))
            self.table_view.show(resultado.table)
            self.function_canvas.draw(resultado.function_fig)
            self.error_canvas.draw(resultado.error_fig)
        except ZeroDivisionError:
            messagebox.showerror("Error", "El método no pudo continuar: se produjo una división por cero. Prueba con otros valores iniciales.")
        except ValueError as e:
            if "math domain error" in str(e):
                messagebox.showerror("Error", "Revisa el intervalo ingresado: xl debe ser menor que xu.")
            else:
                messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def _build_summary_text(self, resultado) -> str:
        """
        Arma el texto de resumen según qué campos opcionales trae el resultado.
        Por ahora solo cubre búsqueda de raíces (Bisección, Falsa posición);
        se amplía cuando agreguemos métodos de optimización.
        """
        if resultado.classification is not None:
            return (f"{resultado.classification}: "
                f"(x={resultado.result_x:.6f}, f={resultado.result_value:.6f}) "
                f"— {resultado.iterations} iteraciones")
        elif resultado.result_value is not None:
            tipo = "Máximo" if resultado.is_maximization else "Mínimo"
            return (f"{tipo}: (x={resultado.result_x:.6f}, f={resultado.result_value:.6f}) "
                f"— {resultado.iterations} iteraciones")
        else:
            return f"Raíz: {resultado.result_x:.6f} ({resultado.iterations} iteraciones)"

    def run(self):
        self.root.mainloop()