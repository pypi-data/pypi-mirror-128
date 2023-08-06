from titania.common.titania_tab import TitaniaPlotTab
from titania.data.examplary_generated_data import RandomNList
from titania.plots import LinePlot


class Thresholds(TitaniaPlotTab):
    def __init__(self, data, plot_cls=LinePlot):
        TitaniaPlotTab.__init__(self, data=data)
        self.PlotClass = plot_cls

    def add_plots_to_layout(self):
        self.grid_layout.addLayout(self.control_panel.get_control_panel(), 0, 0)
        plot1 = self.PlotClass(parent=self.parent, view=self).get_as_plot_widget(row=1)
        plot1.draw_plot(data=self.data)
        self.plot_panel_grid.addWidget(plot1, 0, 0, 1, 3)

    def make_plot(self):
        return LinePlot(parent=self)

    def get_title(self):
        return "ExampleSubTab"

    def create_control_panel(self):
        pass
