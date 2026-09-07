import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameView:
    """
    Encapsula un ``ttk.Treeview`` para mostrar un ``DataFrame`` de pandas.

    Esta vista se ocupa de transformar las columnas y filas del DataFrame en
    elementos visuales de Tkinter. También administra las barras de
    desplazamiento y reemplaza la tabla anterior cuando se muestran nuevos
    resultados.
    """
    def __init__(self, parent:tk.Widget):
        """
        Inicializa las referencias de la vista sin crear todavía una tabla.

        :param parent: Widget de Tkinter que contendrá la tabla y sus barras
            de desplazamiento.
        """
        self.parent = parent
        self.table_container = None
        self.tree = None
        self.scroll_y = None
        self.scroll_x = None

    def show(self, df:pd.DataFrame):
        """
        Renderiza un DataFrame en un Treeview nuevo.

        :param df: DataFrame cuyos nombres de columnas se usarán como
            encabezados y cuyas filas se insertarán en la tabla.

        Si ya existía una tabla, se destruye primero para evitar mostrar datos
        antiguos. Luego se crean el Treeview, los scrollbars, sus conexiones
        y una fila visual por cada registro del DataFrame.
        """

        # Eliminar la tabla anterior completa
        if self.table_container is not None:
            self.table_container.destroy()

        # Crear el contenedor de la tabla
        self.table_container = tk.Frame(self.parent)
        self.table_container.pack(
            fill="both",
            expand=True
        )

        # Crear el TreeView
        self.tree = ttk.Treeview(
            self.table_container,
            columns=list(df.columns),
            show="headings"
        )
        # Scroll vertical
        self.scroll_y = ttk.Scrollbar(
            self.table_container,
            orient="vertical",
            command=self.tree.yview
        )

        # Scroll horizontal
        self.scroll_x = ttk.Scrollbar(
            self.table_container,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        # Configurar las columnas
        for col in df.columns:
            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=100,
                anchor="center"
            )

        # Insertar filas
        for _, row in df.iterrows():

            self.tree.insert(
                "",
                "end",
                values=list(row)
            )

        
        # Posicionar Treeview
        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Scroll vertical
        self.scroll_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # Scroll horizontal
        self.scroll_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # Permitir que el Treeview ocupe todo el espacio
        self.table_container.rowconfigure(
            0,
            weight=1
        )

        self.table_container.columnconfigure(
            0,
            weight=1
        )


    def clear(self):
        """
        Elimina la tabla y reinicia sus referencias.

        No recibe parámetros ni devuelve valores. Si no existe una tabla,
        simplemente no realiza ninguna operación.
        """

        if self.table_container is not None:
            self.table_container.destroy()

            self.table_container = None
            self.tree = None
            self.scroll_y = None
            self.scroll_x = None