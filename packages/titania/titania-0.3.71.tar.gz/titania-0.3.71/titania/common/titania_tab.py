from titania.data.data_core import TitaniaDataInterface
from titania.plots.base_plot import PlotInterface
from titania.common.interface_tab import TitaniaTabInterface
from abc import abstractmethod

class TitaniaPlotTab(TitaniaTabInterface):


    def __init__(self, data: TitaniaDataInterface):
        """
        This is a standard parent class for making titania plot tab.
        Args:
            data: data to be used for plotting
        """
        TitaniaTabInterface.__init__(self)
        self.data = data
        self.title = self.get_title()
        self.control_panel = self.create_control_panel()

    @abstractmethod
    def make_plot(self) -> PlotInterface:
        """
        This method is used to create plot for the tab.

        Returns: any class inheriting from PlotInterface

        """
        pass


    @abstractmethod
    def create_control_panel(self):
        """
        Used to initate control panel

        """
        pass

    def initiate(self):
        """
        Initiates and draws plot

        """
        self.plot = self.make_plot()
        self.plot.pre_draw()
        self.plot.draw_plot()
