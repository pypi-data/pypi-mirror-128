from pandas import np

from titania.plots.base_plot import NavToolbarPlot


class HistogramPlot(NavToolbarPlot):
    """
    Matplotlib's simple bar plot
    """
    def __init__(self, parent=None, view=None, data=None):
        NavToolbarPlot.__init__(self, parent=parent, view=view)
        if data is None:
            self.data = self.view.data.fetch()
        else:
            self.data = data

    def draw_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(self.plot_number)
        min_number = min(self.data)
        max_number = max(self.data)
        ax.bar(list(range(0, len(self.data))), self.data)
        self.draw()

    def get_name(self):
        return "asd"
