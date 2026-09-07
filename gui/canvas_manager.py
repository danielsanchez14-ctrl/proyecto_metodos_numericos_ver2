from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CanvasManager:
    """
    Administra el ciclo de vida de un canvas de Matplotlib en Tkinter.

    Recibe una figura de Matplotlib, la adapta mediante
    ``FigureCanvasTkAgg`` y coloca el widget resultante dentro del frame
    asignado. Cuando se dibuja una figura nueva, elimina primero el canvas
    anterior para que no se acumulen widgets en la interfaz.
    """

    def __init__(self, frame):
        """
        Prepara el administrador para una zona concreta de la interfaz.

        :param frame: Frame de Tkinter donde se insertará el canvas de
            Matplotlib. Se guarda para reutilizarlo cada vez que se dibuje.
        """
        self.frame = frame
        self.canvas = None

    def draw(self, fig):
        """
        Muestra una figura de Matplotlib dentro del frame.

        :param fig: Objeto figura de Matplotlib que contiene la gráfica que
            se quiere representar.

        Si había un canvas anterior, se destruye su widget de Tkinter. Después
        se crea un adaptador ``FigureCanvasTkAgg``, se renderiza la figura y
        se expande el widget para ocupar todo el frame.
        """
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear(self):
        """
        Retira la figura actualmente mostrada.

        No recibe parámetros ni devuelve valores. Si existe un canvas,
        destruye su widget visual y deja la referencia en ``None`` para
        representar que el área está vacía.
        """
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None