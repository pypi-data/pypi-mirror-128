from titania.plots.base_plot import NavToolbarPlot


class RootScatterPlot(NavToolbarPlot):
    """
    Root scatter plot
    """
    def __init__(self, parent=None, view=None):
        NavToolbarPlot.__init__(self, parent=parent, view=view)

    def draw_plot(self):
        self.figure.clear()
        data = self.view.data.fetch()
        ax = self.figure.add_subplot(self.plot_number)
        data.plot(x='one', y='two', kind='scatter', ax=ax)
        self.draw()

    def get_name(self):
        return "asd"
