from titania.plots.base_plot import NavToolbarPlot, MplPlot

class LinePlot(MplPlot):
    def __init__(self, parent=None, view=None, *args, **kwargs):
        """
        Simple matplotlib line plot class
        """
        MplPlot.__init__(self, parent=parent, view=view)

    def draw_plot(self, data=None) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.view.data.fetch(), '*-')
        self.draw()


class ToolbarLinePlot(NavToolbarPlot):

    def __init__(self, parent=None, view=None):
        """
        A Line Plot with a toolbar
        Args:
        """
        NavToolbarPlot.__init__(self, parent=parent, view=view)

    def draw_plot(self, data=None):
        self.figure.clear()
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.view.data.fetch(), '*-')
        self.draw()

    def get_name(self):
        return "asd"
