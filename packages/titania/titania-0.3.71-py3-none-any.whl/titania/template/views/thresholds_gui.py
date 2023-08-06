from titania.QtGUI import QtBaseLayoutTab
from titania.data.examplary_generated_data import RandomNList
from titania.plots import ToolbarLinePlot
from views.thresholds import Thresholds
from panels.control_panel import ControlPanel


class ThresholdsTab(QtBaseLayoutTab, Thresholds):
    def __init__(self, parent=None):
        self.parent = parent
        data = RandomNList()
        QtBaseLayoutTab.__init__(self, data=None, parent=parent)
        Thresholds.__init__(self, data, ToolbarLinePlot)


    def add_plots_to_layout(self):
        Thresholds.add_plots_to_layout(self)

    def make_plot(self):
        return self.PlotClass(parent=self.parent, view=self)

    def create_control_panel(self):
        return ControlPanel(widget=self)
