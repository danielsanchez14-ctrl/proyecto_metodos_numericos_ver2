import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class Plotter:
    @staticmethod
    def plot_function(x_values: list, y_values:list, title:str, x_label:str, y_label:str, function_label:str) -> Figure:
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_values, y_values, label=function_label, color="blue")
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.grid(True)
        ax.legend()
        fig.tight_layout()

        return fig