import numpy as np
from matplotlib.figure import Figure


class TwoVariablePlotter:

    @staticmethod
    def plot_contour(x_range: tuple, y_range: tuple, f, title: str,
                      x_label: str, y_label: str, best_point: tuple = None) -> Figure:
        """
        Genera un mapa de contorno de f(x, y) sobre el rango dado.
        Si se pasa 'best_point' (x, y), lo marca sobre el gráfico.
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        x_vals = np.linspace(x_range[0], x_range[1], 200)
        y_vals = np.linspace(y_range[0], y_range[1], 200)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.array([[f(xi, yi) for xi in x_vals] for yi in y_vals])

        contour = ax.contourf(X, Y, Z, levels=30, cmap="viridis")
        fig.colorbar(contour, ax=ax, label="f(x, y)")

        if best_point is not None:
            ax.plot(best_point[0], best_point[1], "r*", markersize=15, label="Óptimo encontrado")
            ax.legend()

        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        fig.tight_layout()

        return fig