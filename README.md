# Métodos Numéricos

Aplicación de escritorio para ejecutar métodos numéricos y visualizar sus resultados mediante una interfaz gráfica construida con Tkinter.

## Estructura del proyecto

```text
.
├── main.py
├── README.md
├── core/
│   ├── dto.py
│   ├── exceptions.py
│   ├── method_manager.py
│   ├── single_variable_parser.py
│   ├── two_variable_parser.py
│   ├── abstract_classes/
│   │   ├── method_handler.py
│   │   └── parser.py
│   ├── handlers/
│   │   ├── bisection_handler.py
│   │   ├── false_position_handler.py
│   │   ├── golden_section_handler.py
│   │   ├── newton_raphson_optimization_handler.py
│   │   ├── newton_raphson_roots_handler.py
│   │   ├── quadratic_interpolation_handler.py
│   │   └── random_search_handler.py
│   └── methods/
│       ├── bisection_method.py
│       ├── false_position_method.py
│       ├── golden_section_method.py
│       ├── newton_raphson_optimization_method.py
│       ├── newton_raphson_roots_method.py
│       ├── quadratic_interpolation_method.py
│       └── random_search_method.py
├── gui/
│   ├── canvas_manager.py
│   ├── data_frame_view.py
│   ├── dynamic_form.py
│   ├── input_validator.py
│   └── main_window.py
└── utils/
    ├── plotter.py
    └── two_variable_plotter.py
```

## Descripción de los módulos

- `main.py`: punto de entrada de la aplicación.
- `core/`: lógica principal de los métodos numéricos, parsers y objetos compartidos.
- `core/methods/`: implementaciones de los algoritmos numéricos.
- `core/handlers/`: adaptadores que conectan cada algoritmo con la interfaz y sus parámetros.
- `core/abstract_classes/`: clases base para handlers y parsers.
- `core/single_variable_parser.py`: parser para funciones de una variable.
- `core/two_variable_parser.py`: parser para funciones de dos variables.
- `core/method_manager.py`: registro y selección de los métodos disponibles.
- `gui/`: ventana principal, formularios, validaciones, tablas y visualización de resultados.
- `utils/plotter.py`: generación de gráficas para variables simples.
- `utils/two_variable_plotter.py`: generación de gráficas para funciones de dos variables.

## Métodos disponibles

- Bisección
- Falsa posición
- Sección dorada
- Interpolación cuadrática
- Newton-Raphson para raíces
- Newton-Raphson para optimización
- Búsqueda aleatoria
- Soporte para funciones de dos variables en la lógica de visualización y parsing

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python main.py
```
